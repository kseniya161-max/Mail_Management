from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView

from documents.forms import OfferFileForm
from clients.models import Clients
from documents.models import OfferFile
from clients.services.email_service import send_invoice_email, send_offer_email
from documents.services.file_service import generate_offer_file
from products.models import Product
from .forms import InvoiceForm, InvoiceItemFormSet
from documents.services.invoice_generator import generate_invoice_docx
from .models import Invoice
from clients.tasks import send_offerfile_task
from django.conf import settings


class OfferFileCreateView(LoginRequiredMixin, View):
    template_name = "offer_file_create.html"
    model = OfferFile

    def get(self, request):
        form = OfferFileForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = OfferFileForm(request.POST)

        if form.is_valid():
            generate_offer_file(
                user=request.user, products_queryset=form.cleaned_data["products"]
            )
            messages.success(request, "Файл успешно сформирован.")
            return redirect("clients:user_profile")

        return render(request, self.template_name, {"form": form})


class UserOfferFilesView(LoginRequiredMixin, ListView):
    template_name = "user_offer_files.html"
    model = OfferFile
    context_object_name = "offer_files"

    def get_queryset(self):
        return OfferFile.objects.filter(created_by=self.request.user).order_by(
            "-created_at"
        )


class OfferFileDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "user_offer_files_delete.html"
    model = OfferFile
    success_url = reverse_lazy("clients:my_offers")

    def get_queryset(self):
        return OfferFile.objects.filter(created_by=self.request.user)


def health_check(request):
    return JsonResponse({"status": "ok"})


class ClientOfferFileCreateView(LoginRequiredMixin, View):
    template_name = "offer_file_create.html"
    template_name = "offer_file_create.html"

    def get_client(self):
        queryset = Clients.objects.all()
        if self.request.user.role != "manager":
            queryset = queryset.filter(user=self.request.user)
        return get_object_or_404(queryset, pk=self.kwargs["pk"])

    def get(self, request, pk):
        client = self.get_client()
        form = OfferFileForm()

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "client": client,
            },
        )

    def post(self, request, pk):
        client = self.get_client()
        form = OfferFileForm(request.POST)

        if form.is_valid():
            generate_offer_file(
                user=request.user,
                products_queryset=form.cleaned_data["products"],
                client=client,
            )

            messages.success(request, "Предложение для клиента успешно сформировано.")
            return redirect("clients:client_detail", pk=client.pk)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "client": client,
            },
        )


class ClientOfferDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        offer = get_object_or_404(OfferFile, pk=pk, created_by=request.user)

        if offer.file:
            offer.file.delete(save=False)
        client_id = offer.client.id
        offer.delete()

        return redirect("documents:client_offer_files", pk=client_id)


class ClientOfferFilesView(LoginRequiredMixin, ListView):
    template_name = "documents/client_offer_files.html"
    model = OfferFile
    context_object_name = "client_offer_files"

    def get_client(self):
        queryset = Clients.objects.all()

        if self.request.user.role != "manager":
            queryset = queryset.filter(user=self.request.user)

        return get_object_or_404(queryset, pk=self.kwargs["pk"])

    def get_queryset(self):
        self.client = self.get_client()

        queryset = OfferFile.objects.filter(client=self.client)

        if self.request.user.role != "manager":
            queryset = queryset.filter(created_by=self.request.user)

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = self.client
        return context


class InvoiceCreateView(LoginRequiredMixin, View):
    template_name = "documents/invoice_form.html"

    def get(self, request, client_id):
        products = Product.objects.all()
        client = get_object_or_404(Clients, pk=client_id)

        form = InvoiceForm()
        formset = InvoiceItemFormSet()

        return render(
            request,
            self.template_name,
            {
                "client": client,
                "form": form,
                "formset": formset,
                "products": products,
            },
        )

    def post(self, request, client_id):
        client = get_object_or_404(Clients, pk=client_id)

        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)
        products = Product.objects.all()

        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.client = client
            invoice.created_by = request.user
            invoice.save()

            items = formset.save(commit=False)

            for item_form, item in zip(formset.forms, items):
                item.invoice = invoice

                item.product_name = item_form.cleaned_data["product_name_input"]

                if item.product:
                    item.product_name = item.product.name

                item.save()
            file_path = generate_invoice_docx(invoice)

            invoice.file = file_path
            invoice.save()
            return redirect("clients:client_detail", pk=client.pk)

        return render(
            request,
            self.template_name,
            {
                "client": client,
                "form": form,
                "formset": formset,
                "products": products,
            },
        )


class ClientInvoiceListView(View):
    def get(self, request, client_id):
        client = get_object_or_404(Clients, pk=client_id)
        invoices = Invoice.objects.filter(client=client).order_by("-created_at")
        return render(
            request,
            "documents/client_invoice.html",
            {"client": client, "invoices": invoices},
        )


class InvoiceDeleteView(View):
    def post(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk, created_by=request.user)
        client_id = invoice.client.id
        if invoice.file:
            invoice.file.delete(save=False)
        invoice.delete()
        return redirect("documents:client_invoices", client_id=client_id)


class InvoiceSendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk, created_by=request.user)
        try:
            send_invoice_email(invoice)
            invoice.is_sent = True
            invoice.save()
        except Exception as e:
            messages.error(request, f"Ошибка отправки {e}")
        return redirect("documents:client_invoices", client_id=invoice.client.id)


class ClientOfferSendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        offer = get_object_or_404(OfferFile, pk=pk, created_by=request.user)

        try:
            if settings.USE_CELERY:
                send_offerfile_task.delay(offer.id)
            else:
                send_offer_email(offer)

            offer.is_sent = True
            offer.save()
        except Exception as e:
            messages.error(request, f"Ошибка: {e}")

        return redirect("documents:client_offer_files", pk=offer.client.id)

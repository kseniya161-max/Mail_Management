from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from clients.forms import OfferFileForm
from clients.models import Clients, OfferFile
from clients.services.file_service import generate_offer_file
from django.contrib import messages


class ClientOfferFileCreateView(LoginRequiredMixin, View):
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


class ClientOfferFilesView(LoginRequiredMixin, ListView):
    template_name = "client_offer_files.html"
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

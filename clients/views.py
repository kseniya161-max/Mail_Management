from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    DetailView,
)
from clients.services.mailing_service import MailingService
from Users.models import User
from clients.forms import (
    MailingSendForm,
    ClientForm,
    MessageForm,
    UserForm,
    OfferFileForm,
)
from clients.models import (
    Clients,
    Message,
    Mailing,
    MailingAttempt,
    EmailStatistics,
    OfferFile,
)
from django.conf import settings
from django.views.decorators.cache import cache_page
from clients.services.file_service import generate_offer_file
from clients.services.email_service import send_email_via_resend, send_email_via_brevo
from clients.tasks import send_mailing_task
from clients.services.statistics_service import (
    get_email_statistics_for_user,
    get_email_statistics_summary,
    get_email_statistics_by_category,
)


class ClientListView(LoginRequiredMixin, ListView):
    model = Clients
    template_name = "client_list.html"
    context_object_name = "list_clients"

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)

        location = self.request.GET.get("location")
        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Clients
    form_class = ClientForm
    template_name = "client_create.html"
    success_url = reverse_lazy("clients:client_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Clients
    form_class = ClientForm
    template_name = "client_edit.html"
    success_url = reverse_lazy("clients:client_list")

    def get_queryset(self):
        return Clients.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Clients
    template_name = "client_delete.html"
    success_url = reverse_lazy("clients:client_list")

    def get_queryset(self):
        return Clients.objects.filter(user=self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "message_list.html"
    context_object_name = "list_messages"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == "manager":
            return queryset
        return Message.objects.filter(user=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "message_create.html"
    success_url = reverse_lazy("clients:message_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "message_update.html"
    success_url = reverse_lazy("clients:message_list")

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "message_delete.html"
    success_url = reverse_lazy("clients:message_list")

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing_list.html"
    context_object_name = "list_mailing"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == "manager":
                return Mailing.objects.all()
            else:
                return Mailing.objects.filter(user=self.request.user)
        else:
            return Mailing.objects.none()


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingSendForm
    template_name = "mailing_create.html"
    success_url = reverse_lazy("clients:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingSendForm
    template_name = "mailing_update.html"
    success_url = reverse_lazy("clients:mailing_list")

    def get_queryset(self):
        if self.request.user.role == "manager":
            return Mailing.objects.filter(user=self.request.user)
        return super().get_queryset()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing_delete.html"
    success_url = reverse_lazy("clients:mailing_list")

    def get_queryset(self):
        if self.request.user.role == "manager":
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)


# class MailingSendView(LoginRequiredMixin, CreateView):
#     form_class = MailingSendForm
#     template_name = "mailing_send.html"
#     success_url = reverse_lazy("clients:mailing_list")
#
#     def form_valid(self, form):
#         mailing = form.save(commit=False)
#         mailing.user = self.request.user
#         mailing.status = "started"
#         mailing.save()
#         form.save_m2m()
#
#         if settings.USE_CELERY:
#             send_mailing_task.delay(mailing.id)
#             messages.success(self.request, "Рассылка поставлена в очередь на отправку")
#         else:
#             MailingService.send_mailing(mailing, self.request.user)
#             mailing.status = "completed"
#             mailing.save()
#             messages.success(self.request, "Рассылка отправлена")
#
#         return redirect(self.success_url)


class MailingSendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, user=request.user)
        mailing.status = "started"
        mailing.save()

        if settings.USE_CELERY:
            send_mailing_task.delay(mailing.id)
            messages.success(request, "Рассылка поставлена в очередь на отправку")
        else:
            MailingService.send_mailing(mailing, request.user)
            mailing.status = "completed"
            mailing.save()
            messages.success(request, "Рассылка отправлена")

        return redirect("clients:mailing_list")


@method_decorator(cache_page(60 * 3), name="dispatch")
class HomePageView(TemplateView):
    template_name = "home.html"


class EmailStatisticsView(LoginRequiredMixin, ListView):
    model = EmailStatistics
    template_name = "email_statistic.html"
    context_object_name = "statistic"

    def get_queryset(self):
        return get_email_statistics_for_user(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_email_statistics_summary(self.object_list))
        context["category_statistics"] = get_email_statistics_by_category(self.request.user)
        return context


class ManegerClientListView(LoginRequiredMixin, ListView):
    model = Clients
    template_name = "manager_client_list.html"
    context_object_name = "list_clients"

    def get_queryset(self):
        return Clients.objects.all()


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user_profile.html"
    context_object_name = "user_profile"

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "user_profile_update.html"
    success_url = reverse_lazy("clients:user_profile")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = self.request.user
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        if "avatar" in self.request.FILES:
            user.avatar = self.request.FILES["avatar"]
        user.save()
        messages.success(self.request, "Профиль успешно обновлён!")
        return super().form_valid(form)


class DeactivateMailingView(LoginRequiredMixin, View):
    def post(self, request, mailing_id):
        if request.user.role != "manager":
            messages.error(request, "Только менеджер может отключить рассылку.")
            return redirect("clients:mailing_list")

        mailing = get_object_or_404(Mailing, id=mailing_id)
        mailing.status = "closed"
        mailing.save()
        messages.success(request, "Рассылка успешно отключена.")
        return redirect("clients:mailing_list")


class DeactivateMailingConfirmView(LoginRequiredMixin, View):
    def get(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, id=mailing_id)
        return render(request, "deactivate_mailing_confirm.html", {"mailing": mailing})

    def post(self, request, mailing_id):
        if request.user.role != "manager":
            messages.error(request, "Только менеджер может отключить рассылку.")
            return redirect("clients:mailing_list")

        mailing = get_object_or_404(Mailing, id=mailing_id)
        mailing.status = "closed"
        mailing.save()
        messages.success(request, "Рассылка успешно отключена.")
        return redirect("clients:mailing_list")


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

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView

from Users.models import User
from clients.forms import MailingSendForm, ClientForm, MessageForm, UserForm
from clients.models import Clients, Message, Mailing, MailingAttempt, EmailStatistics
from django.conf import settings
from django.views.decorators.cache import cache_page


class ClientListView(LoginRequiredMixin, ListView):
    model = Clients
    template_name = 'client_list.html'
    context_object_name = 'list_clients'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)

        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Clients
    form_class = ClientForm
    template_name = 'client_create.html'
    success_url = reverse_lazy('clients:client_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Clients
    form_class = ClientForm
    template_name = 'client_edit.html'
    success_url = reverse_lazy('clients:client_list')

    def get_queryset(self):
        return Clients.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientDeleteView(DeleteView):
    model = Clients
    template_name = 'client_delete.html'
    success_url = reverse_lazy('clients:client_list')

    def get_queryset(self):
        return Clients.objects.filter(user=self.request.user)

    # def delete(self, request, *args, **kwargs):
    #     response = super().delete(request, *args, **kwargs)
    #     return response


class MessageListView(ListView):
    model = Message
    template_name = 'message_list.html'
    context_object_name = 'list_messages'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_create.html'
    success_url = reverse_lazy('clients:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_update.html'
    success_url = reverse_lazy('clients:message_list')

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'message_delete.html'
    success_url = reverse_lazy('clients:message_list')

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_list.html'
    context_object_name = 'list_mailing'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 'manager':
                return Mailing.objects.all()
            else:
                return Mailing.objects.filter(user=self.request.user)
        else:
            return Mailing.objects.none()


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingSendForm
    template_name = 'mailing_create.html'
    success_url = reverse_lazy('clients:mailing_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingSendForm
    template_name = 'mailing_update.html'
    success_url = reverse_lazy('clients:mailing_list')

    def get_queryset(self):
        if self.request.user.role == 'manager':
            return Mailing.objects.filter(user=self.request.user)
        return super().get_queryset()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing_delete.html'
    success_url = reverse_lazy('clients:mailing_list')

    def get_queryset(self):
        if self.request.user.role == 'manager':
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)


class MailingSendView(CreateView):
    form_class = MailingSendForm
    template_name = 'mailing_send.html'
    success_url = reverse_lazy('clients:mailing_list')

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.user = self.request.user
        mailing.status = 'started'
        mailing.save()
        form.save_m2m()

        self.send_mailing(mailing)

        mailing.status = 'completed'
        mailing.save()

        messages.success(self.request, 'Рассылка обработана')
        return redirect(self.success_url)

    def send_mailing(self, mailing):
        success_count = 0
        failed_count = 0

        for recipient in mailing.recipients.all():
            try:
                sent_count = send_mail(
                    mailing.message.header,
                    mailing.message.content,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient.email],
                    fail_silently=False,
                )

                if sent_count == 1:
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status='success',
                        server_response=f'SMTP accepted message for {recipient.email}',
                    )
                    success_count += 1
                else:
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status='failed',
                        server_response=f'SMTP did not accept message for {recipient.email}',
                    )
                    failed_count += 1

            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status='failed',
                    server_response=str(e),
                )
                failed_count += 1

        EmailStatistics.objects.update_or_create(
            user=self.request.user,
            mailing=mailing,
            defaults={
                'success_attempt_mailing': success_count,
                'failed_attempt_mailing': failed_count,
            }
        )

@method_decorator(cache_page(60 * 3), name='dispatch')
class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailing'] = Mailing.objects.count()
        context['active_mailing'] = Mailing.objects.filter(status='started').count()
        context['unique_recipients'] = Clients.objects.count()
        return context


class EmailStatisticsView(LoginRequiredMixin, ListView):
    model = EmailStatistics
    template_name = 'email_statistic.html'
    context_object_name = 'statistic'

    def get_queryset(self):
        if self.request.user.role == 'manager':
            return EmailStatistics.objects.select_related('mailing').values(
                'mailing__message__header', 'mailing__status', 'user__username'
            ).annotate(
                total_success=Sum('success_attempt_mailing'),
                total_failed=Sum('failed_attempt_mailing')
            ).order_by('mailing__message__header')
        else:
            return EmailStatistics.objects.filter(user=self.request.user).select_related('mailing').values(
                'mailing__message__header', 'mailing__status', 'user__username'
            ).annotate(
                total_success=Sum('success_attempt_mailing'),
                total_failed=Sum('failed_attempt_mailing')
            ).order_by('mailing__message__header')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_success'] = sum(stat['total_success'] for stat in self.object_list)
        context['total_failed'] = sum(stat['total_failed'] for stat in self.object_list)
        context['total_attempts'] = context['total_success'] + context['total_failed']
        return context


class ManegerClientListView(ListView):
    model = Clients
    template_name = 'manager_client_list.html'
    context_object_name = 'list_clients'

    def get_queryset(self):
        return Clients.objects.all()


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_profile_update.html'
    success_url = reverse_lazy('clients:user_profile')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        if 'avatar' in self.request.FILES:
            user.avatar = self.request.FILES['avatar']
        user.save()
        messages.success(self.request, 'Профиль успешно обновлён!')
        return super().form_valid(form)


class DeactivateMailingView(LoginRequiredMixin, View):
    def post(self, request, mailing_id):
        if request.user.role != 'manager':
            messages.error(request, 'Только менеджер может отключить рассылку.')
            return redirect('clients:mailing_list')

        mailing = get_object_or_404(Mailing, id=mailing_id)
        mailing.status = 'closed'
        mailing.save()
        messages.success(request, 'Рассылка успешно отключена.')
        return redirect('clients:mailing_list')


class DeactivateMailingConfirmView(LoginRequiredMixin, View):
    def get(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, id=mailing_id)
        return render(request, 'deactivate_mailing_confirm.html', {'mailing': mailing})

    def post(self, request, mailing_id):
        if request.user.role != 'manager':
            messages.error(request, 'Только менеджер может отключить рассылку.')
            return redirect('clients:mailing_list')

        mailing = get_object_or_404(Mailing, id=mailing_id)
        mailing.status = 'closed'
        mailing.save()
        messages.success(request, 'Рассылка успешно отключена.')
        return redirect('clients:mailing_list')

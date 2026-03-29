from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetCompleteView, PasswordResetConfirmView
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from itsdangerous import URLSafeTimedSerializer
from Users.forms import UserRegisterForm, CustomAuthenticationForm
from Users.models import User
from clients.models import EmailStatistics
from config import settings
from django.core.mail import send_mail


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        if self.request.user.role == 'manager':
            return User.objects.all()
        return User.objects.none()


class CreateUserView(CreateView):
    """Создаем представление для регистрации"""
    model = User
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('Users:login')

    def form_valid(self, form):
        user = form.save()
        self.send_confirmation_email(user)
        messages.success(self.request, 'Ваш аккаунт был успешно создан! Проверьте Вашу почту для подтверждения.')
        return super().form_valid(form)

    def send_confirmation_email(self, user):
        """Отправка письма для Подтверждение Email"""
        s = URLSafeTimedSerializer(settings.SECRET_KEY)
        token = s.dumps(user.email, salt='email-confirmation')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirmation_link = f"http://localhost:8000/users/confirm/{uid}/{token}/"
        subject = 'Подтверждение email'
        message = render_to_string('email_confirmation.html', {
            'confirmation_link': confirmation_link,
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


User = get_user_model()


def confirm_email(request, uidb64, token):
    """Подтверждение Email"""
    try:
        s = URLSafeTimedSerializer(settings.SECRET_KEY)
        email = s.loads(token, salt='email-confirmation', max_age=3600)
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        if user.email == email:
            user.email_verified = True
            user.save()
            messages.success(request, 'Ваш email был успешно подтвержден!')
            return redirect('Users:login')
    except Exception as e:
        messages.error(request, 'Ссылка для подтверждения недействительна или истекла.')
        messages.error(request, f"Ошибка при подтверждении email: {e}")
    return redirect('Users:register')


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = EmailStatistics.objects.filter(user=self.object).values(
            'mailing__datetime_start'
        ).annotate(
            total_success=Sum('success_attempt_mailing'),
            total_failed=Sum('failed_attempt_mailing')
        )
        context['user_statistics'] = list(stats)
        return context


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('clients:user_profile')

    def __str__(self):
        return CustomLoginView


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('Users:login')

    def __str__(self):
        return CustomLogoutView


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('Users:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    success_url = reverse_lazy('Users:password_reset_confirm')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('Users:password_reset_complete')


class BlockUserView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        if request.user.role != 'manager':
            messages.error(request, 'У вас нет прав для блокировки пользователя')
            return redirect('Users:user_block_confirm')

        user = get_object_or_404(User, id=user_id)
        user.is_active = False
        user.save()
        messages.success(request, 'Пользователь успешно заблокирован')
        return redirect('Users:user_block_confirm')


class UnblockUserView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        if request.user.role != 'manager':
            messages.error(request, 'У вас нет прав для разблокировки пользователя')
            return redirect('Users:user_list')

        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save()
        messages.success(request, 'Пользователь успешно разблокирован')
        return redirect('Users:user_list')


class BlockUserConfirmationView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, 'user_block_confirm.html', {'user': user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.is_active = False
        user.save()
        messages.success(request, 'Пользователь успешно заблокирован.')
        return redirect('Users:user_list')


class UnBlockUserConfirmationView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return render(request, 'user_unblock_confirm.html', {'user': user})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save()
        messages.success(request, 'Пользователь успешно разблокирован.')
        return redirect('Users:user_list')



from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from Users.models import User
from clients.services.email_service import send_email_via_resend
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string



class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password1",
            "password2",
            "avatar",
            "country",
            "phone_number",
        )

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите email"}
        )
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите имя пользователя"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите пароль"}
        )

        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите еще раз пароль"}
        )

        self.fields["avatar"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Загрузите аватар"}
        )

        self.fields["country"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите страну"}
        )

        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите номер телефона"}
        )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите Email"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        )
    )

    class Meta:
        model = User
        fields = ["username", "password"]


class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        subject = render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())

        body = render_to_string(email_template_name, context)

        send_email_via_resend(
            to_email=to_email,
            subject=subject,
            body=body,
        )



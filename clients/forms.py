from django.forms import ModelForm
from django.core.exceptions import ValidationError
from Users.models import User
from clients.models import Message, Clients, Mailing, OfferFile, City
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from products.models import Product


class ClientForm(ModelForm):
    """Форма Создания клиента"""
    phone_number = PhoneNumberField()

    class Meta:
        model = Clients
        fields = ["email", "name", "comment", "location", "phone_number"]

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

        self.fields["location"].queryset = City.objects.order_by('name')
        self.fields["location"].empty_label = "Выберите город ..."
        self.fields["location"].widget.attrs.update(
            {"class": "form-control select2", "data-placeholder": "Начните вводить название города..."}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите email"}
        )
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите Имя"}
        )
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "+79998887766"}
        )
        self.fields["phone_number"].required = True
        self.fields["comment"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите комментарий"}
        )
        self.fields["location"].required = False

    def clean_email(self):
        """Валидация email"""
        email = self.cleaned_data.get("email")
        queryset = Clients.objects.filter(email=email)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise ValidationError("Пользовталь с таким email уже существует")
        return email


class MessageForm(ModelForm):
    """Форма Создания сообщения"""

    class Meta:
        model = Message
        fields = ["header", "content", "product", "offer_file"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["header"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите Заголовок"}
        )
        self.fields["content"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите Контент"}
        )
        self.fields["product"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите товар"}
        )
        self.fields["offer_file"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Файл"}
        )

        if user:
            self.fields["offer_file"].queryset = OfferFile.objects.filter(
                created_by=user
            )


class MailingSendForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["recipients", "message", "status", "datetime_start", "datetime_end"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(MailingSendForm, self).__init__(*args, **kwargs)
        self.fields["recipients"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите получателя"}
        )
        self.fields["message"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберите сообщение"}
        )
        self.fields["status"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберите статус"}
        )
        self.fields["datetime_start"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Дата старта"}
        )
        self.fields["datetime_end"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Дата окончания"}
        )
        if user and user.role != "manager":
            self.fields["recipients"].queryset = Clients.objects.filter(user=user)

        if user and user.role != "manager":
            self.fields["message"].queryset = Message.objects.filter(user=user)

        if user and user.role == "manager":
            self.fields["recipients"].queryset = Clients.objects.all()

        if user and user.role == "manager":
            self.fields["message"].queryset = Message.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        datetime_start = cleaned_data.get("datetime_start")
        datetime_end = cleaned_data.get("datetime_end")
        if datetime_start and datetime_end and datetime_end < datetime_start:
            raise ValidationError("Дата завершения не может быть больше даты начала")
        return cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "avatar",
            "country",
            "phone_number",
            "role",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "role": forms.TextInput(attrs={"class": "form-control"}),
        }


class OfferFileForm(forms.Form):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите продукты",
    )

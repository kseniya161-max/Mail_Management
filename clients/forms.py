from django.forms import ModelForm
from django.core.exceptions import ValidationError

from Users.models import User
from clients.models import Message, Clients, Mailing
from django import forms


class ClientForm(ModelForm):
    """ Форма Создания клиента"""
    class Meta:
        model = Clients
        fields = ['email', 'name', 'comment', 'location']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите email'})
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите Имя'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Напишите комментарий'})
        self.fields['location'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите город'})

    def clean_email(self):
        """ Валидация email"""
        email = self.cleaned_data.get('email')
        if Clients.objects.filter(email=email).exists():
            raise ValidationError('Пользовталь с таким email уже существует')
        return email


class MessageForm(ModelForm):
    """ Форма Создания сообщения"""

    class Meta:
        model = Message
        fields = ['header', 'content', 'product']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['header'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите Заголовок'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите Контент'})
        self.fields['product'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите товар'})


class MailingSendForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['recipients', 'message', 'status', 'datetime_start', 'datetime_end']

    def __init__(self, *args, **kwargs):
        super(MailingSendForm, self).__init__(*args, **kwargs)
        self.fields['recipients'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите получателя'})
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Выберите сообщение'})
        self.fields['status'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Выберите статус'})
        self.fields['datetime_start'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Дата старта'})
        self.fields['datetime_end'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Дата окончания'})

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        datetime_start = cleaned_data.get('datetime_start')
        datetime_end = cleaned_data.get('datetime_end')
        if datetime_start and datetime_end and  datetime_end < datetime_start:
            raise ValidationError('Дата завершения не может быть больше даты начала')
        return cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'country', 'phone_number', 'role',]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
        }
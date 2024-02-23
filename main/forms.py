from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    """
        Форма для регистрации нового пользователя.

    Наследует от UserCreationForm и добавляет дополнительные поля для логина,
    адреса электронной почты, пароля и подтверждения пароля. Поля настроены
    с пользовательскими классами CSS для улучшения внешнего вида.

    :param username: Поле для ввода логина пользователя.
    :param email: Поле для ввода адреса электронной почты.
    :param password1: Поле для ввода пароля.
    :param password2: Поле для подтверждения пароля.
    """
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    """
    Форма для входа пользователя в систему.

    Наследует от AuthenticationForm и добавляет поля для логина и пароля с
    пользовательскими классами CSS. Предоставляет функционал для аутентификации пользователя.

    :param username: Поле для ввода логина пользователя.
    :param password: Поле для ввода пароля пользователя.
    """
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input form-control'}))

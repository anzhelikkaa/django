from django import forms
from .models import Order
import re
from django.core.exceptions import ValidationError

def validate_ukrainian_phone(value):
    if not re.match(r'^\+380\d{9}$', value):
        raise ValidationError("Введіть номер у форматі +380XXXXXXXXX")

class OrderForm(forms.ModelForm):
    name = forms.CharField(
        label="Ім'я та прізвище",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ваше повне ім'я"})
    )
    email = forms.EmailField(
        label="Електронна пошта",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "example@email.com"})
    )
    phone = forms.CharField(
        label="Мобільний номер",
        validators=[validate_ukrainian_phone],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "+380XXXXXXXXX"})
    )
    address = forms.CharField(
        label="Адреса доставки",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Область, місто, вулиця, будинок, квартира", 'rows': 3})
    )

    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'address']

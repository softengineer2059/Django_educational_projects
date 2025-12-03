from .models import Order
from django import forms
from django.core.validators import EmailValidator


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес'}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пост код'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город'}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city'] #__all__
        """widgets = {
            "first_name": forms.CharField(attrs={'class': 'form-control'}),
        }"""

        """def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['product_name'].widget.attrs.update({'class': 'control mb-4'})

        field_classes = {
                    "product_name": forms.TextInput(attrs={'class': 'form-control mb-4'}),
                }"""


class OrderForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )

    last_name = forms.CharField(
        max_length=100,
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        })
    )

    email = forms.EmailField(
        max_length=254,
        label='Email',
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@email.com'
        })
    )

    address = forms.CharField(
        max_length=255,
        label='Адрес доставки',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите полный адрес доставки',
            'rows': 3
        })
    )

    postal_code = forms.CharField(
        max_length=20,
        label='Почтовый индекс',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123456'
        })
    )

    city = forms.CharField(
        max_length=100,
        label='Город',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш город'
        })
    )

    phone = forms.CharField(
        max_length=20,
        label='Телефон',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (XXX) XXX-XX-XX'
        })
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Базовая валидация телефона (можно доработать)
            phone = ''.join(filter(str.isdigit, phone))
            if len(phone) < 10:
                raise forms.ValidationError("Введите корректный номер телефона")
        return phone
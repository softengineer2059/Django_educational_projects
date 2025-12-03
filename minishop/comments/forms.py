from django import forms
from .models import *




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text', 'grade']  # Укажите поля, которые хотите использовать
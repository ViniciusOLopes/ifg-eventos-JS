
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from ifg_eventos.models import Student


class RegisterForm(UserCreationForm):

    # Dados do aluno
    name = forms.CharField(
        max_length=50,
        label='Nome completo'
    )

    email = forms.EmailField(
        label='E-mail'
    )

    cpf = forms.CharField(
        max_length=14,
        required=False,
        label='CPF'
    )

    cellphone = forms.CharField(
        max_length=15,
        required=False,
        label='Celular'
    )

    class Meta:
        model = User
        fields = ['username']

    def clean_email(self):
        email = self.cleaned_data['email']

        if Student.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'Este e-mail já está cadastrado.'
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            with transaction.atomic():
                user.save()

                Student.objects.create(
                    user=user,
                    name=self.cleaned_data['name'],
                    email=self.cleaned_data['email'],
                    cpf=self.cleaned_data['cpf'] or None,
                    cellphone=self.cleaned_data['cellphone'] or None
                )

        return user

from django import forms
from .models import Event, Registration, Student

class RegisterForm(forms.ModelForm):

    class Meta:
        model = Registration
        fields = ['name']
        labels = {'name':''}
        widgets = {
            'name': forms.TextInput(attrs={
                'style': 'font-size: 18px'
            })}

class EventForm(forms.ModelForm):
    """
    Criando os eventos e adicionano informações.
    """
    class Meta:
        model = Event
        fields = ['name',
                  'description',
                  'start_date',
                  'end_date',
                  'max_registration'
                  ]
        labels = {'name':'',
                  'description':'',
                  'start_date':'',
                  'end_date':'',
                  'max_registration':''
                  }
        widgets = {
            'name': forms.TextInput(attrs={
                'style': 'font-size: 18px'}),
                
            'description': forms.Textarea(attrs={
                'style': 'font-size: 18px',
                'cols':48
            }),

            'start_date':forms.TextInput(attrs={
                'style': 'font-size: 18px'
            }),

            'end_date':forms.TextInput(attrs={
                'style': 'font-size: 18px'
            }),

            'max_registration':forms.TextInput(attrs={
                'style': 'font-size: 18px'
            })
        }
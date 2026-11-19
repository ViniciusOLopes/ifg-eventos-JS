from django import forms
from .models import Event, Registration, Student

class RegisterForm(forms.ModelForm):

    class Meta:
        model = Registration
        fields = ['student']
        labels = {'student':''}
        widgets = {
            'student': forms.Select(attrs={
                'style': 'font-size: 18px'
            })}

class EventForm(forms.ModelForm):
    """
    Criando os eventos e adicionano informações.
    """
    start_date = forms.DateTimeField(
        label='Data de início',
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.TextInput(attrs={
            'style': 'font-size: 18px',
            'placeholder': 'Ex: 19/11/2026 14:00'
        })
    )

    end_date = forms.DateTimeField(
        label='Data de fim',
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.TextInput(attrs={
            'style': 'font-size: 18px',
            'placeholder': 'Ex: 19/11/2026 18:00'
        })
    )
    class Meta:
        
        model = Event
        fields = ['name',
                  'description',
                  'start_date',
                  'end_date',
                  'max_registration',
                  'local',
                  'latitude',
                  'longitude'
                  ]
        labels = {'name':'Nome do Evento',
                  'description':'Descrição',
                  'start_date':'Data de inicio',
                  'end_date':'Data de fim',
                  'max_registration':'Máximo de inscrições',
                  'local':'Localização',
                  }
        widgets = {
            'name': forms.TextInput(attrs={
                'style': 'font-size: 18px'}),
                
            'description': forms.Textarea(attrs={
                'style': 'font-size: 18px',
                'cols':48
            }),

            'max_registration':forms.TextInput(attrs={
                'style': 'font-size: 18px'
            }),

            'local':forms.TextInput(attrs={
                'id': 'local',
                'style': 'font-size: 18px',
                'readonly': 'readonly',
                'placeholder': 'Clique em "Selecionar no Mapa"'
            }),
            
            'latitude': forms.HiddenInput(attrs={'id': 'latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'longitude'}),
            
        }
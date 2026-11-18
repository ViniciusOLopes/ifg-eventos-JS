from django.shortcuts import render
from .models import Event, Registration, Student

# Create your views here.
def index(request):
    """
    Pagina inicial do sistema
    """
    return render(request,'ifg_eventos/index.html')

def event(request, event_id):
    """
    Mostra o Evento selecionado
    """
    event = Event.objects.get(id = event_id)
    registrations = event.registration_set.order_by('date_added')

    context = {'event':event, 'registrations':registrations}

    return render(request, 'ifg_eventos/event.html', context)

def list_events(request):
    """
    Lista todos os eventos criados e disponiveis para inscrição.
    """
    event = Event.objects.order_by('date_added')
    context = {'event':event}

    return render(request, 'ifg_eventos/list_events.html', context)

def register(request):
    """
    Registrar um aluno no evento.
    """
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            
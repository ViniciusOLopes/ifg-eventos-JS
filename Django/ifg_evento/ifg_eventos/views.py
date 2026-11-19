from django.shortcuts import render
from .models import Event, Registration, Student
from .forms import RegisterForm, EventForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse


# Create your views here.
def index(request):
    """
    Pagina inicial do sistema
    """
    return render(request,'ifg_eventos/index.html')


def sobre(request):
    """
    Pagina que mostra um resumo do uso do aplicativo.
    """
    return render(request, 'ifg_eventos/sobre.html')


def event(request, event_id):
    """
    Mostra o Evento selecionado
    """
    event = Event.objects.get(id = event_id)
    registrations = event.registration_set.order_by('date_added')

    context = {'event':event, 'registrations':registrations}

    return render(request, 'ifg_eventos/event.html', context)


def add_event(request):
    """
    Cria um novo envento.
    """
    if request.method != "POST":
        form = EventForm()
    else:
        form = EventForm(request.POST)

        if form.is_valid():
            new_event = form.save(commit = False)
            new_event.save()

            return HttpResponseRedirect(reverse('list_events'))
        
    context = {'form':form}
    return render(request, 'ifg_eventos/add_event.html', context)


def list_events(request):
    """
    Lista todos os eventos criados e disponiveis para inscrição.
    """
    event = Event.objects.order_by('date_added')
    context = {'event':event}

    return render(request, 'ifg_eventos/list_events.html', context)


def register(request, event_id):
    """
    Registrar um aluno no evento.
    """
    event = Event.objects.get(id = event_id)

    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)

        if form.is_valid():
            """Busca o ID do student dado pelo post"""
            student_id = request.POST.get('student') 

            """Instancia um student"""
            student, create = Student.objects.get_or_create(id=student_id)
            
            new_registration = form.save(commit=False)
            new_registration.student = student
            new_registration.event = event
            new_registration.save()

            return HttpResponseRedirect(reverse('list_events'))


    context = {'event':event,'form':form}
    return render(request, 'ifg_eventos/register.html', context)
            
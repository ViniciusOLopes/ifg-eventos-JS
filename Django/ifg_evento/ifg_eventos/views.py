from django.shortcuts import get_object_or_404, render
from .models import Event, Registration, Student
from .forms import RegisterForm, EventForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages


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

    event = get_object_or_404(Event, id=event_id)

    registrations = Registration.objects.filter(event=event)

    total_inscritos = registrations.count()

    vagas_disponiveis = max(
        0,
        event.max_registration - total_inscritos
    )

    context = {
        'event': event,
        'registrations': registrations,
        'total_inscritos': total_inscritos,
        'vagas_disponiveis': vagas_disponiveis,
    }

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
            form.save()
            
            return HttpResponseRedirect(reverse('list_events'))
        
    context = {'form':form}
    return render(request, 'ifg_eventos/add_event.html', context)

def edit_event(request, event_id):
    """
    Modifica os eventos.
    """
    event = Event.objects.get(id = event_id)
    
    if request.method != "POST":
        form = EventForm(instance=event)
    else:
        form = EventForm(instance=event, data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('event', kwargs={'event_id': event.id}))
        
    context = {'event':event, 'form':form}
    return render(request, 'ifg_eventos/edit_event.html',context)


def list_events(request):
    """
    Lista todos os eventos criados e disponiveis para inscrição.
    """
    events = Event.objects.order_by('date_added')
    for event in events:
        total_inscritos = Registration.objects.filter(event= event).count()

        event.total_inscritos = total_inscritos
        event.vagas_disponiveis = max(0, event.max_registration-total_inscritos)

    context = {'event':events}

    return render(request, 'ifg_eventos/list_events.html', context)



def register(request, event_id):
    """
    Registrar um aluno no evento.
    """
    event = Event.objects.get(id=event_id)
    total_inscritos = Registration.objects.filter(event=event).count()

    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)

        if form.is_valid():
            
            # Verifica se o evento ainda possui vagas
            if total_inscritos >= event.max_registration:
                messages.error(request,'Este evento atingiu o limite de inscrições.')
                return HttpResponseRedirect(reverse('event', kwargs={'event_id': event_id}))

            # Busca o ID do aluno enviado pelo formulário
            student_id = request.POST.get('student')

            # Busca ou instancia um Student
            student, created = Student.objects.get_or_create(id=student_id)

            # Verifica se o aluno já está inscrito
            if Registration.objects.filter(student=student,event=event).exists():
                messages.error(request,'Você já está inscrito neste evento!')
                return HttpResponseRedirect(reverse('event', kwargs={'event_id': event_id}))

            # Cria a inscrição
            new_registration = form.save(commit=False)
            new_registration.student = student
            new_registration.event = event
            new_registration.save()

            messages.success(request,'Inscrição realizada com sucesso!')

            return HttpResponseRedirect(reverse('list_events'))

    context = {'event': event, 'form': form}
    return render(request, 'ifg_eventos/register.html', context)

            
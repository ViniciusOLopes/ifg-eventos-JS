from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm


def logout_view(request):
    """
    Faz o logout do usuário.
    """
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    """
    Cria novos usuários e ja conecta com seu respectivo cadastro de aluno
    """
    if request.method != 'POST':
        #RECRIAR FORMULARIO MANUALMENTE
        form = RegisterForm()

    else:
        #Processsa o formulario preenchido
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()

            #Fazendo o login e o redireciona para a pagina inicial
            authenticated_user = authenticate(request,
                                              username = new_user.username,
                                              password = form.cleaned_data['password1'])
            if authenticated_user is not None:
                login(request, authenticated_user)    
                return HttpResponseRedirect(reverse('index'))
        
    context = {'form':form}
    return render(request, 'users/register.html', context)
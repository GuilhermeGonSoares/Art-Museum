from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST
from museum.models import Painting

from .forms import LoginForm, RegisterForm


#UTILIZAR A SESSÃO DO USUÁRIO PARA PODER TRAFEGAR DADOS DE UMA VIEW PARA OUTRA
#UMA VEZ QUE SÃO VIEWS DIFERENTES. CADA UMA COM SUA RESPONSABILIDADE
@require_GET
def register(request: HttpRequest)-> HttpResponse:
    register_form = request.session.get('register_form_data', None)
    
    form = RegisterForm(register_form)

    return render(request, 'user/pages/register.html', {
        'form': form,
        'form_action': 'user:register_create',
        'search': False,
    })

#ESSA VIEW É APENAS PARA TRATAR OS DADOS NÃO IRÁ RENDERIZAR
#DEPENDENDO ELE CRIA O USUÁRIO OU RETORNA PARA REGISTER MOSTRANDO OS ERROS
@require_POST
def register_create(request: HttpRequest)-> HttpResponse:
    
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, "Usuário criado, por favor faça o log in.")

        del(request.session['register_form_data'])
        return redirect('user:login')

    return redirect('user:register')

@require_GET
def login_view(request:HttpRequest)-> HttpResponse:
    login_form = LoginForm()
    
    return render(request, 'user/pages/login.html',{
        'form': login_form,
        'form_action': 'user:login_create',
        'search': False,
    })

@require_POST
def login_create(request: HttpRequest)-> HttpResponse:
    
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username', '')
        password = login_form.cleaned_data.get('password', '')
        authenticated_user = authenticate(request,
            username = username,
            password = password
        )
        if authenticated_user is not None:
            messages.success(request, f'Usuário {username} logado com sucesso!')
            login(request, authenticated_user)
            return redirect('user:dashboard')
        
        messages.error(request, 'Login inválido! Por favor, tente novamente.')
        return redirect('user:login')
    
    messages.error(request, 'Error ao validar o formulário.')
    return redirect('user:login')

#Utilizamos uma proteção para o nosso logout para ele não aceitar requisição GET
#com isso para deslogar tem que ser necessariamente pelo site
@require_POST
@login_required(login_url='user:login', redirect_field_name='next')
def logout_user(request: HttpRequest)-> HttpResponse:
    
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Error ao realizar logout')
        return redirect('painting:home')
    
    logout(request)
    messages.success(request, 'Usuário deslogado com sucesso')
    return redirect('user:login')

@require_GET
@login_required(login_url='user:login')
def dashboard(request:HttpRequest) -> HttpResponse:
    user = request.user
    paintings = Painting.objects.filter(
        is_published=False, post_author=user
    ).order_by('-id')


    return render(request, 'user/pages/dashboard.html', {
        'paintings': paintings,
        'search': False,
    })

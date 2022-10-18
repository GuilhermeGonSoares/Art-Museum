from http.client import HTTPResponse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
from museum.models import Painting

from .forms import (LoginForm, RegisterAuthorForm, RegisterChurchForm,
                    RegisterForm, RegisterPaintingForm)


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

@require_http_methods(['GET', 'POST'])
@login_required(login_url='user:login')
def painting_edit(request:HttpRequest, id:int)-> HttpResponse:
    try:
        user = request.user
        painting = Painting.objects.get(
            pk=id,
            is_published=False, 
            post_author=user,
        )
 
    except ObjectDoesNotExist:
        raise Http404("Painter doesn't found in this database!")
    

    form = RegisterPaintingForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=painting
        )

    request.session['painting_edit_id'] = id
    
    if form.is_valid():
        authors = form.cleaned_data['author']
        pant = form.save(commit=False)
        pant.author.set(authors)
        pant.post_author = user
        pant.is_published = False
        pant.save()

        del(request.session['painting_edit_id'])
        messages.success(request, 'Pintura alterada com sucesso!')
        return redirect(reverse('user:painting_edit', args=(id,)))


    return render(request, 'user/pages/dashboard_painting.html', {
        'method': 'Editar',
        'form': form,
        'search': False,
        
    })

@require_http_methods(['GET', 'POST'])
@login_required(login_url='user:login')
def painting_create(request:HttpRequest)-> HttpResponse:
    session_id = request.session.get('painting_edit_id', '')
    if session_id:
        del(request.session['painting_edit_id'])
    
    user = request.user
    form = RegisterPaintingForm(
            data=request.POST or None,
            files=request.FILES or None,
        )
    
    if form.is_valid():
        authors = form.cleaned_data['author']
        pant = form.save(commit=False)
        pant.post_author = user
        pant.is_published = False
        pant.save()
        form.save_m2m()

        messages.success(request, 'Pintura cadastrada com sucesso!')
        return redirect('user:painting_create')


    return render(request, 'user/pages/dashboard_painting.html', {
        'method': 'Criar',
        'form': form,
        'search': False,
    })


@require_http_methods(['GET', 'POST'])
@login_required(login_url='user:login')
def painting_author_create(request:HttpRequest) -> HTTPResponse:
    id = request.session.get('painting_edit_id', '')

    form = RegisterAuthorForm(data=request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Autor cadastrado com sucesso")
        #TENTAR ARMAZENAR NO SESSION OS DADOS QUE ESTAVAM NO FORMULÁRIO ANTES DE CRIAR O AUTOR
        if id:
            return redirect(reverse('user:painting_edit', args=(id,)))
        
        return redirect('user:painting_create')

    return render(request, 'user/pages/dashboard_author.html', {
        'form': form,
        'search': False,
    })

@require_POST
@login_required(login_url='user:login')
def painting_delete(request:HttpRequest, id:int)-> HttpResponse:
    try:
        painting = Painting.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404("Pintura com esse ID não encontrada!")
    
    painting.delete()
    messages.success(request, "Pintura excluida com sucesso.")

    return redirect('user:dashboard')

@require_http_methods(['GET', 'POST'])
@login_required(login_url='user:login')
def painting_church_create(request:HttpRequest) -> HttpResponse:
    id = request.session.get('painting_edit_id', '')

    form = RegisterChurchForm(data=request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Igreja cadastrada com sucesso")
        #TENTAR ARMAZENAR NO SESSION OS DADOS QUE ESTAVAM NO FORMULÁRIO ANTES DE CRIAR O AUTOR
        if id:
            return redirect(reverse('user:painting_edit', args=(id,)))
        
        return redirect('user:painting_create')

    return render(request, 'user/pages/dashboard_church.html', {
        'form': form,
        'search': False,
    })

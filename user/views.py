from audioop import reverse

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)

from .forms import RegisterForm


#UTILIZAR A SESSÃO DO USUÁRIO PARA PODER TRAFEGAR DADOS DE UMA VIEW PARA OUTRA
#UMA VEZ QUE SÃO VIEWS DIFERENTES. CADA UMA COM SUA RESPONSABILIDADE
@require_GET
def register(request: HttpRequest)-> HttpResponse:
    register_form = request.session.get('register_form_data', None)
    
    form = RegisterForm(register_form)

    return render(request, 'user/pages/register.html', {
        'form': form,
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
        return redirect('painting:home')

    return redirect('user:register')

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .forms import RegisterForm


@require_GET
def register(request: HttpRequest)-> HttpResponse:
    form = RegisterForm()

    return render(request, 'user/pages/register.html', {
        'form': form,
    })

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Painting


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    paintings = Painting.objects.all().order_by('-id') 

    return render(request, 'museum/pages/home.html', {
        'paintings': paintings
    })

@require_GET
def detail_painting(request: HttpRequest, painting_id: int) -> HttpResponse:
    try:
        painting = Painting.objects.get(pk=painting_id)
    
    except ObjectDoesNotExist:
        raise Http404('Objects not found in database')
    
    return render(request, 'museum/pages/detail_painting.html', {
        'painting': painting,
        'isDetailPage': True,
    })

@require_GET
def detail_church(request: HttpRequest, id_church: int) -> HttpResponse:
    paintings = Painting.objects.filter(church__id=id_church).order_by('-id')
    if not paintings:
        raise Http404("there are no paintings related to this church id")
    
    return render(request, 'museum/pages/church.html', {
        'paintings': paintings,
        'church': paintings.first().church
    })

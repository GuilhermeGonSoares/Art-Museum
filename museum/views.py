from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .models import Author, Church, Painting


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    paintings = Painting.objects.filter(is_published=True).order_by('-id')

    return render(request, 'museum/pages/home.html', {
        'paintings': paintings
    })

@require_GET
def detail_painting(request: HttpRequest, painting_id: int) -> HttpResponse:
    try:
        painting = Painting.objects.get(pk=painting_id, is_published=True)
    
    except ObjectDoesNotExist:
        raise Http404('Objects not found in database')
    
    return render(request, 'museum/pages/detail_painting.html', {
        'painting': painting,
        'isDetailPage': True,
    })

@require_GET
def detail_church(request: HttpRequest, id_church: int) -> HttpResponse:
    paintings = Painting.objects.filter(church__id=id_church, is_published=True).order_by('-id')
    if not paintings:
        raise Http404("there are no paintings related to this church id")
    
    return render(request, 'museum/pages/church.html', {
        'paintings': paintings,
        'church': paintings.first().church
    })

@require_GET
def detail_painter(request: HttpRequest, id_painter: int)-> HttpResponse:
    try:
        painter = Author.objects.get(pk=id_painter)
        paintings_this_painter = painter.painting_set.filter(is_published=True).order_by('-id')
    except ObjectDoesNotExist:
        raise Http404("Painter doesn't found in this database!")

    return render(request, 'museum/pages/painter.html', {
        'painter': painter,
        'paintings': paintings_this_painter,
    })

@require_GET
def search(request: HttpRequest)-> HttpResponse:
    filter = request.GET.get("filter", "paintings")
    search = request.GET.get("q", "")
    
    if filter == 'paintings':
        template = 'museum/pages/search.html'
        paintings = Painting.objects.filter(
            Q(
                Q(name__icontains=search) | Q(summary__icontains=search) 
            ) & Q(is_published=True)
        ).order_by('-id')
        
        return render(request, template, {
            'paintings': paintings
        })

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from utils.pagination import pagination

from .models import Author, Church, Painting


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    current_page = int(request.GET.get('page', 1))
    paintings = Painting.objects.filter(is_published=True).order_by('-id')
    paginator = Paginator(paintings, 6)

    page = pagination(paginator, current_page)
    return render(request, 'museum/pages/home.html', {
        'paintings': page['paintings'],
        'pagination': page['pagination'],
        'current_page': current_page,
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
def churches(request:HttpRequest) -> HttpResponse:
    churches_paintings = []
    churches = Church.objects.filter(painting__is_published = True).distinct().order_by('-id')
    for church in churches:
        churches_paintings.append((church, church.painting_set.count()))
    
    return render(request, 'museum/pages/search_church.html',{
            'churches': churches_paintings,
            'search_result': search,
            'filterChurch': 'selected',
        })


@require_GET
def detail_church(request: HttpRequest, id_church: int) -> HttpResponse:
    paintings = Painting.objects.filter(church__id=id_church, is_published=True).order_by('-id')
    if not paintings:
        raise Http404("there are no paintings related to this church id")
    
    return render(request, 'museum/pages/church.html', {
        'paintings': paintings,
        'church': paintings.first().church,
        'filterChurch': 'selected',
    })

@require_GET
def painters(request: HttpRequest) -> HttpResponse:
    painter_paintings = []
    painters = Author.objects.filter(painting__is_published = True).distinct().order_by('-id')
    for painter in painters:
        painter_paintings.append((painter, painter.painting_set.count()))
    
    return render(request, 'museum/pages/search_painter.html',{
            'painters': painter_paintings,
            'search_result': search,
            'filterPainter': 'selected',
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
        'filterPainter': 'selected',
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
            'paintings': paintings,
            'search_result': search,
        })

    if filter == 'churches':
        template = 'museum/pages/search_church.html'
        churches_with_paintings_published = []
        churches = Church.objects.filter(
            Q(
                Q(name__icontains=search) | Q(city__icontains=search) | Q(state__icontains=search)
            ) 
        ).order_by('-id')
        

        for church in churches:
            painting_this_church = church.painting_set.filter(is_published=True).count()
            if painting_this_church > 0:
                churches_with_paintings_published.append((church, painting_this_church))

        return render(request, template,{
            'churches': churches_with_paintings_published,
            'search_result': search,
            'filterChurch': 'selected',
        })
    
    if filter == "painters":
        template = 'museum/pages/search_painter.html'
        painters_with_paintings_published = []
        authors = Author.objects.filter(name__icontains=search).order_by('-id')

        for painter in authors:
            paintings_this_painter = painter.painting_set.filter(is_published=True).count()
            if paintings_this_painter > 0:
                painters_with_paintings_published.append((painter, paintings_this_painter))
    

        return render(request, template,{
            'painters': painters_with_paintings_published,
            'search_result': search,
            'filterPainter': 'selected',
        })

@require_GET
def detail_painting_not_published(request: HttpRequest, painting_id: int) -> HttpResponse:
    try:
        painting = Painting.objects.get(pk=painting_id, is_published=False)
    
    except ObjectDoesNotExist:
        raise Http404('Objects not found in database')
    
    return render(request, 'museum/pages/detail_painting.html', {
        'painting': painting,
        'isDetailPage': True,
        'search':False,
        
    })

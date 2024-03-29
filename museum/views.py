from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from tag.models import Tag
from utils.pagination import pagination

from .models import Author, Church, Engraving, Painting


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    current_page = int(request.GET.get('page', 1))
    paintings = Painting.objects.filter(is_published=True).order_by('-id')
    paintings = paintings.select_related('church', 'post_author') \
                .defer('description', 'is_published')
    paintings = paintings.prefetch_related('engraving', 'author') \
                .defer('engraving__book', 'engraving__cover')

    page = pagination(paintings, current_page)
    return render(request, 'museum/pages/home.html', {
        'page':page,
        'obras':'-selected',
        'search_action': 'painting:search',
        'placeholder': 'Pesquise as obras pelo nome ou pelo resumo',
    })

@require_GET
def detail_painting(request: HttpRequest, painting_id: int) -> HttpResponse:
    try:
        painting = Painting.objects.select_related('church', 'post_author').prefetch_related('engraving__author', 'author').get(pk=painting_id, is_published=True)
        engravings = painting.engraving.all()
    except ObjectDoesNotExist:
        raise Http404('Objects not found in database')

    return render(request, 'museum/pages/detail_painting.html', {
        'painting': painting,
        'engravings':engravings,
        'range': [i+1 for i in range(engravings.count())],
        'isDetailPage': True,
        'searchbar': False,
        
    })

@require_GET
def tags_paintings(request, slug):
    current_page = int(request.GET.get('page', 1))  
    paintings = Painting.objects.filter(tag__slug=slug)
    tag_name = Tag.objects.get(slug=slug).name
    page = pagination(paintings, current_page)
    return render(request, 'museum/pages/tag_paintings.html', {
        'page':page,
        'tag_name': tag_name,
    })

@require_GET
def churches(request:HttpRequest) -> HttpResponse:
    churches_paintings = []
    churches = Church.objects.filter(painting__is_published = True).distinct().order_by('-id')
    churches = churches.annotate(
        num_paintings=Count('painting')
    )
    for church in churches:
        paintings_number = church.num_paintings
        if paintings_number > 0:
            churches_paintings.append((church, paintings_number))
    
    return render(request, 'museum/pages/search_church.html',{
            'churches': churches_paintings,
            'filterChurch': 'selected',
            'igrejas': '-selected',
            'search_action': 'painting:search',
            'placeholder': 'Pesquise as igrejas pelo nome, cidade ou estado',
        })


@require_GET
def detail_church(request: HttpRequest, id_church: int) -> HttpResponse:
    filter = request.GET.get('filter', '')
    current_page = int(request.GET.get('page', 1))
    paintings = Painting.objects.filter(church__id=id_church, is_published=True).order_by('-id')
    paintings = paintings.select_related('church', 'post_author')
    paintings = paintings.prefetch_related('engraving', 'author')

    
    if not paintings:
        raise Http404("there are no paintings related to this church id")
    church = paintings.first().church
    
    if filter == 'churches':
        search = request.GET.get('q', '')
        paintings = paintings.filter(Q(
            Q(name__icontains=search) | Q(summary__icontains=search)
        ))
    
    page = pagination(paintings, current_page)
    return render(request, 'museum/pages/church.html', {
        'page':page,
        'church': church,
        'filterChurch': 'selected',
        'placeholder': 'Pesquise pelas obras dessa igreja.',
        'limparPesquisa': True if filter == 'churches' else False,
        'search_result': search if filter == 'churches' else False,
        
    })

@require_GET
def painters(request: HttpRequest) -> HttpResponse:
    painter_paintings = []
    painters = Author.objects.filter(painting__is_published = True).distinct().order_by('-id')
    painters = painters.annotate(
        num_paintings = Count('painting')
    )
    for painter in painters:
        paintings_number = painter.num_paintings
        painter_paintings.append((painter, paintings_number))
    
    return render(request, 'museum/pages/search_painter.html',{
            'painters': painter_paintings,
            'filterPainter': 'selected',
            'pintores': '-selected',
            'search_action': 'painting:search',
            'placeholder': 'Pesquise os pintores pelo nome',
        })

@require_GET
def detail_painter(request: HttpRequest, id_painter: int)-> HttpResponse:
    filter = request.GET.get('filter', '')
    try:
        painter = Author.objects.get(pk=id_painter)
        paintings_this_painter = painter.painting_set.filter(is_published=True).order_by('-id')
        paintings_this_painter = paintings_this_painter.select_related('church', 'post_author').defer('church__city','church__state', 'description')
        paintings_this_painter = paintings_this_painter.prefetch_related('engraving', 'author').defer('engraving__book', 'author__biography')
        
    except ObjectDoesNotExist:
        raise Http404("Painter doesn't found in this database!")
    
    current_page = int(request.GET.get('page', 1))
    
    if filter == 'painters':
        search = request.GET.get('q', '')
        paintings_this_painter = paintings_this_painter.filter(Q(
            Q(name__icontains=search) | Q(summary__icontains=search)
        ))

    page = pagination(paintings_this_painter, current_page)
    return render(request, 'museum/pages/painter.html', {
        'painter': painter,
        'page': page,
        'filterPainter': 'selected',
        'placeholder': 'Pesquise pelas obras desse pintor.',
        'limparPesquisa': True if filter == 'painters' else False,
        'search_result': search if filter == 'painters' else False,

    })

@require_GET
def engravings(request: HttpRequest) -> HttpResponse:
    engraving_paintings = []
    engravings = Engraving.objects.filter(painting__is_published = True).distinct().order_by('-id')
    for engraving in engravings:
        paintings_number = engraving.painting_set.filter(is_published=True).count()
        engraving_paintings.append((engraving, paintings_number))
    
    return render(request, 'museum/pages/search_engraving.html',{
            'engravings': engraving_paintings,
            'filterEngraving': 'selected',
            'gravuras': '-selected',
            'search_action': 'painting:search',
            'placeholder': 'Pesquise a gravura pelo nome ou livro',
        })

@require_GET
def detail_engraving(request: HttpRequest, id_engraving:int) -> HttpResponse:
    try:
        engraving = Engraving.objects.get(pk=id_engraving)
        if not engraving.painting_set.filter(is_published=True).exists():
            raise Http404("Gravura não encontrada")
    except ObjectDoesNotExist:
        raise Http404("Gravura não encontrada")
    
    return render(request, 'museum/pages/detail_engraving.html', {
        'engraving': engraving,
        'search': False,
    })

@require_GET
def search(request: HttpRequest)-> HttpResponse:
    filter = request.GET.get("filter", "paintings")
    search = request.GET.get("q", "")
    current_page = int(request.GET.get('page', 1))
    
    if filter == 'paintings':
        template = 'museum/pages/search_painting.html'
        paintings = Painting.objects.filter(
            Q(
                Q(name__icontains=search) | Q(summary__icontains=search) 
            ) & Q(is_published=True)
        ).order_by('-id')
        paintings = paintings.select_related('church', 'post_author').prefetch_related('engraving', 'author')
        page = pagination(paintings, current_page)
        return render(request, template, {
            'page': page,
            'search_result': search,
            'is_search': True,
            'filter': filter,
            'obras': '-selected',
            'placeholder': 'Pesquise as obras pelo nome ou pelo resumo',
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
            'igrejas': '-selected',
            'placeholder': 'Pesquise as igrejas pelo nome, cidade ou estado',
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
            'pintores': '-selected',
            'placeholder': 'Pesquise os pintores pelo nome',
        })

@require_GET
def detail_painting_not_published(request: HttpRequest, painting_id: int) -> HttpResponse:
    try:
        painting = Painting.objects.select_related('church', 'post_author').prefetch_related('author', 'engraving__author').get(pk=painting_id, is_published=False)
        engravings = painting.engraving.all()
    except ObjectDoesNotExist:
        raise Http404('Objects not found in database')
    
    return render(request, 'museum/pages/detail_painting_edit.html', {
        'painting': painting,
        'engravings': engravings,
        'range': [i+1 for i in range(engravings.count())],
        'isDetailPage': True,
        'search':False,
        'edit': True,
        
    })

@require_GET
def info(request: HttpRequest) -> HttpResponse:
    return render(request, 'museum/pages/info.html', {
            'searchbar': False,
            'sobre': '-selected',
            })

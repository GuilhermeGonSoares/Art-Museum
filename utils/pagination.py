from django.core.paginator import Paginator


def pagination(lista, current_page: int):
    paginator = Paginator(lista, 6, orphans=1)
    page = paginator.get_page(current_page)
    pagination = paginator.get_elided_page_range(current_page, on_each_side = 2, on_ends = 1)
    number_page = paginator.num_pages
    
    return {
        'current_page': current_page,
        'paintings': page.object_list,
        'pagination': pagination if number_page > 1 else [],
        'number_page': number_page,
        'total_paintings': paginator.count,
    }

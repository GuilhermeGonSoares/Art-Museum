from unicodedata import name

from django.contrib import admin

from .models import Author, Church, Engraving, Painting


class PaintingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_published', 'post_date', 'post_author')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'summary')
    list_filter = ('is_published', 'church', 'author', 'post_author')
    list_per_page: int = 10
    list_editable = ('is_published',)
    ordering = '-id',
    autocomplete_fields = 'tag', 'author', 'engraving'


    
    #No futuro irá ter "slug"
    #prepopulated_fields ele popula esse campo com base no campo que queremos
    '''
    prepopulated_fields = {
        'slug': ('name',)
    }
    '''

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_engraving')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_per_page: int = 10
    ordering = '-id',
class ChurchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'state')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_per_page: int = 10
    ordering = '-id',
class EngravingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_per_page: int = 10
    ordering = '-id',
    autocomplete_fields = 'author',

admin.site.register(Painting, PaintingAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Church, ChurchAdmin)
admin.site.register(Engraving, EngravingAdmin)



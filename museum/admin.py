from django.contrib import admin

from .models import Author, Church, Engraving, Painting


class PaintingAdmin(admin.ModelAdmin):
    ...
class AuthorAdmin(admin.ModelAdmin):
    ...
class ChurchAdmin(admin.ModelAdmin):
    ...
class EngravingAdmin(admin.ModelAdmin):
    ...

admin.site.register(Painting, PaintingAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Church, ChurchAdmin)
admin.site.register(Engraving, EngravingAdmin)



from django.contrib import admin
from .models import Corpora, Genres


class CorporaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'keywords','genre', 'url')
    list_display_links = ('id', 'genre')
    search_fields = ['title', 'text', 'annotation', 'keywords',]
    list_filter = (('genre', admin.RelatedOnlyFieldListFilter),)
    list_per_page = 15
    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js',
        '/static/admin/js/doubleScroll.js',
        '/static/admin/js/call.js',)
admin.site.register(Corpora, CorporaAdmin)

class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'en', 'kz', 'rus')
    list_display_links = ('en', 'kz', 'rus',)
    search_fields = ('en', 'kz', 'rus',)
    list_per_page = 25
admin.site.register(Genres, GenresAdmin)
# Register your models here.

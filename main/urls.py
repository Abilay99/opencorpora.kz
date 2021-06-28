from django.urls import path
from django.conf.urls import url, include

from .views import index, handlerpost, download, ressumma, execute, execpost, about, privacy

urlpatterns = [
    url(r'^$', index, name='index'),
    url('handlerpost/', handlerpost, name='handlerpost'),
    url('download/', download, name='download'),
    url('ressumma/', ressumma, name='ressuma'),
    url('execpost/', execpost, name='execpost'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^exec/$', execute, name='exec'),
    url(r'^about/$', about, name='about'),
    url(r'^privacy/$', privacy, name='privacy'),
]
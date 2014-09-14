from django.conf.urls import url

from simpletemp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ac', views.ac, name='ac'),
    url(r'^heat', views.heat, name='heat')
]

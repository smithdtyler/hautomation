from django.conf.urls import url

from simpletemp import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]

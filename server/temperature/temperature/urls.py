from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# patterns are evaluated in order
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'temperature.views.home', name='home'),
    # url(r'^temperature/', include('temperature.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Until I get around to adding proper authentication    
    url(r'^accounts/login/', include(admin.site.urls)),

    url(r'^', include('simpletemp.urls')),
)

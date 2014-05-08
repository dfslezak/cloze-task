from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^trial/$', 'cloze.views.trial'),
    url(r'^trial/subir/$', 'cloze.views.subir'),
    url(r'^trial/subirInformation/$', 'cloze.views.subirInformation'),
    url(r'^bajar_todo/$', 'cloze.views.bajar_todo'),
    url(r'^ganadores/$', 'cloze.views.ganadores'),
    url(r'^FAQ/$', 'cloze.views.FAQ'),
    url(r'^bajar_sujetos/$', 'cloze.views.bajar_sujetos'),
    url(r'^$', 'cloze.views.home', name='home'),
    # url(r'^prueba/', include('prueba.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

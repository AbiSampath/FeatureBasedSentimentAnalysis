from django.conf.urls import patterns, url

from scoreTest import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #url(r'^mobilesentiment/',include('mysite.urls'))
)
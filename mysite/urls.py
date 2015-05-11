from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from scoreTest.views import render_sentiment,abinaya,overall_sentiment


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$','mysite.views.login'),
    url(r'^accounts/auth/$', 'mysite.views.auth_view'),
    
    url(r'^accounts/loggedin/$', 'mysite.views.loggedin2'),
    url(r'^accounts/invalid/$', 'mysite.views.invalid_login'),
    url(r'^accounts/register/$', 'mysite.views.register_user'),
    url(r'^accounts/register_success/$', 'mysite.views.register_success'),
    url(r'^accounts/product/$', 'mysite.views.product'),
    url(r'^accounts/about/$', 'mysite.views.about'),
    url(r'^accounts/architecture/$', 'mysite.views.architecture'),
    url(r'^accounts/index/$', 'mysite.views.index'),
    url(r'^accounts/loggedin/logout/$', 'mysite.views.log_me_out'),
     url(r'^accounts/home/$', 'mysite.views.home'),


        url(r'^accounts/loggedin/getSentiment/$', 'scoreTest.views.render_sentiment'),
    url(r'^accounts/loggedin/abi/$', 'scoreTest.views.cloud_render'),
    url(r'^accounts/loggedin/overall/$', 'scoreTest.views.overall_sentiment'),


)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()


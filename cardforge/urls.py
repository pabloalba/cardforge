from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from .designer import views as designer_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', designer_views.logout, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    # url(r'^login/success$', designer_views.login_success, name='login_success'),
    url(r'^login/success$', designer_views.login_success, name='login_success'),
    url(r'', designer_views.home, name='home'),

    url(r'^api/me/$', designer_views.MeDetail.as_view(), name='me'),
    url(r'^api/games/$', designer_views.GameList.as_view()),
    url(r'^api/games/(?P<pk>[0-9]+)$', designer_views.GameDetail.as_view()),
    url(r'^api/games/(?P<pk>[0-9]+)/owners/$', designer_views.GameOwners.as_view()),
]

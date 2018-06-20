from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

import designer.views as designer_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^login/success$', designer_views.login_success, name='login_success'),

    url(r'^api/games/$', designer_views.GameList.as_view()),
    url(r'^api/games/(?P<pk>[0-9]+)$', designer_views.GameDetail.as_view()),
]

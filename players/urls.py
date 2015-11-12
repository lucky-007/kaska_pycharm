from django.conf.urls import url
from players import views

urlpatterns = [
    url(r'^$', views.roster, name='roster'),
    url(r'(?P<player_id>[0-9]+)/$', views.player_info, name='info'),
    url(r'^change/$', views.player_change, name='change'),
    url(r'^create/$', views.player_create, name='create'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^change/password/$', views.password_change, name='password_change'),
    url(r'^password_reset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset_check_email/$', views.check_email, name='password_reset_check_email'),
    url(r'^password_reset_no_email/$', views.no_email, name='password_reset_no_email'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password_reset_complete/$', views.password_reset_complete, name='password_reset_complete'),
]

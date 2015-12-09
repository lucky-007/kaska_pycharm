from django.conf.urls import url
from players import views, views_admin

urlpatterns = [
    url(r'^$', views.teams, name='main'),
    url(r'^available/$', views.teams_available, name='available'),
    url(r'^success/$', views.teams_success, name='success'),
    url(r'^upload/$', views_admin.teams_upload),
    url(r'^flush/$', views_admin.teams_flush),
    url(r'^pools/$', views_admin.pools_update),
]

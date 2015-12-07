from django.conf.urls import url
from players import views

urlpatterns = [
    url(r'^$', views.teams, name='main'),
    url(r'^available/$', views.teams_available, name='available'),
    url(r'^success/$', views.teams_success, name='success'),
]

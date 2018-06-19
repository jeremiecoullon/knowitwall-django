from django.conf.urls import url

from . import views

app_name = 'content'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^all_episodes/$', views.AllEpisodesView.as_view(), name='all_episodes'),
    url(r'^episodes/(?P<slug>[\w\-]+)/$', views.EpisodePageView.as_view(), name='episode_page'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^terms/$', views.terms, name='terms'),
    url(r'^team/$', views.team, name='team')
]

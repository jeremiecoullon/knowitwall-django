from django.conf.urls import url

from . import views

app_name = 'content'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^episodes/(?P<slug>[\w\-]+)/$', views.episode_page, name='episode_page'),
    url(r'^about/$', views.about_page, name='about'),
    url(r'^terms/$', views.terms, name='terms'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^discipline/(?P<discipline>[\w ]+)/$', views.discipline_page, name='discipline_page'),
    url(r'^results/$', views.search, name='search'),

]

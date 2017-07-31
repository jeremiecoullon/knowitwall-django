from django.conf.urls import url


from . import views

app_name = 'notifications'
urlpatterns = [
    url(r'^le_feedback$', views.get_feedback , name='get_feedback'),
]

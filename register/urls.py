from django.conf.urls import url

from . import views

app_name = 'register'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^signin/$', views.signin, name='login'),
    url(r'^signout/$', views.signout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
]

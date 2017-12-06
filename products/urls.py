from django.conf.urls import url

from . import views

app_name = 'products'
urlpatterns = [
    url(r'^post/$', views.post, name='post'),
    # url(r'^order/$', views.order, name='order'),
]

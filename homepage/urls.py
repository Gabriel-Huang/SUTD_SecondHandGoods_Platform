from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^user/(?P<pk>\w+)$', views.user_view, name='user-view'),
    url(r'^search/', views.search, name='search'),
]
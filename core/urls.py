from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('register.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^homepage/', include('homepage.urls')),
]

urlpatterns += [
    url(r'^$', RedirectView.as_view(url='/homepage/', permanent=True), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

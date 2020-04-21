
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static


urlpatterns = [
    path('',include('pages.urls')),
    path('chat/',include('chat.urls')),
    path('account/',include('account.urls')),
    path('products/',include('products.urls')),
    path('admin/', admin.site.urls),
    
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
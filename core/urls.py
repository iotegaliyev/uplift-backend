from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .yasg import urlpatterns

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('startups.urls')),
    path('api/', include('articles.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

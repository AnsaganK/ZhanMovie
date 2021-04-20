from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),

]

urlpatterns += i18n_patterns(
    path('', include('movie.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

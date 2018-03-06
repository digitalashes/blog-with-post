from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from config.api_docs import docs

api_urlpatterns = [
    path('', include('users.urls')),
]

urlpatterns = [
    path('', RedirectView.as_view(url='/api/docs/'), name='index'),
    path(settings.ADMIN_URL, admin.site.urls),

    path('api/docs/', docs),
    path('api/', include(arg=(api_urlpatterns, 'config'), namespace='api')),
]

if settings.USE_SILK:
    urlpatterns += [
        path('silk/', 'silk.urls')
    ]

if settings.USE_DEBUG_TOOLBAR:
    urlpatterns += [
        path('__debug__/', 'debug_toolbar.urls'),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

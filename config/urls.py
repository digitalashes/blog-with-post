from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

from config.api_docs import docs

api_urlpatterns = [
    url(r'^', include('users.urls')),
    url(r'^', include('posts.urls')),
    url(r'^', include('comments.urls')),
]

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/api/docs/'), name='index'),
    url(settings.ADMIN_URL, admin.site.urls),

    url(r'api/docs/', docs),
    url(r'api/', include(arg=(api_urlpatterns, 'config'), namespace='api')),
]

if settings.USE_SILK:
    urlpatterns += [
        url(r'^silk/', 'silk.urls'),
    ]

if settings.USE_DEBUG_TOOLBAR:
    urlpatterns += [
        url(r'^__debug__/', 'debug_toolbar.urls'),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

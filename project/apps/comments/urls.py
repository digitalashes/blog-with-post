from django.conf.urls import include, url

from comments import views

urlpatterns = [
    url(r'^comments/', include([
        url(r'^create/$', views.comment_create, name='create'),
        url(r'^update/(?P<pk>\d+)/$', views.comment_update, name='update'),
        url(r'^delete/(?P<pk>\d+)/$', views.comment_delete, name='delete'),
    ], namespace='comments')),
]

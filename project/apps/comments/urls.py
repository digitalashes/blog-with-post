from django.conf.urls import include, url

from comments import views

urlpatterns = [
    url(r'comments/', include([
        url('create/$', views.comment_create, name='create'),
        url('update/(?P<pk>\d+)/$', views.comment_update, name='update'),
        url('delete/(?P<pk>\d+)/$', views.comment_delete, name='delete'),
    ], namespace='comments')),
]

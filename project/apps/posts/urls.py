from django.conf.urls import include, url

from posts import views

urlpatterns = [
    url(r'^posts/', include([
        url(r'^list/$', views.post_list, name='list'),
        url(r'^my_post_list/$', views.my_post_list, name='my_post_list'),
        url(r'^create/$', views.post_create, name='create'),
        url(r'^detail/(?P<pk>\d+)/$', views.post_detail, name='detail'),
        url(r'^update/(?P<pk>\d+)/$', views.post_update, name='update'),
        url(r'^delete/(?P<pk>\d+)/$', views.post_delete, name='delete'),

    ], namespace='posts')),
]

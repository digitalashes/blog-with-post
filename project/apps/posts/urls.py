from django.urls import path, include

from posts import views

urlpatterns = [
    path('posts/', include((
        [
            path('list/', views.post_list, name='list'),

        ], 'posts'), namespace='posts')),
]

from django.urls import path, include

from posts import views

urlpatterns = [
    path('posts/', include((
        [
            path('list/', views.post_list, name='list'),
            path('my_post_list/', views.my_post_list, name='my_post_list'),
            path('create/', views.post_create, name='create'),
            path('detail/<int:pk>/', views.post_detail, name='detail'),
            path('update/<int:pk>/', views.post_update, name='update'),
            path('delete/<int:pk>/', views.post_delete, name='delete'),

        ], 'posts'), namespace='posts')),
]

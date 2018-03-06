from django.urls import path, include

from comments import views

urlpatterns = [
    path('comments/', include((
        [
            path('create/', views.comment_create, name='create'),
            path('update/<int:pk>/', views.comment_update, name='update'),
            path('delete/<int:pk>/', views.comment_delete, name='delete'),
        ], 'comments'), namespace='comments')),
]

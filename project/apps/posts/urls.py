from django.urls import path, include

from posts import views

urlpatterns = [
    path('posts/', include((
        [

        ], 'posts'), namespace='posts')),
]

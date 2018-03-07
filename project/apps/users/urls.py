from django.urls import path, include
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

from users import views

urlpatterns = [
    path('auth/', include((
        [
            path('registration/', views.registration, name='registration', ),

            path('verify_email_resend/', views.verify_email_resend, name='verify_email_resend', ),
            path('verify_email_confirm/', views.verify_email_confirm, name='verify_email_confirm', ),

            path('login/', views.login, name='login', ),
            path('logout/', views.logout, name='logout'),

            path('token_refresh/', refresh_jwt_token, name='token_refresh'),
            path('token_verify/', verify_jwt_token, name='token_verify'),

            path('password_change/', views.password_change, name='password_change'),
            path('password_reset/', views.password_reset, name='password_reset'),
            path('password_reset_confirm/', views.password_reset_confirm, name='password_reset_confirm'),

        ], 'users'), namespace='auth')),
    path('users/', include((
        [
            path('user_list/', views.user_list, name='user_list'),
            path('user_info/<int:pk>/', views.user_info, name='user_info'),
            path('user_update/', views.user_update, name='user_update'),

            path('user_posts/<int:pk>/', views.user_posts, name='user_posts'),
            path('user_comments/<int:pk>/', views.user_comments, name='user_comments'),

        ], 'users'), namespace='users')),
]

from django.urls import path, include

from users import views

urlpatterns = [
    path('auth/', include((
        [
            path(
                'registration/',
                views.registration,
                name='registration'
            ),
            path(
                'verify_email_resend/',
                views.verify_email_resend,
                name='verify_email_resend'
            ),
            path(
                'verify_email_confirm/',
                views.verify_email_confirm,
                name='verify_email_confirm'
            ),

            # path('login/', obtain_jwt_token, name='login'),
            # path('logout/', views.logout, name='logout'),
            #
            # path('token_refresh/', refresh_jwt_token, name='token_refresh'),
            # path('token_verify/', verify_jwt_token, name='token_verify'),
            #
            # path('password_change/', views.password_change, name='password_change'),

        ], 'users'), namespace='auth')),
    path('users/', include((
        [

        ], 'users'), namespace='users')),
]

from django.conf.urls import include, url
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

from users import views

urlpatterns = [
    url(r'auth/', include([
        url(r'^registration/$', views.registration, name='registration', ),

        url(r'^verify_email_resend/$', views.verify_email_resend, name='verify_email_resend', ),
        url(r'^verify_email_confirm/$', views.verify_email_confirm, name='verify_email_confirm', ),

        url(r'^login/$', views.login, name='login', ),
        url(r'^logout/$', views.logout, name='logout'),

        url(r'^token_refresh/$', refresh_jwt_token, name='token_refresh'),
        url(r'^token_verify/$', verify_jwt_token, name='token_verify'),

        url(r'^password_change/$', views.password_change, name='password_change'),
        url(r'^password_reset/$', views.password_reset, name='password_reset'),
        url(r'^password_reset_confirm/$', views.password_reset_confirm, name='password_reset_confirm'),

    ], namespace='auth')),
    url('users/', include([
        url(r'^user_list/$', views.user_list, name='user_list'),
        url(r'^user_info/(?P<pk>\d+)/$', views.user_info, name='user_info'),
        url(r'^user_update/$', views.user_update, name='user_update'),

        url(r'^user_posts/(?P<pk>\d+)/$', views.user_posts, name='user_posts'),
        url(r'^user_comments/(?P<pk>\d+)/$', views.user_comments, name='user_comments'),

    ], namespace='users')),
]

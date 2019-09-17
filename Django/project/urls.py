from project import views
from django.conf.urls import url, include
from django.urls import path

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^student/$', views.student, name='student'),
#    url(r'^professor/$', views.professor, name='professor'),
    path('permission/<userid>/', views.permission, name='permission'),
    path('managehw/<hwname>/', views.managehw, name='managehw'),
    url(r'^permission/$', views.permission, name='permission'),
    url(r'^signup/$', views.signup_form, name='signup'),
    url(r'^success_login/$', views.success_login, name='success_login'),
    url(r'^createhw/$', views.createhw, name='createhw'),
    url(r'^webhook/$', views.webhook, name='webhook'),
#    url(r'^studentlist/$', views.UsersView.as_view(), name='studentlist'),
#   url(r'^api/push/$', views.git_alert, name='push'),
    url(r'^api/result/(?P<repository_name>[^/]+)/$', views.run_code, name='test'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^auth/', include('social_django.urls', namespace='social')),
]


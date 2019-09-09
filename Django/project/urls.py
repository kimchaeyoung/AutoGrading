from project import views
from django.conf.urls import url, include

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^student/$', views.student, name='student'),
    url(r'^professor/$', views.professor, name='professor'),
    url(r'^signup/$', views.signup_form, name='signup'),
    url(r'^success_login/$', views.success_login, name='success_login'),
    url(r'^createhw/$', views.createhw, name='createhw'),
    url(r'^webhook/$', views.webhook, name='webhook'),
    url(r'^myhw/$', views.myhw, name='myhw'),
    url(r'^studentlist/$', views.UsersView.as_view(), name='studentlist'),
#   url(r'^api/push/$', views.git_alert, name='push'),
#    url(r'^api/result/$', views.test_code),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^auth/', include('social_django.urls', namespace='social')),
]


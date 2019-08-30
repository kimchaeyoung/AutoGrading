from project import views
from django.conf.urls import url, include


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^student$', views.student, name='student'),
    url(r'^professor$', views.professor, name='professor'),
    url(r'^studentlist$', views.UsersView.as_view(), name='studentlist'),
    url(r'^class$', views.classroom, name='class'),
    url(r'^api/push/$', views.git_alert, name='push'),
    url(r'^api/result/$', views.test_code),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^auth/', include('social_django.urls', namespace='social')),
]


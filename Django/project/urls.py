from project import views
from django.conf.urls import url

urlpatterns = [
    url(r'^api/push/$', views.git_alert, name='push'),
    url(r'^api/result/$', views.test_code),
]

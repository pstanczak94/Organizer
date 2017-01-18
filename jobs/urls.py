from django.conf.urls import url

from jobs import views

app_name = "jobs"

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^add/$', views.add, name='add'),
	url(r'^add/submit/$', views.addsubmit, name='addsubmit'),
	url(r'^show/(?P<job_id>[0-9]+)/$', views.show, name='show'),
    url(r'^remove/(?P<job_id>[0-9]+)/$', views.remove, name='remove')
]
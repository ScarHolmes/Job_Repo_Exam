from django.conf.urls import url
from . import views  
from django.conf.urls.static import static         # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^sucess$', views.success),
    url(r'logout$', views.logout),
    url(r'addjob$', views.addjob),
    url(r'process$', views.process),
    url(r'^view/(?P<id>\d+)$', views.viewjob, name='show_job'),
    url(r'delete$', views.delete),
    url(r'^edit/(?P<id>\d+)$', views.edit, name='my_edit'),
     url(r'edit_u$', views.editprocess),
    # url(r'^show$', views.show)   # This line has changed! Notice that urlpatterns is a list, the comma is in
]   
from django.conf.urls import patterns, url
from student.views import IndexView

urlpatterns = patterns('',
    url(r'^/', IndexView.as_view, name='home')
   )
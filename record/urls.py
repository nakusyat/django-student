from django.conf.urls import patterns, url
from record.views import IndexView, GroupAddView, GroupsAllView, GroupDeleteView, StudentsAllView, StudentDeleteView, \
    StudentEditView
from record.views import GroupView
from record.views import GroupEditView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'students$', StudentsAllView.as_view(), name='students'),
    url(r'student/delete$', StudentDeleteView.as_view(), name='student_delete'),
    url(r'student/edit$', StudentEditView.as_view(), name='student_edit'),
    url(r'group/add$', GroupAddView.as_view(), name='group_add'),
    url(r'group/edit$', GroupEditView.as_view(), name='group_edit'),
    url(r'group/delete$', GroupDeleteView.as_view(), name='group_delete'),
    url(r'group/(?P<group_id>\d+)/$', GroupView.as_view(), name='group'),
    url(r'groups$', GroupsAllView.as_view(), name='groups'),
   )
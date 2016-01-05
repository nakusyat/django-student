# coding=utf-8
from datetime import datetime
from django.core import serializers
import json
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from record.forms import GroupForm
from record.submodels.group import Group
from record.submodels.student import Student


class IndexView(View):
    temp_dir = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        data = Student.objects.values('group__id', 'group__name', 'group__starosta__name__first_name', 'group__starosta__name__last_name').annotate(total=Count('id'))
        return render(request, self.temp_dir, {'groups': data})


class GroupsAllView(View):
    temp_dir = 'group/list.html'

    def dispatch(self, request, *args, **kwargs):
        groups = Group.objects.all()
        return render(request, self.temp_dir, {'groups': groups})


class GroupDeleteView(View):
    def dispatch(self, request, *args, **kwargs):
        response_data = {}

        try:
            Group.objects.get(id__exact=request.POST.get('group_id')).delete()
        except ObjectDoesNotExist:
            response_data['error'] = 'The group doesnt exist'
        else:
            response_data['success'] = 'The group was successfully deleted'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


class StudentDeleteView(View):
    def dispatch(self, request, *args, **kwargs):
        response_data = {}

        try:
            Student.objects.get(id__exact=request.POST.get('stud_id')).delete()
        except ObjectDoesNotExist:
            response_data['error'] = 'The student doesnt exist'
        else:
            response_data['success'] = 'The student was successfully deleted'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


class GroupView(View):
    temp_dir = 'group/index.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            group = Group.objects.get(id__exact=kwargs['group_id'])
        except ObjectDoesNotExist:
            group = None

        if group:
            students = Student.objects.filter(group=kwargs['group_id'])
        else:
            students = {}
            messages.error(request, 'The group with id= ' + kwargs['group_id'] + ' doesnt exist')

        return render(request, self.temp_dir, {'group':group, 'students': students})


class GroupEditView(View):

    def dispatch(self, request, *args, **kwargs):
        response_data = {}
        try:
            group = Group.objects.get(id__exact=request.POST.get('group_id'))
        except ObjectDoesNotExist:
            response_data['error'] = 'The group with id= ' + request.POST.get('group_id') + ' doesnt exist'
        else:
            group.name = request.POST.get('group_name')
            group.save()
            response_data['success'] = 'Запись успешно изменена'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


class StudentEditView(View):

    def dispatch(self, request, *args, **kwargs):
        response_data = {}
        try:
            student = Student.objects.get(id__exact=request.POST.get('stud_id'))
        except ObjectDoesNotExist:
            response_data['error'] = 'The group with id= ' + request.POST.get('stud_id') + ' doesnt exist'
        else:
            student.first_name = request.POST.get('stud_name')
            student.last_name = request.POST.get('stud_surname')
            student.birth_date = datetime.strptime(request.POST.get('stud_birth'), "%Y-%m-%d")
            student.stud_no = request.POST.get('stud_no')
            student.save()
            response_data['success'] = 'Запись успешно изменена'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


class GroupAddView(View):
    temp_dir = 'group/form.html'

    def dispatch(self, request, *args, **kwargs):
        render_data = {}
        render_data['action'] = reverse('record:group_add')
        render_data['button'] = 'Добавить'
        render_data['form'] = GroupForm()
        if request.method == 'POST':
            render_data['form'] = GroupForm(request.POST)
            if render_data['form'].is_valid():
                if render_data['form'].save():
                    messages.success(request, "Запись успешно добавлена")
        return render(request, self.temp_dir, render_data)


class StudentsAllView(View):
    def dispatch(self, request, *args, **kwargs):
        if self.request.is_ajax():
            students = Student.objects.filter(group_id__exact=request.POST.get('group_id'))
            data = serializers.serialize('json', students)
            return HttpResponse(
                data,
                content_type="application/json"
            )
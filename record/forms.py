# coding=utf-8
from django.forms import ModelForm
from django import forms
from record.submodels.group import Group


class GroupForm(ModelForm):
    name = forms.CharField(label="Наименование", error_messages={'required': 'Заполните поле'})

    class Meta:
        model = Group
        fields = '__all__'

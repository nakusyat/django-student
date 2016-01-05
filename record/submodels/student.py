# coding=utf-8
from django.db import models
from group import Group


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(editable=True)
    stud_no = models.CharField(max_length=20)
    group = models.ForeignKey(Group, blank=True, verbose_name='Группа')

    def __str__(self):
        return self.first_name + " " + self.last_name
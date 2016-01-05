# coding=utf-8
from django.db import models
from student import Student
from group import Group


class Starosta(models.Model):
    name = models.ForeignKey(Student, verbose_name='Староста', blank=True)
    group = models.ForeignKey(Group, verbose_name='Группа', blank=True)

    def __str__(self):
        return self.name__first_name + self.name__last_name
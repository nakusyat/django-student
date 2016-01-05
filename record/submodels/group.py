# coding=utf-8
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=120)

    def __unicode__(self):
        return self.name

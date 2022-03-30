from django.db import models
from taggit.managers import TaggableManager

from AthenaTools import settings


class Project(models.Model):
    project_code = models.CharField(unique=True, max_length=30)
    project_name = models.CharField(max_length=50)
    geo_area = models.CharField(max_length=50, verbose_name="Geographical area", null=True, blank=True)
    project_desc = models.CharField(max_length=50, verbose_name="Project description", null=True, blank=True)
    project_admin = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='project_admin')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='project_users',
                                   blank=True)

    def __str__(self):
        return self.project_name

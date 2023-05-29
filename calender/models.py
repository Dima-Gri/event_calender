from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    project_name = models.CharField(max_length=150, null=True)
    manager = models.CharField(max_length=150, null=True)
    status = models.CharField(max_length=50, default='To Do')

    @property
    def get_html_url(self):
        url = reverse('calender:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

    @property
    def get_url(self):
        url = reverse('calender:event_edit_to_dashboard', args=(self.id,))
        return url

    @property
    def get_url_default(self):
        url = reverse('calender:event_edit_to_dashboard_default', args=(self.id,))
        return url

    @property
    def get_delete_url(self):
        url = reverse('calender:event_delete', args=(self.id,))
        return url

    @property
    def get_delete_url_dsh(self):
        url = reverse('calender:event_delete_to_dashboard', args=(self.id,))
        return url

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    group = models.CharField(max_length=255)


class Projects(models.Model):
    project_name = models.CharField(max_length=150)
    manager = models.CharField(max_length=150)
    worker = models.CharField(max_length=150, null=True)
    def __str__(self):
        return f'{self.project_name}({self.manager})'

    @property
    def get_url(self):
        url = reverse('calender:proj_dashboard', args=(self.id,))
        return url


class Project(models.Model):
    project_name = models.CharField(max_length=150)
    manager = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.project_name}({self.manager})'

    @property
    def get_url(self):
        url = reverse('calender:proj_dashboard', args=(self.id,))
        return url

    @property
    def get_url_add(self):
        url = reverse('calender:add_worker', args=(self.project_name,))
        return url
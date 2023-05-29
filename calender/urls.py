from . import views
from django.urls import path, include

from .views import *

app_name = 'calender'
urlpatterns = [
    # path(r'index/', views.index, name='index'),
    path(r'', views.CalendarView.as_view(), name='calendar'),
    path(r'register/', RegisterUser.as_view(), name='register'),
    path(r'login/', LoginUser.as_view(), name='login'),
    path(r'logout/', logout_user, name='logout'),
    path(r'event/new/', views.event, name='event_new'),
    path(r'event/edit_dsh/(?P<event_id>\d+)/', views.event_dashboards, name='event_edit_to_dashboard'),
    path(r'event/edit_dsh_default/(?P<event_id>\d+)/', views.event_dashboard_default, name='event_edit_to_dashboard_default'),
    path(r'event/edit/(?P<event_id>\d+)/', views.event, name='event_edit'),
    path(r'event/kdelete/(?P<event_id>\d+)/', views.delete_dashboard, name='event_delete_to_dashboard'),
    path(r'event/delete/(?P<event_id>\d+)/', views.delete, name='event_delete'),
    path(r'dashboard', views.dashboard, name='dashboard'),
    path(r'proj_dashboard/(?P<project_id>\d+)/', views.proj_dashboard, name='proj_dashboard'),
    path(r'back', views.back, name='back'),
    path(r'projects', views.get_projects, name='projects'),
    path(r'add/(?P<projects_name>\d+)/', views.add_worker, name='add_worker'),
    path(r'adding', views.add_worker_without_name, name='add_worker_without_name'),
]

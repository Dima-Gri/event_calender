import calendar
from datetime import datetime, date, timedelta
from django.contrib.auth import authenticate, login
from datetime import datetime
import pytz


import django.db.models
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.core.checks import messages
from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils.safestring import mark_safe
from django.views.generic import CreateView
from psycopg.types.datetime import utc

from .forms import EventForm, RegisterUserForm, LoginUserForm, EventForm_NE, AddForm, AddForm1
from .models import *
from .utils import Calendar


def get_dicts(request):
    projects = Projects.objects.filter(worker=request.user.username)
    todo = Event.objects.filter(manager=request.user.username, status='To Do')
    prog = Event.objects.filter(manager=request.user.username, status='In progress')
    review = Event.objects.filter(manager=request.user.username, status='Review')
    done = Event.objects.filter(manager=request.user.username, status='Done')
    for project in projects:
        if project.project_name == 'personal':
            continue
        todo |= Event.objects.filter(project_name=project.project_name, status='To Do')
        prog |= Event.objects.filter(project_name=project.project_name, status='In progress')
        review |= Event.objects.filter(project_name=project.project_name, status='Review')
        done |= Event.objects.filter(project_name=project.project_name, status='Done')
    return {'todo': todo, 'prog': prog, 'review': review, 'done': done}


class CalendarView(generic.ListView):
    model = Event
    template_name = 'calender/calender.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        # d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True, username=self.request.user.username)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        my_projects = Project.objects.filter(manager=self.request.user.username)
        context['flag'] = bool(len(my_projects) - 1)
        my_projects2 = Projects.objects.filter(worker=self.request.user.username)
        res = [proj.project_name for proj in my_projects2]
        my_projects2 = Project.objects.filter(project_name__in=res)
        context['projects'] = [proj for proj in my_projects if proj.project_name != 'personal'] + [proj for proj in
                                                                                                   my_projects2 if
                                                                                                   proj.project_name != 'personal']
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def add_worker(request, projects_name):
    instance, form = None, None
    instance = Projects()
    instance.manager = request.user.username
    instance.project_name = projects_name
    form = AddForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calender:calendar'))

    return render(request, 'calender/add.html', {'form': form})


def add_worker_without_name(request):
    instance, form = None, None

    instance = Projects()
    instance.manager = request.user.username
    form = AddForm1(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.fields['project_name'].choices = list(
            map(lambda a: (a[0], a[0]),
                Project.objects.filter(manager=request.user.username).values_list('project_name')))
        form.save()
        return HttpResponseRedirect(reverse('calender:calendar'))
    form.fields['project_name'].choices = [item
                                           for item in map(lambda a: (a[0], a[0]),
                                                           Project.objects.filter(
                                                               manager=request.user.username).values_list(
                                                               'project_name')) if item[0] != 'personal']

    return render(request, 'calender/add.html', {'form': form})

def event(request, event_id=None):  #
    instance = None
    form, status = None, None
    if event_id:
        print('HER1')
        instance = get_object_or_404(Event, pk=event_id)
        if request.user.username == instance.manager:
            print('HER2')
            form = EventForm(request.POST or None, instance=instance)
            status = 1
        else:
            print('HER3')
            form = EventForm_NE(request.POST or None, instance=instance)
            status = 0
    else:
        print('HER4')
        instance = Event()
        instance.manager = request.user.username
        form = EventForm(request.POST or None, instance=instance)
        status = 1

    if request.POST and form.is_valid():
        print(request.user.username)
        if status:
            form.fields['project_name'].choices = list(
                map(lambda a: (a[0], a[0]),
                    Project.objects.filter(manager=request.user.username).values_list('project_name')))
        form.save()
        return HttpResponseRedirect(reverse('calender:calendar'))
    if status:
        ls = list(
            map(lambda a: (a[0], a[0]),
                Project.objects.filter(manager=request.user.username).values_list('project_name')))
        form.fields['project_name'].choices = ls
        print(ls)
    return render(request, 'calender/event.html',
                  {'form': form, 'flag': False, 'status': bool(event_id), 'instance': instance, 'project': None})


def event_dashboards(request, event_id=None):  # из дашбордов
    instance = Event()
    form = None
    status = None
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
        if request.user.username == instance.manager:
            form = EventForm(request.POST or None, instance=instance)
            status = 1
        else:
            form = EventForm_NE(request.POST or None, instance=instance)
            status = 0
    else:
        instance = Event()
        instance.manager = request.user.username
        form = EventForm(request.POST or None, instance=instance)
        status = 1

    if request.POST and form.is_valid():
        print(request.user.username)
        if status:
            form.fields['project_name'].choices = list(
                map(lambda a: (a[0], a[0]),
                    Project.objects.filter(manager=request.user.username).values_list('project_name')))
        form.save()
        project = get_object_or_404(Project, project_name=instance.project_name, manager=instance.manager)
        return proj_dashboard(request, project.id)
    if status:
        form.fields['project_name'].choices = list(
            map(lambda a: (a[0], a[0]),
                Project.objects.filter(manager=request.user.username).values_list('project_name')))

    project = get_object_or_404(Project, project_name=instance.project_name, manager=instance.manager)
    return render(request, 'calender/event.html',
                  {'form': form, 'flag': True, 'status': bool(event_id), 'instance': instance, 'project': project})


def event_dashboard_default(request, event_id=None):  # з дефолтного
    instance = Event()
    form = None
    status = None
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
        if request.user.username == instance.manager:
            form = EventForm(request.POST or None, instance=instance)
            status = 1
        else:
            form = EventForm_NE(request.POST or None, instance=instance)
            status = 0
    else:
        instance = Event()
        instance.manager = request.user.username
        form = EventForm(request.POST or None, instance=instance)
        status = 1

    if request.POST and form.is_valid():
        if status:
            form.fields['project_name'].choices = list(
                map(lambda a: (a[0], a[0]),
                    Project.objects.filter(manager=request.user.username).values_list('project_name')))
        form.save()
        return HttpResponseRedirect(reverse('calender:dashboard'))
    if status:
        form.fields['project_name'].choices = list(
            map(lambda a: (a[0], a[0]),
                Project.objects.filter(manager=request.user.username).values_list('project_name')))
    return render(request, 'calender/event.html',
                  {'form': form, 'flag': True, 'status': bool(event_id), 'instance': instance, 'project': None})


def delete(request, event_id=None):
    instance = get_object_or_404(Event, pk=event_id)
    instance.delete()
    return HttpResponseRedirect(reverse('calender:calendar'))


def delete_dashboard(request, event_id=None):
    instance = get_object_or_404(Event, pk=event_id)
    instance.delete()
    dicts = get_dicts(request)
    dicts['flag'] = False
    dicts['cur'] = datetime.now().replace(tzinfo=pytz.utc)
    return render(request, 'calender/dashboard.html', dicts)


def get_projects(request):
    print(request.user.username)
    my_projects = Projects.objects.filter(manager=request.user.username)

    print(my_projects)
    return render(request, 'calender/projects.html', {'my_projects': my_projects})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'calender/register.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            project = Projects(project_name='personal', manager=user, worker=user)
            project.save()
            project = Project(project_name='personal', manager=user)
            project.save()

            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('calender:calendar')
        else:
            return render(request, self.template_name, {'form': form})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'calender/login.html'

    def get_success_url(self):
        user_name = self.request.POST['username']
        user_group = CustomUser.objects.filter(username=user_name)
        print(user_group[0].group)
        if user_group[0].group == 'Менеджер':
            return reverse_lazy('calender:calendar')  # view for manager
        else:
            return reverse_lazy('calender:calendar')


def logout_user(request):
    logout(request)
    return redirect('calender:login')


def dashboard(request):
    dicts = get_dicts(request)
    dicts['flag'] = False
    dicts['cur'] = datetime.now().replace(tzinfo=pytz.utc)
    return render(request, 'calender/dashboard.html', dicts)


def get_dict(request, project_name):
    todo = Event.objects.filter(project_name=project_name, status='To Do')
    prog = Event.objects.filter(project_name=project_name, status='In progress')
    review = Event.objects.filter(project_name=project_name, status='Review')
    done = Event.objects.filter(project_name=project_name, status='Done')
    return {'todo': todo, 'prog': prog, 'review': review, 'done': done}


def proj_dashboard(request, project_id):
    instance = get_object_or_404(Project, pk=project_id)
    print(instance)
    dicts = get_dict(request, instance.project_name)
    dicts['flag'] = True
    dicts['cur'] = datetime.now().replace(tzinfo=pytz.utc)
    return render(request, 'calender/dashboard.html', dicts)


def back(request):
    return redirect(request.META.get('HTTP_REFERER'))

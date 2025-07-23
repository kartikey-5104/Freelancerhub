from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Application
from .forms import ProjectForm, ApplicationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required
def dashboard(request):
    user = request.user
    profile = user.profile
    if profile.role == 'freelancer':
        applications = Application.objects.filter(freelancer=user)
        return render(request, 'core/dashboard.html', {'applications': applications})
    else:
        projects = Project.objects.filter(client=user)
        return render(request, 'core/dashboard.html', {'projects': projects})

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, client=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'core/edit_project.html', {'form': form})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, client=request.user)
    project.delete()
    return redirect('dashboard')

@login_required
def apply_to_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.project = project
            app.freelancer = request.user
            app.save()
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'core/apply_to_project.html', {'form': form, 'project': project})

@login_required
def add_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.freelancer = request.user
            app.save()
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'core/add_application.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # or another success URL
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
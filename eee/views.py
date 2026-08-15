from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import (
    WorkApplicationForm,
    ProjectForm,
    TaskForm,
)

from .models import (
    WorkApplication,
    Project,
    Task,
    TaskApplication,
)

User = get_user_model()


# =========================================================
# ROLE CHECK
# =========================================================

def is_manager(user):
    return user.groups.filter(name="Manager").exists()


# =========================================================
# USER DASHBOARD
# =========================================================

# =========================================================
# USER DASHBOARD
# PUBLIC
# =========================================================

def Userdashboard(request):

    # -----------------------------------------------------
    # Public data
    # -----------------------------------------------------

    projects = Project.objects.all().order_by("-created_at")

    tasks = Task.objects.filter(
        status="Available"
    ).select_related(
        "project"
    )

    # -----------------------------------------------------
    # Default empty data
    # -----------------------------------------------------

    active_tasks = []
    completed_tasks = []
    pending_tasks = []
    user_projects = []

    # -----------------------------------------------------
    # If user is logged in
    # -----------------------------------------------------

    if request.user.is_authenticated:

        active_tasks = TaskApplication.objects.filter(
            user=request.user,
            status="Accepted",
            task__status="Assigned"
        ).select_related(
            "task",
            "task__project"
        )

        completed_tasks = TaskApplication.objects.filter(
            user=request.user,
            status="Accepted",
            task__status="Completed"
        ).select_related(
            "task",
            "task__project"
        )

        pending_tasks = TaskApplication.objects.filter(
            user=request.user,
            status="Pending"
        ).select_related(
            "task",
            "task__project"
        )

        user_projects = Project.objects.filter(
            tasks__applications__user=request.user
        ).distinct()

    # -----------------------------------------------------
    # Render dashboard
    # -----------------------------------------------------

    return render(
        request,
        "Userdashborad.html",
        {
            "projects": projects,
            "tasks": tasks,

            "active_tasks": active_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,

            "user_projects": user_projects,

            "is_logged_in": request.user.is_authenticated,
        }
    )


# =========================================================
# MANAGER DASHBOARD
# =========================================================

@login_required
def Managerdashboard(request):

    if not is_manager(request.user):

        messages.error(
            request,
            "Only Manager can access Manager Dashboard."
        )

        return redirect("home")

    return render(
        request,
        "managerdashboard.html"
    )


# =========================================================
# APPLY FOR WORK
# =========================================================

@login_required
def apply_work(request):

    if request.method == "POST":

        form = WorkApplicationForm(request.POST)

        if form.is_valid():

            application = form.save(commit=False)

            application.user = request.user

            application.save()

            messages.success(
                request,
                "Your work application has been submitted successfully."
            )

            return redirect("userdashboard")

    else:

        form = WorkApplicationForm()

    return render(
        request,
        "apply_work.html",
        {
            "form": form
        }
    )


# =========================================================
# PROJECT LIST
# =========================================================

@login_required
def projects(request):

    project_list = Project.objects.all().order_by("-created_at")

    return render(
        request,
        "projects.html",
        {
            "projects": project_list
        }
    )


# =========================================================
# ACTIVITY
# =========================================================

@login_required
def activity(request):

    return render(
        request,
        "activity.html"
    )


# =========================================================
# PROFILE
# =========================================================

@login_required
def profile(request):

    return render(
        request,
        "profile.html"
    )


# =========================================================
# CREATE PROJECT
# ONLY SUPERUSER
# =========================================================

@login_required
def createproject(request):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Only Superuser can create projects."
        )

        return redirect("home")

    if request.method == "POST":

        form = ProjectForm(request.POST)

        if form.is_valid():

            project = form.save(commit=False)

            project.created_by = request.user

            project.save()

            messages.success(
                request,
                "Project created successfully."
            )

            return redirect("projects")

    else:

        form = ProjectForm()

    return render(
        request,
        "createproject.html",
        {
            "form": form
        }
    )


# =========================================================
# CREATE TASK
# ONLY MANAGER
# =========================================================

@login_required
def create_task(request):

    if not is_manager(request.user):

        messages.error(
            request,
            "Only Manager can create tasks."
        )

        return redirect("home")

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save()

            messages.success(
                request,
                "Task created successfully."
            )

            return redirect("my_tasks")

    else:

        form = TaskForm()

    return render(
        request,
        "create_task.html",
        {
            "form": form
        }
    )


# =========================================================
# MY TASKS
# ONLY NORMAL USERS
# =========================================================

@login_required
def my_tasks(request):

    # Manager and Superuser cannot apply for worker tasks

    if request.user.is_superuser or is_manager(request.user):

        messages.error(
            request,
            "This page is only for workers."
        )

        return redirect("home")

    # -----------------------------------------------------
    # Accepted work applications
    # -----------------------------------------------------

    work_applications = WorkApplication.objects.filter(
        user=request.user,
        status="Accepted"
    )

    # -----------------------------------------------------
    # Work types
    # -----------------------------------------------------

    work_types = work_applications.values_list(
        "work_type",
        flat=True
    )

    # -----------------------------------------------------
    # Available tasks
    # -----------------------------------------------------

    tasks = Task.objects.filter(
        status="Available",
        project__status__in=[
            "Pending",
            "Running"
        ]
    ).select_related(
        "project"
    )

    # -----------------------------------------------------
    # Match task with work type
    # -----------------------------------------------------

    matching_tasks = []

    for task in tasks:

        task_title = task.title.lower().strip()

        for work_type in work_types:

            if not work_type:
                continue

            work_type = work_type.lower().strip()

            if work_type in task_title:

                matching_tasks.append(task)

                break

    # -----------------------------------------------------
    # Already applied tasks
    # -----------------------------------------------------

    applied_task_ids = set(
        TaskApplication.objects.filter(
            user=request.user
        ).values_list(
            "task_id",
            flat=True
        )
    )

    return render(
        request,
        "my_tasks.html",
        {
            "tasks": matching_tasks,
            "applied_task_ids": applied_task_ids,
        }
    )


# =========================================================
# APPLY FOR TASK
# ONLY NORMAL USER
# =========================================================

@login_required
def apply_task(request, task_id):

    # Manager / Superuser cannot apply

    if request.user.is_superuser or is_manager(request.user):

        messages.error(
            request,
            "Managers and Superusers cannot apply for tasks."
        )

        return redirect("home")

    # -----------------------------------------------------
    # Get task
    # -----------------------------------------------------

    task = get_object_or_404(
        Task,
        id=task_id
    )

    # -----------------------------------------------------
    # POST only
    # -----------------------------------------------------

    if request.method != "POST":

        return redirect("my_tasks")

    # -----------------------------------------------------
    # Task must be Available
    # -----------------------------------------------------

    if task.status != "Available":

        messages.error(
            request,
            "This task is no longer available."
        )

        return redirect("my_tasks")

    # -----------------------------------------------------
    # Already applied?
    # -----------------------------------------------------

    already_applied = TaskApplication.objects.filter(
        task=task,
        user=request.user
    ).exists()

    if already_applied:

        messages.warning(
            request,
            "You have already applied for this task."
        )

        return redirect("my_tasks")

    # -----------------------------------------------------
    # Create application
    # -----------------------------------------------------

    TaskApplication.objects.create(
        task=task,
        user=request.user
    )

    messages.success(
        request,
        "You successfully applied for this task."
    )

    return redirect("my_tasks")

# =========================================================
# ASSIGN WORK
# ONLY MANAGER
# =========================================================

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404


def assignwork(request, user_id):

    user = get_object_or_404(User, id=user_id)

    return render(
        request,
        "assignwork.html",
        {
            "user": user
        }
    )
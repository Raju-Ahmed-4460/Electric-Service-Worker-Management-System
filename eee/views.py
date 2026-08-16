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
    WorkAssignment,
)


User = get_user_model()


def is_manager(user):
    return (
        user.is_authenticated
        and user.groups.filter(
            name="Manager"
        ).exists()
    )


def Userdashboard(request):

    user = request.user

    projects = Project.objects.all().order_by(
        "-created_at"
    )

    tasks = Task.objects.filter(
        status="Available"
    ).select_related(
        "project"
    )

    active_tasks = TaskApplication.objects.none()
    completed_tasks = TaskApplication.objects.none()
    pending_tasks = TaskApplication.objects.none()
    user_projects = Project.objects.none()
    assigned_works = WorkAssignment.objects.none()

    if user.is_authenticated:

        active_tasks = TaskApplication.objects.filter(
            user=user,
            status="Accepted",
            task__status="Assigned"
        ).select_related(
            "task",
            "task__project"
        )

        completed_tasks = TaskApplication.objects.filter(
            user=user,
            status="Accepted",
            task__status="Completed"
        ).select_related(
            "task",
            "task__project"
        )

        pending_tasks = TaskApplication.objects.filter(
            user=user,
            status="Pending"
        ).select_related(
            "task",
            "task__project"
        )

        user_projects = Project.objects.filter(
            tasks__applications__user=user
        ).distinct()

        assigned_works = WorkAssignment.objects.filter(
            worker=user
        ).select_related(
            "worker",
            "assigned_by"
        ).order_by(
            "-assigned_at"
        )

    context = {
        "projects": projects,
        "tasks": tasks,
        "active_tasks": active_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "user_projects": user_projects,
        "assigned_works": assigned_works,
        "is_logged_in": user.is_authenticated,
    }

    return render(
        request,
        "Userdashborad.html",
        context
    )


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


@login_required
def apply_work(request):

    if (
        request.user.is_superuser
        or is_manager(request.user)
    ):

        messages.error(
            request,
            "Managers and Superusers cannot apply for worker jobs."
        )

        return redirect("profile")

    if request.method == "POST":

        form = WorkApplicationForm(request.POST)

        if form.is_valid():

            application = form.save(
                commit=False
            )

            application.user = request.user

            application.save()

            messages.success(
                request,
                "Your work application has been submitted successfully."
            )

            return redirect("profile")

    else:

        form = WorkApplicationForm()

    return render(
        request,
        "apply_work.html",
        {
            "form": form
        }
    )


@login_required
def projects(request):

    project_list = Project.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "projects.html",
        {
            "projects": project_list
        }
    )


@login_required
def activity(request):

    return render(
        request,
        "activity.html"
    )


@login_required
def profile(request):

    user = request.user

    work_applications = WorkApplication.objects.filter(
        user=user
    ).order_by(
        "-id"
    )

    if (
        user.is_superuser
        or is_manager(user)
    ):

        dashboard_url = "managerdashboard"

    else:

        dashboard_url = "userdashboard"

    return render(
        request,
        "profile.html",
        {
            "user": user,
            "work_applications": work_applications,
            "dashboard_url": dashboard_url,
        }
    )


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

            project = form.save(
                commit=False
            )

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

            form.save()

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


@login_required
def my_tasks(request):

    if (
        request.user.is_superuser
        or is_manager(request.user)
    ):

        messages.error(
            request,
            "This page is only for workers."
        )

        return redirect("home")

    assigned_works = WorkAssignment.objects.filter(
        worker=request.user
    ).select_related(
        "assigned_by"
    ).order_by(
        "-assigned_at"
    )

    work_applications = WorkApplication.objects.filter(
        user=request.user,
        status="Accepted"
    )

    work_types = work_applications.values_list(
        "work_type",
        flat=True
    )

    tasks = Task.objects.filter(
        status="Available",
        project__status__in=[
            "Pending",
            "Running"
        ]
    ).select_related(
        "project"
    )

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
            "assigned_works": assigned_works,
            "tasks": matching_tasks,
            "applied_task_ids": applied_task_ids,
        }
    )


@login_required
def apply_task(request, task_id):

    if (
        request.user.is_superuser
        or is_manager(request.user)
    ):

        messages.error(
            request,
            "Managers and Superusers cannot apply for tasks."
        )

        return redirect("home")

    task = get_object_or_404(
        Task,
        id=task_id
    )

    if request.method != "POST":

        return redirect(
            "my_tasks"
        )

    if task.status != "Available":

        messages.error(
            request,
            "This task is no longer available."
        )

        return redirect(
            "my_tasks"
        )

    already_applied = TaskApplication.objects.filter(
        task=task,
        user=request.user
    ).exists()

    if already_applied:

        messages.warning(
            request,
            "You have already applied for this task."
        )

        return redirect(
            "my_tasks"
        )

    TaskApplication.objects.create(
        task=task,
        user=request.user
    )

    messages.success(
        request,
        "You successfully applied for this task."
    )

    return redirect(
        "my_tasks"
    )


@login_required
def assignwork(request, user_id):

    if not is_manager(request.user):

        messages.error(
            request,
            "Only Manager can assign work."
        )

        return redirect("home")

    worker = get_object_or_404(
        User,
        id=user_id
    )

    work_applications = WorkApplication.objects.filter(
        user=worker
    ).order_by(
        "-id"
    )

    if request.method == "POST":

        work_name = request.POST.get(
            "work_name",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        location = request.POST.get(
            "location",
            ""
        ).strip()

        if not work_name:

            messages.error(
                request,
                "Work name is required."
            )

            return render(
                request,
                "assignwork.html",
                {
                    "user": worker,
                    "work_applications": work_applications,
                }
            )

        WorkAssignment.objects.create(
            worker=worker,
            assigned_by=request.user,
            work_title=work_name,
            description=description,
            location=location,
        )

        messages.success(
            request,
            f"Work assigned successfully to {worker.username}."
        )

        return redirect(
            "userlist"
        )

    return render(
        request,
        "assignwork.html",
        {
            "user": worker,
            "work_applications": work_applications,
        }
    )


def explore_services(request):

    services = [
        {
            "icon": "⚡",
            "title": "Electrical Work",
            "description": "Professional electrical installation, repair and maintenance services.",
        },
        {
            "icon": "💡",
            "title": "House Wiring",
            "description": "Complete house wiring, rewiring and electrical connection services.",
        },
        {
            "icon": "🔌",
            "title": "Electrical Repair",
            "description": "Troubleshooting and repair for electrical problems in homes and buildings.",
        },
        {
            "icon": "🔧",
            "title": "Pipe Fitting",
            "description": "Reliable pipe fitting and installation services for residential projects.",
        },
        {
            "icon": "🚿",
            "title": "Plumbing Work",
            "description": "Plumbing installation, repair and maintenance for your home.",
        },
        {
            "icon": "🛠️",
            "title": "Maintenance & Repair",
            "description": "General maintenance and repair services for different types of projects.",
        },
        {
            "icon": "👷",
            "title": "Worker Assignment",
            "description": "Managers can assign suitable workers to specific jobs and projects.",
        },
        {
            "icon": "📋",
            "title": "Task Management",
            "description": "Create, assign, apply for and track work tasks efficiently.",
        },
        {
            "icon": "📍",
            "title": "Location Based Work",
            "description": "Keep track of where assigned work is being performed.",
        },
    ]

    return render(
        request,
        "explore_services.html",
        {
            "services": services,
        }
    )
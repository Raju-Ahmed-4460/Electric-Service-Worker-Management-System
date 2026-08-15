from django.urls import path

from eee.views import (
    Userdashboard,
    Managerdashboard,
    apply_work,
    profile,
    projects,
    activity,
    createproject,
    create_task,
    my_tasks,
    apply_task,
    assignwork,
)


urlpatterns = [

    path(
        "userdashboard/",
        Userdashboard,
        name="userdashboard"
    ),

    path(
        "managerdashboard/",
        Managerdashboard,
        name="managerdashboard"
    ),

    path(
        "apply-work/",
        apply_work,
        name="apply_work"
    ),

    path(
        "projects/",
        projects,
        name="projects"
    ),

    path(
        "activity/",
        activity,
        name="activity"
    ),

    path(
        "profile/",
        profile,
        name="profile"
    ),

    path(
        "create-project/",
        createproject,
        name="createproject"
    ),

    path(
        "create-task/",
        create_task,
        name="create_task"
    ),

    path(
        "my-tasks/",
        my_tasks,
        name="my_tasks"
    ),

    path(
        "apply-task/<int:task_id>/",
        apply_task,
        name="apply_task"
    ),
    path("assignwork/<int:user_id>/",assignwork, name="assignwork")
]
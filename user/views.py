from django.shortcuts import render, redirect, get_object_or_404

from user.forms import (
    RegistrationForm,
    login_form,
    Assign_role_form,
    Create_group_form
)

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required


User = get_user_model()


# =========================================================
# REGISTRATION
# =========================================================

def registration(request):

    form = RegistrationForm()

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data.get("password")
            )

            user.is_active = False

            user.save()

            messages.success(
                request,
                "Registration successful! Check your email address and click the activation link before login."
            )

            return redirect("login")

    return render(
        request,
        "registration.html",
        {
            "form": form
        }
    )


# =========================================================
# ACCOUNT ACTIVATION
# =========================================================

def activate(request, uid, token):

    try:

        uid = urlsafe_base64_decode(uid).decode()

        user = User.objects.get(
            pk=uid
        )

    except:

        user = None

    if user and default_token_generator.check_token(
        user,
        token
    ):

        user.is_active = True

        user.save()

        messages.success(
            request,
            "Your account has been activated. You can now login."
        )

        return redirect("login")

    return HttpResponse(
        "This is invalid link"
    )


# =========================================================
# LOGIN
# =========================================================

def user_login(request):

    form = login_form()

    if request.method == "POST":

        form = login_form(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get(
                "username"
            )

            password = form.cleaned_data.get(
                "password"
            )

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(
                    request,
                    user
                )

                # -----------------------------------------
                # SUPERUSER
                # -----------------------------------------

                if user.is_superuser:

                    return redirect(
                        "admindashboard"
                    )

                # -----------------------------------------
                # MANAGER
                # -----------------------------------------

                if user.groups.filter(
                    name="Manager"
                ).exists():

                    return redirect(
                        "managerdashboard"
                    )

                # -----------------------------------------
                # NORMAL USER
                # -----------------------------------------

                return redirect(
                    "home"
                )

    return render(
        request,
        "login.html",
        {
            "form": form
        }
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def user_logout(request):

    logout(request)

    return redirect(
        "login"
    )


# =========================================================
# HOME
# =========================================================

@login_required
def home(request):

    user = User.objects.all()

    return render(
        request,
        "home.html",
        {
            "user": user
        }
    )


# =========================================================
# ASSIGN GROUP
# SUPERUSER + MANAGER
# =========================================================

@login_required
def assign_role(request, user_id):

    # Superuser OR Manager
    allowed = (
        request.user.is_superuser
        or request.user.groups.filter(
            name="Manager"
        ).exists()
    )

    if not allowed:

        messages.error(
            request,
            "You are not allowed to assign groups."
        )

        return redirect(
            "home"
        )

    user = get_object_or_404(
        User,
        id=user_id
    )

    form = Assign_role_form()

    if request.method == "POST":

        form = Assign_role_form(
            request.POST
        )

        if form.is_valid():

            role = form.cleaned_data.get(
                "role"
            )

            user.groups.clear()

            user.groups.add(
                role
            )

            messages.success(
                request,
                f"{role.name} group assigned to {user.username}."
            )

            return redirect(
                "grouplist"
            )

    return render(
        request,
        "assignrole.html",
        {
            "form": form,
            "user": user
        }
    )


# =========================================================
# CREATE GROUP
# SUPERUSER ONLY
# =========================================================

@login_required
def create_group(request):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Only Superuser can create groups."
        )

        return redirect(
            "home"
        )

    form = Create_group_form()

    if request.method == "POST":

        form = Create_group_form(
            request.POST
        )

        if form.is_valid():

            group = form.save()

            messages.success(
                request,
                f"Group '{group.name}' created successfully."
            )

            return redirect(
                "grouplist"
            )

    return render(
        request,
        "creategroup.html",
        {
            "form": form
        }
    )


# =========================================================
# GROUP LIST
# SUPERUSER + MANAGER
# =========================================================

@login_required
def grouplist(request):

    allowed = (
        request.user.is_superuser
        or request.user.groups.filter(
            name="Manager"
        ).exists()
    )

    if not allowed:

        messages.error(
            request,
            "You are not allowed to view group list."
        )

        return redirect(
            "home"
        )

    groups = Group.objects.prefetch_related(
        "permissions"
    ).all()

    return render(
        request,
        "grouplist.html",
        {
            "groups": groups
        }
    )


# =========================================================
# USER LIST
# SUPERUSER ONLY
# =========================================================

@login_required
def userlist(request):

    # Superuser OR Manager can access
    is_manager = request.user.groups.filter(name="Manager").exists()

    if not request.user.is_superuser and not is_manager:

        messages.error(
            request,
            "Only Superuser and Manager can view users."
        )

        return redirect("home")

    users = User.objects.all()

    return render(
        request,
        "userlist.html",
        {
            "users": users
        }
    )

# =========================================================
# ADMIN DASHBOARD
# SUPERUSER ONLY
# =========================================================

@login_required
def admindashboard(request):

    if not request.user.is_superuser:

        messages.error(
            request,
            "Only Superuser can access Admin Dashboard."
        )

        return redirect(
            "home"
        )

    return render(
        request,
        "admindashboard.html"
    )
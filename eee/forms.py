from django import forms
from .models import WorkApplication, Project, Task


class WorkApplicationForm(forms.ModelForm):

    class Meta:
        model = WorkApplication

        fields = [
            "location",
            "skills",
            "work_type",
            "expected_salary",
            "available_from",
            "description",
        ]

        widgets = {

            "location": forms.TextInput(
                attrs={
                    "class": "w-full border rounded-lg p-3"
                }
            ),

            "skills": forms.Textarea(
                attrs={
                    "class": "w-full border rounded-lg p-3",
                    "rows": 3
                }
            ),

            "work_type": forms.TextInput(
                attrs={
                    "class": "w-full border rounded-lg p-3"
                }
            ),

            "expected_salary": forms.NumberInput(
                attrs={
                    "class": "w-full border rounded-lg p-3"
                }
            ),

            "available_from": forms.DateInput(
                attrs={
                    "class": "w-full border rounded-lg p-3",
                    "type": "date"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "w-full border rounded-lg p-3",
                    "rows": 4
                }
            ),
        }


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = [
            "name",
            "location",
            "description",
            "start_date",
            "end_date",
            "status",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "w-full border rounded-lg p-3"
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "w-full border rounded-lg p-3"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "w-full border rounded-lg p-3",
                    "rows": 4
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "class": "w-full border rounded-lg p-3",
                    "type": "date"
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "class": "w-full border rounded-lg p-3",
                    "type": "date"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "w-full border rounded-lg p-3"
                }
            ),
        }


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            "project",
            "title",
            "description",
            "start_date",
            "end_date",
            "status",
        ]

        widgets = {

            "project": forms.Select(
                attrs={
                    "class": "w-full border rounded-lg p-3"
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "w-full border rounded-lg p-3",
                    "placeholder": "Example: Electrical Wiring"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "w-full border rounded-lg p-3",
                    "rows": 4
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "class": "w-full border rounded-lg p-3",
                    "type": "date"
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "class": "w-full border rounded-lg p-3",
                    "type": "date"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "w-full border rounded-lg p-3"
                }
            ),
        }
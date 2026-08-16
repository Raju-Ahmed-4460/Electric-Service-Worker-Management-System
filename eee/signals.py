from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import WorkAssignment



@receiver(
    post_save,
    sender=WorkAssignment
)
def send_work_assignment_email(
    sender,
    instance,
    created,
    **kwargs
):


    if not created:
        return


    worker = instance.worker

    if not worker.email:
        return

    send_mail(
        subject="New Work Assigned",

        message=(
            f"Hello {worker.username},\n\n"

            f"You have been assigned a new work.\n\n"

            f"Work: {instance.work_title}\n"

            f"Description: "
            f"{instance.description or 'No description provided.'}\n"

            f"Location: "
            f"{instance.location or 'Not specified.'}\n\n"

            f"Please check your dashboard for more details.\n\n"

            f"Thank you."
        ),

        from_email=settings.DEFAULT_FROM_EMAIL,

        recipient_list=[
            worker.email
        ],

        fail_silently=False,
    )
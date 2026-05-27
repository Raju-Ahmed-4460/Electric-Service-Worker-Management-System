from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import Group

User = get_user_model()

@receiver(post_save,sender=User)
def user_activation_mail(sender,instance,created,**kwargs):

    if created and  not instance.is_active:
        uid=urlsafe_base64_encode(force_bytes(instance.pk))
        token=default_token_generator.make_token(instance)

        link=f"{settings.FRONTEND_URL}/activate/{uid}/{token}/"

        send_mail(
            f"{instance.username} active your account",
            f"Click here to activate: \n{link}",
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,

        )


@receiver(post_save,sender=User)
def assign_group(sender,instance,created,**kwargs):
    if created:
         usergroup,create=Group.objects.get_or_create(name='User')
         instance.groups.add(usergroup)
         instance.save()


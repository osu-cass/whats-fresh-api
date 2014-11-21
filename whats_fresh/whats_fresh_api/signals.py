from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group


@receiver(post_save, sender=User)
def default_group_callback(sender, instance, *args, **kwargs):
    if instance.groups.filter(name='Data Entry Users').exists():
        return
    else:
        group = Group.objects.get(name='Data Entry Users')
        instance.groups.add(group)
        instance.save()
        return

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from accounts.models import Profile
from storage.views import folder_create_root
from storage.utils import generate_random_name

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created:
            Profile.objects.create(user=instance)
    except Exception as err:
        print(f'Error creating user profile!\n{err}')


# TODO: move
@receiver(post_save, sender=User)
def create_root_directory(sender, instance, created, **kwargs):
    try:
        if created:
            name = generate_random_name(10) + '/'
            print(f'creating folder for user:{instance.id}; folder_name: {name}')
            folder_create_root(instance.id, name)
    except Exception as err:
         print(f'Error creating user profile!\n{err}')

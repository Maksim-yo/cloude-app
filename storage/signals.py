import random

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from storage.views import folder_create_root

test_names = ['hello', 'asgdf', 'cdcads', 'adsfa']


@receiver(post_save, sender=User)
def create_root_directory(sender, instance, created, **kwargs):
    try:
        if created:
            name = test_names[random.randrange(len(test_names))]
            folder_create_root(instance.id, name)
    except Exception as err:
        print(f'Error creating user profile!\n{err}')

#
# @receiver(post_save, sender=User)
# def save_root_directory(sender, instance, **kwargs):
#     instance.storage_items.save()

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
import logging

from accounts.models import Profile
from storage.utils import generate_random_name
import storage.config as config


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created:
            logging.debug(f'creating profile for user:{instance.id}')
            Profile.objects.create(user=instance)
    except Exception as err:
        logging.critical(f'Error creating user profile!\n{err}')


@receiver(post_save, sender=User)
def create_root_directory(sender, instance, created, **kwargs):
    try:
        if created:
            name = generate_random_name(10) + '/'
            logging.info(f'creating root folder for user:{instance.id}; folder_name: {name}')
            config.folder_service.save_root_folder(instance.id, name)
    except Exception as err:
        logging.critical(f'Error creating user profile!\n{err}')

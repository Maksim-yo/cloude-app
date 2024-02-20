from django.db import models
from django.conf import settings
from polymorphic.models import PolymorphicModel


class StorageItem(PolymorphicModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="storage_items", on_delete=models.CASCADE
    )
    path = models.CharField(max_length=2048, null=False)
    bucket = models.CharField(max_length=255, null=False)
    hash = models.CharField(max_length=255, null=False)
    size = models.IntegerField(null=False)
    last_modified = models.DateTimeField(null=False)
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE, related_name="items")
    is_dir = models.BooleanField(null=False)
    name = models.CharField(max_length=255, null=False)


class  RootStorageItem(StorageItem):
    user_root = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="root_item", on_delete=models.CASCADE
    )

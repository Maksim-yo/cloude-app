from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import signals

from storage.services.dao.StorageDAO import StorageDAO, RootStorageItem
from storage.services.dto.StorageItemDTO import StorageDTO
from storage.minio.MinioPathFactory import MinioObjectFactory
from storage.models import StorageItem


# TODO: Add mock for ObjectFactory
class DAOTest(TestCase):

    def setUp(self):
        signals.post_save.receivers = []
        object_factory = MinioObjectFactory()
        self.storage = StorageDAO(object_factory)
        self.user = User.objects.create_user('user')
        self.date = timezone.now()
        self.folder_item = StorageItem.objects.create(user=self.user, path="test", bucket='test', hash='test',
                                                      size=0, last_modified=self.date, is_dir=True, name='test')
        self.folder_item_dto = self.storage._orm_to_entity(self.folder_item)

    def test_get_user(self):
        user = self.storage.get_user(self.user.id)
        _user = User.objects.get(pk=self.user.id)
        self.assertEqual(user, _user)

    def test_is_object_exist(self):
        res = self.storage.is_object_exist(self.user.id, "test")
        self.assertEqual(res, True)

    def test_get_object(self):
        res = self.storage.get_object(self.user.id, self.folder_item.hash)
        self.assertEqual(res.hash, self.folder_item.hash)

    def test_create_root(self):
        new_item = StorageDTO("hello", 'hello', self.user.id, 'hello', 0, str(self.date), True, 'hello')
        res = self.storage.create_root_folder(new_item)
        self.assertEqual(self.user.root_item.hash, res.hash)

    def test_get_root(self):
        user = User.objects.get(pk=self.user.id)
        new_item = RootStorageItem.objects.create(
            user=user,
            path="hello",
            bucket="hello",
            hash="hello",
            size=0,
            last_modified=self.date,
            is_dir=True,
            user_root=user,
            name="hello",
        )
        res = self.storage._orm_to_entity(new_item)
        root = self.storage.get_root_object(self.user.id)
        self.assertEqual(res.hash, root.hash)

    def test_create_object(self):
        new_item = StorageDTO("hello", 'hello', self.user.id, 'hello', 0, str(self.date), True, 'hello')
        res = self.storage.create_object(new_item, self.folder_item.hash, new_item.user_id)
        item = StorageItem.objects.get(hash__exact=res.hash)
        self.assertEqual(item.hash, res.hash)

    def test_object_parent(self):
        new_item = StorageItem.objects.create(user=self.user, path="hello", bucket='hello', hash='hello', size=0,
                                   last_modified=self.date, is_dir=True, parent=self.folder_item, name='hello')
        item_parent = self.storage.object_parent(self.user.id, new_item.hash)
        self.assertEqual(self.folder_item_dto.hash, item_parent.hash)

    def test_lists_objects_recursive(self):
        item1 = StorageItem.objects.create(user=self.user, path="hello1", bucket='hello1', hash='hello1', size=0,
                                           last_modified=self.date, parent=self.folder_item, is_dir=True, name='hello1')
        item2 = StorageItem.objects.create(user=self.user, path="hello2", bucket='hello2', hash='hello2', size=0,
                                           last_modified=self.date, parent=self.folder_item, is_dir=True, name='hello2')
        item3 = StorageItem.objects.create(user=self.user, path="hello3", bucket='hello3', hash='hello3', size=0,
                                           last_modified=self.date, parent=self.folder_item, is_dir=True, name='hello3')

        data = []
        self.storage._list_objects_recursive(data, self.folder_item)
        _data = [item for sublist in data for item in sublist]
        self.assertEqual(len(_data), 3)
        self.assertIn(item1, _data)
        self.assertIn(item2, _data)
        self.assertIn(item3, _data)

    def test_delete_object(self):
        item = StorageItem.objects.create(user=self.user, path="hello1", bucket='hello1', hash='hello1', size=0,
                                           last_modified=self.date, parent=self.folder_item, is_dir=True, name='hello1')
        deleted_items = self.storage.delete_object(self.user.id, item.hash)
        self.assertEqual(len(deleted_items), 1)
        self.assertEqual(deleted_items[0].hash, item.hash)

    def test_delete_object_recursive(self):
        item2 = StorageItem.objects.create(user=self.user, path="hello2", bucket='hello2', hash='hello2', size=0,
                                           last_modified=self.date, parent=self.folder_item, is_dir=True, name='hello2')
        item3 = StorageItem.objects.create(user=self.user, path="hello3", bucket='hello3', hash='hello3', size=0,
                                           last_modified=self.date, parent=item2, is_dir=True, name='hello3')
        deleted_items = self.storage.delete_object(self.user.id, item2.hash)
        deleted_items_hash = [item.hash for item in deleted_items]
        self.assertEqual(len(deleted_items), 2)
        self.assertIn(item2.hash, deleted_items_hash)
        self.assertIn(item3.hash, deleted_items_hash)

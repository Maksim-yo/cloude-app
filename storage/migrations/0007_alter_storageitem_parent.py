# Generated by Django 4.2.6 on 2023-11-26 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0006_storageitem_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storageitem',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='storage.storageitem'),
        ),
    ]

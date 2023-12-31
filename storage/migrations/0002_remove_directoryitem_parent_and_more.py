# Generated by Django 4.2.6 on 2023-11-05 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='directoryitem',
            name='parent',
        ),

        migrations.AddField(
            model_name='storageitem',
            name='hash',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storageitem',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item', to='storage.storageitem'),
        ),
    ]

# Generated by Django 4.2.16 on 2024-12-14 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('region_app', '0021_alter_notification_system'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('manager', 'cooperative managers'), ('AD', 'admin')], max_length=50, null=True),
        ),
    ]
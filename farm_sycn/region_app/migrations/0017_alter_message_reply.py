# Generated by Django 4.2.16 on 2024-12-07 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('region_app', '0016_alter_cooperative_location_cell_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='reply',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
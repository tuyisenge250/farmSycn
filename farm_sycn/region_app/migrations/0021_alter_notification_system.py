# Generated by Django 4.2.16 on 2024-12-14 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('region_app', '0020_message_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='region_app.cooperative'),
        ),
    ]

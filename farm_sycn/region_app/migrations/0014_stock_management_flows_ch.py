# Generated by Django 4.2.16 on 2024-11-30 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('region_app', '0007_alter_notification_date_alter_stock_management_flows'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock_management',
            name='flows_ch',
            field=models.CharField(choices=[('IN', 'Input Stock'), ('OUT', 'Output Stock')], default='IN', max_length=50),
        ),
    ]

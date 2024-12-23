# Generated by Django 4.2.16 on 2024-12-01 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('region_app', '0014_stock_management_flows_ch'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cooperative',
            old_name='location',
            new_name='location_village',
        ),
        migrations.AddField(
            model_name='cooperative',
            name='location_cell',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cooperative',
            name='location_district',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='cooperative',
            name='location_province',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='cooperative',
            name='location_sector',
            field=models.CharField(max_length=60, null=True),
        ),
    ]

# Generated by Django 5.1 on 2024-08-28 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ships', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='positionreport',
            name='cargo_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='positionreport',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='positionreport',
            name='ship_id',
            field=models.CharField(max_length=255),
        ),
    ]

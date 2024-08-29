# Generated by Django 5.1 on 2024-08-28 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ships', '0002_positionreport_cargo_type_positionreport_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='positionreport',
            name='speed',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='positionreport',
            name='cargo_type',
            field=models.CharField(default='NIL', max_length=255),
        ),
        migrations.AlterField(
            model_name='positionreport',
            name='name',
            field=models.CharField(default='NIL', max_length=255),
        ),
        migrations.AlterField(
            model_name='positionreport',
            name='ship_id',
            field=models.CharField(max_length=100),
        ),
    ]

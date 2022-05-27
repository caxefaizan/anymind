# Generated by Django 4.0.4 on 2022-05-27 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeclock', '0007_rename_clockin_clock_clockedin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clock',
            name='clockedIn',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clock',
            name='clockedOut',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clock',
            name='totalHours',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]

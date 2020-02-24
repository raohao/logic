# Generated by Django 2.0.4 on 2018-05-15 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guard', '0002_auto_20180515_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='guardplan',
            name='guard_level',
            field=models.CharField(choices=[('normal', '平时'), ('prepare', '备战'), ('wartime', '战时')], default='normal', max_length=10, verbose_name='保障等级'),
        ),
    ]
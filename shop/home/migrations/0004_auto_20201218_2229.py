# Generated by Django 3.1.1 on 2020-12-18 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20201218_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

# Generated by Django 3.1.1 on 2020-12-18 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
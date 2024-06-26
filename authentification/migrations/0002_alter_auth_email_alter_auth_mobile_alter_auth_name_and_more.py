# Generated by Django 5.0.6 on 2024-05-19 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auth',
            name='email',
            field=models.TextField(max_length=320, unique=True),
        ),
        migrations.AlterField(
            model_name='auth',
            name='mobile',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='auth',
            name='name',
            field=models.TextField(max_length=20),
        ),
        migrations.AlterField(
            model_name='auth',
            name='regNo',
            field=models.TextField(max_length=500, unique=True),
        ),
    ]

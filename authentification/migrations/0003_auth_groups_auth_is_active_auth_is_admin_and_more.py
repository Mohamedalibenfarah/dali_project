# Generated by Django 5.0.6 on 2024-05-19 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('authentification', '0002_alter_auth_email_alter_auth_mobile_alter_auth_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auth',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='auth_users', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='auth',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='auth',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='auth',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='auth',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='auth',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='auth_users', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='auth',
            name='email',
            field=models.EmailField(max_length=320, unique=True),
        ),
        migrations.AlterField(
            model_name='auth',
            name='mobile',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='auth',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='auth',
            name='password',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='auth',
            name='regNo',
            field=models.CharField(max_length=500, unique=True),
        ),
    ]

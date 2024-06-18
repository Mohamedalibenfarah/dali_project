# Generated by Django 5.0.6 on 2024-06-18 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mydata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Assistant', models.FloatField(blank=True, null=True)),
                ('TMission', models.CharField(max_length=100)),
                ('CMission', models.CharField(max_length=100)),
                ('Raison_sociale', models.CharField(max_length=100)),
                ('Description', models.CharField(max_length=1000)),
                ('Client', models.CharField(max_length=100)),
                ('Manager', models.FloatField(blank=True, null=True)),
                ('Date', models.DateField()),
                ('Libellé', models.CharField(max_length=100)),
                ('Nbre_heures', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]

# Generated by Django 3.1.5 on 2021-01-17 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BylawException',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=10)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BylawSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.CharField(max_length=128)),
                ('area', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=10)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GeoJson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
            ],
        ),
    ]
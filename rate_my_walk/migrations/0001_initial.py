# Generated by Django 2.2.17 on 2021-03-26 10:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('views', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('owner', models.CharField(max_length=128)),
                ('picture', models.ImageField(blank=True, upload_to='page_image')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('url', models.URLField()),
                ('views', models.IntegerField(default=0)),
                ('length', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=0)),
                ('difficulty', models.IntegerField(default=0)),
                ('enjoyment', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WalkPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('desc', models.CharField(max_length=128, unique=True)),
                ('start', models.CharField(max_length=128, unique=True)),
                ('end', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('enjoyment', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=0)),
                ('difficulty', models.IntegerField(default=0)),
                ('date', models.DateField(default=datetime.datetime(2021, 3, 26, 10, 2, 13, 822999, tzinfo=utc))),
            ],
            options={
                'verbose_name_plural': 'Walks',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('url', models.URLField()),
                ('views', models.IntegerField(default=0)),
                ('picture', models.ImageField(blank=True, upload_to='page_image')),
                ('startPoint', models.CharField(max_length=32)),
                ('endPoint', models.CharField(max_length=32)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_my_walk.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('url', models.URLField()),
                ('views', models.IntegerField(default=0)),
                ('comment', models.CharField(max_length=128)),
                ('owner', models.CharField(max_length=128)),
                ('date', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_my_walk.Category')),
            ],
        ),
    ]

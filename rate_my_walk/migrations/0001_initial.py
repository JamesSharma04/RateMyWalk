# Generated by Django 2.2.17 on 2021-04-03 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WalkPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('desc', models.CharField(max_length=2048)),
                ('start', models.CharField(max_length=128)),
                ('end', models.CharField(max_length=128)),
                ('slug', models.SlugField(unique=True)),
                ('cover', models.ImageField(default='default.jpg', upload_to='page_image')),
                ('enjoyment', models.IntegerField(default=5)),
                ('duration', models.IntegerField(default=5)),
                ('difficulty', models.IntegerField(default=5)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Walks',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(default=0)),
                ('difficulty', models.IntegerField(default=0)),
                ('enjoyment', models.IntegerField(default=0)),
                ('rater', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Rater', to=settings.AUTH_USER_MODEL)),
                ('walk', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rate_my_walk.WalkPage')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('picture', models.ImageField(default='default.jpg', upload_to='more_page_image')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Uploader', to=settings.AUTH_USER_MODEL)),
                ('walk', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rate_my_walk.WalkPage')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('comment', models.CharField(max_length=128)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Owner', to=settings.AUTH_USER_MODEL)),
                ('walk', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rate_my_walk.WalkPage')),
            ],
        ),
    ]

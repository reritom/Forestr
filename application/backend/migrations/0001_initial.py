# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-08 18:17
from __future__ import unicode_literals

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
            name='Contract',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(default='pending', max_length=255)),
                ('contract_type', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('external_id', models.CharField(max_length=255)),
                ('tags', models.CharField(max_length=255, null=True)),
                ('photos', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('location', models.CharField(max_length=255, null=True)),
                ('location_description', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('moderator', models.BooleanField(default=False)),
                ('joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('origin', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('description', models.CharField(max_length=255)),
                ('personal', models.BooleanField(default=True)),
                ('enterprise', models.BooleanField(default=False)),
                ('publicly_searchable', models.BooleanField(default=True)),
                ('founder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='founder', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Organisation')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('survey_type', models.CharField(default='Misc', max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(null=True)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Organisation')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyItem',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('notes', models.CharField(max_length=255)),
                ('photos', models.CharField(max_length=255)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Item')),
                ('survey', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Survey')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Organisation'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Organisation'),
        ),
        migrations.AddField(
            model_name='contract',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Organisation'),
        ),
        migrations.AddField(
            model_name='contract',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

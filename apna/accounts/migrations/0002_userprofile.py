# Generated by Django 5.2 on 2025-04-17 18:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_me', models.TextField(blank=True, null=True)),
                ('skills', models.TextField(blank=True, help_text='Comma-separated skills', null=True)),
                ('work_experience', models.TextField(blank=True, null=True)),
                ('education', models.TextField(blank=True, null=True)),
                ('projects', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

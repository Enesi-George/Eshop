# Generated by Django 5.0.4 on 2024-04-22 08:34

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=150, validators=[django.core.validators.RegexValidator(message='Name must contain only letters and no spaces.', regex='^[a-zA-Z]+$')])),
                ('last_name', models.CharField(max_length=150, validators=[django.core.validators.RegexValidator(message='Name must contain only letters and no spaces.', regex='^[a-zA-Z]+$')])),
                ('email', models.EmailField(error_messages={'unique': 'A user with this email already exists.'}, max_length=254, unique=True)),
                ('username', models.CharField(error_messages={'unique': 'A user with this username already exists.'}, max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Username must contain only letters and numbers with no spaces.', regex='^[a-zA-Z0-9]+$')])),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='custom_user_set', related_query_name='custom_user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='custom_user_set', related_query_name='custom_user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
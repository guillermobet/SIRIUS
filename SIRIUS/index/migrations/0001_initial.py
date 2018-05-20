# Generated by Django 2.0.4 on 2018-05-20 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import index.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user', models.CharField(max_length=40, unique=True, verbose_name='Usuario')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Correo electronico')),
                ('full_name', models.CharField(blank=True, max_length=100, verbose_name='Nombre completo')),
                ('telephone', models.CharField(blank=True, max_length=11, verbose_name='Telefono')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', index.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Criteria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('acronym', models.CharField(max_length=3, unique=True)),
                ('metric', models.CharField(max_length=12)),
                ('atribute', models.CharField(max_length=12)),
                ('comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Heuristic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('acronym', models.CharField(max_length=2, unique=True)),
                ('comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('browser', models.CharField(max_length=20)),
                ('browser_version', models.CharField(max_length=10)),
                ('comment', models.TextField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='user')),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.URLField(unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='website',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Website'),
        ),
        migrations.AddField(
            model_name='heuristic',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Review'),
        ),
        migrations.AddField(
            model_name='criteria',
            name='heuristic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Heuristic'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('website', 'username')},
        ),
    ]

# Generated by Django 2.0.4 on 2018-06-05 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_auto_20180604_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='type',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
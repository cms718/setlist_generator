# Generated by Django 3.0.6 on 2020-05-25 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0008_auto_20200520_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='is_slow_song',
            field=models.BooleanField(default=False, verbose_name='slow song'),
        ),
    ]

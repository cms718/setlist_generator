# Generated by Django 3.0.6 on 2020-05-20 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0007_band_creator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='key',
            new_name='song_key',
        ),
    ]

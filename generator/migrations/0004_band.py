# Generated by Django 3.0.6 on 2020-05-17 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0003_auto_20200516_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band_name', models.CharField(max_length=40)),
            ],
        ),
    ]

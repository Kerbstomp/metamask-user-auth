# Generated by Django 4.1.5 on 2023-02-01 22:27

import api.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField(blank=True)),
                ('public_address', models.TextField(unique=True)),
                ('nonce', models.BigIntegerField(default=api.utils.get_new_nonce)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

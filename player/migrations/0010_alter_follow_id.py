# Generated by Django 5.2.1 on 2025-05-31 04:58

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0009_profile_backgroundphoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]

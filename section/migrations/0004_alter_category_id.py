# Generated by Django 5.2.1 on 2025-05-30 05:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('section', '0003_alter_category_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]

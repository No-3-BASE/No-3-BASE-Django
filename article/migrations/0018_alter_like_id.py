# Generated by Django 5.2.1 on 2025-05-31 15:35

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0017_article_bookmark_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]

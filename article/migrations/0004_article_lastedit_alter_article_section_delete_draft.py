# Generated by Django 5.2.1 on 2025-05-29 08:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_alter_article_author_alter_draft_author'),
        ('board', '0005_rename_created_at_section_createdat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='lastEdit',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='board.section'),
        ),
        migrations.DeleteModel(
            name='Draft',
        ),
    ]

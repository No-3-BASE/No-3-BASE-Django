# Generated by Django 5.2.1 on 2025-06-08 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0014_profile_comment_visibility_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bookmark_visibility',
            field=models.CharField(choices=[('public', '公開'), ('fans', '僅限粉絲'), ('private', '私人')], default='public', max_length=10),
        ),
    ]

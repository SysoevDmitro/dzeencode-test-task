# Generated by Django 5.0.6 on 2025-01-20 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='comments/media'),
        ),
    ]

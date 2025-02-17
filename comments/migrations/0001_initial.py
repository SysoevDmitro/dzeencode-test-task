# Generated by Django 5.0.6 on 2025-01-17 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя пользователя')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('home_page', models.URLField(blank=True, null=True, verbose_name='Домашняя страница')),
                ('captcha', models.CharField(max_length=6, verbose_name='Капча')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='comments.comment')),
            ],
        ),
    ]

# Generated by Django 3.2.3 on 2021-05-21 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discord_posts', '0006_alter_post_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='related_ticker',
        ),
    ]
# Generated by Django 3.2.3 on 2021-05-19 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discord_posts', '0004_alter_post_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

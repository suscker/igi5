# Generated by Django 5.2.1 on 2025-06-10 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0021_remove_article_img_url_remove_master_img_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='img_url',
            field=models.CharField(default='', max_length=500),
        ),
    ]

# Generated by Django 4.1.2 on 2022-10-06 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum', '0003_painting_is_published_painting_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='church',
            name='city',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='church',
            name='state',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='engraving',
            name='book',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]

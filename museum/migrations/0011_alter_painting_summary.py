# Generated by Django 4.1.2 on 2022-11-17 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum', '0010_alter_author_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='painting',
            name='summary',
            field=models.TextField(blank=True),
        ),
    ]
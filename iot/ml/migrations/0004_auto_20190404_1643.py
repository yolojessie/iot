# Generated by Django 2.1.7 on 2019-04-04 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ml', '0003_survive_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='survive',
            options={'ordering': ['id']},
        ),
    ]

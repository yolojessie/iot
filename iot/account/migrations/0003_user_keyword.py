# Generated by Django 2.1.7 on 2019-06-13 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20190613_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='keyword',
            field=models.TextField(blank=True, null=True),
        ),
    ]

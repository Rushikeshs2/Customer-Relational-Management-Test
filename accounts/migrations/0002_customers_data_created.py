# Generated by Django 3.1 on 2020-09-14 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='data_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

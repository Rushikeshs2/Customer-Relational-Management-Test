# Generated by Django 3.1.2 on 2020-12-09 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='email',
            field=models.CharField(default=False, max_length=100),
        ),
    ]

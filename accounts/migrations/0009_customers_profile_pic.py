# Generated by Django 3.1 on 2020-09-29 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_customers_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]

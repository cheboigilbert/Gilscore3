# Generated by Django 3.2.9 on 2021-12-19 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0008_auto_20211202_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]

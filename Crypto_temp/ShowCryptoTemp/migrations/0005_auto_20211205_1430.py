# Generated by Django 2.2.5 on 2021-12-05 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShowCryptoTemp', '0004_auto_20211205_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapper',
            name='created_utc',
            field=models.IntegerField(null=True),
        ),
    ]

# Generated by Django 2.2.5 on 2021-11-21 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShowCryptoTemp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='scrapper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=10)),
                ('author', models.CharField(max_length=100)),
                ('title', models.TextField()),
                ('selftext', models.TextField()),
                ('created_utc', models.IntegerField()),
                ('num_comments', models.IntegerField()),
                ('score', models.IntegerField()),
                ('title_vader', models.FloatField()),
            ],
        ),
    ]
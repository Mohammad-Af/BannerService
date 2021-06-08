# Generated by Django 3.2.4 on 2021-06-08 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Impression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_id', models.IntegerField()),
                ('campaign_id', models.IntegerField()),
                ('quarter', models.IntegerField()),
            ],
            options={
                'unique_together': {('banner_id', 'campaign_id', 'quarter')},
            },
        ),
        migrations.CreateModel(
            name='Conversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conversion_id', models.IntegerField()),
                ('click_id', models.IntegerField()),
                ('revenue', models.IntegerField()),
                ('quarter', models.IntegerField()),
            ],
            options={
                'unique_together': {('conversion_id', 'quarter')},
            },
        ),
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('click_id', models.IntegerField()),
                ('banner_id', models.IntegerField()),
                ('campaign_id', models.IntegerField()),
                ('quarter', models.IntegerField()),
            ],
            options={
                'unique_together': {('click_id', 'quarter')},
            },
        ),
    ]
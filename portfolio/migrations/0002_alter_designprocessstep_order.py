# Generated by Django 5.0.6 on 2024-08-14 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designprocessstep',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]

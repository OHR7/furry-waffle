# Generated by Django 4.0.4 on 2022-05-16 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kudos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kudo',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

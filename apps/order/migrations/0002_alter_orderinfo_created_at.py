# Generated by Django 3.2.11 on 2022-01-22 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='created_at',
            field=models.TimeField(editable=False),
        ),
    ]

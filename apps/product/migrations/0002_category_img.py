# Generated by Django 3.2.11 on 2022-01-11 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='img',
            field=models.ImageField(null=True, upload_to='Images/'),
        ),
    ]
# Generated by Django 3.2.11 on 2022-01-19 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_botuser_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='botuser',
            name='address',
        ),
        migrations.CreateModel(
            name='AddressItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=300, null=True)),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.address')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.botuser'),
        ),
    ]

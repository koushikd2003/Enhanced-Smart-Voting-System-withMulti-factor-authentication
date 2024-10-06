# Generated by Django 3.2 on 2024-09-25 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate', models.CharField(max_length=255)),
                ('date_voted', models.DateTimeField(auto_now_add=True)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base.userprofile')),
            ],
        ),
    ]

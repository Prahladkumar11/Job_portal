# Generated by Django 4.2.6 on 2023-11-04 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portal_app', '0020_jobdetails_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=254)),
                ('Sub', models.CharField(max_length=250)),
                ('Msg', models.CharField(max_length=500)),
            ],
        ),
    ]

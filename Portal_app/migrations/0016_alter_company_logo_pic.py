# Generated by Django 4.2.3 on 2023-08-06 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portal_app', '0015_delete_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo_pic',
            field=models.ImageField(default='images/default/d1.png', upload_to='img/Company'),
        ),
    ]

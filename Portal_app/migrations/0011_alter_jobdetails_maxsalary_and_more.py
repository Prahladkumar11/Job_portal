# Generated by Django 4.2.3 on 2023-08-05 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portal_app', '0010_alter_jobdetails_qualification_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobdetails',
            name='maxSalary',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='jobdetails',
            name='minSalary',
            field=models.CharField(max_length=10),
        ),
    ]
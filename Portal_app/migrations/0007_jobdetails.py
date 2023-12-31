# Generated by Django 4.2.3 on 2023-08-04 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Portal_app', '0006_alter_company_aboutus'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('JobTitle', models.CharField(max_length=250)),
                ('JobType', models.CharField(max_length=250)),
                ('JobDescription', models.TextField()),
                ('JobLocation', models.CharField(max_length=250)),
                ('minSalary', models.IntegerField()),
                ('maxSalary', models.IntegerField()),
                ('JobExperience', models.IntegerField()),
                ('Qualification', models.CharField(max_length=300)),
                ('Responsiblity', models.CharField(max_length=300)),
                ('Company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Portal_app.company')),
            ],
        ),
    ]

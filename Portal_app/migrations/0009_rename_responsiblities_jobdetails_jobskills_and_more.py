# Generated by Django 4.2.3 on 2023-08-04 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portal_app', '0008_rename_responsiblity_jobdetails_responsiblities'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobdetails',
            old_name='Responsiblities',
            new_name='JobSkills',
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='PostDate',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='jobdetails',
            name='Responsibilities',
            field=models.CharField(max_length=300, null=True),
        ),
    ]

# Generated by Django 4.1.1 on 2022-11-30 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eduficationapp", "0008_student_s_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="faculty",
            name="f_status",
            field=models.CharField(
                choices=[("Active", "Active"), ("Inactive", "Inactive")],
                default="Active",
                max_length=200,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="s_status",
            field=models.CharField(
                choices=[("Active", "Active"), ("Inactive", "Inactive")],
                default="Active",
                max_length=200,
                null=True,
            ),
        ),
    ]

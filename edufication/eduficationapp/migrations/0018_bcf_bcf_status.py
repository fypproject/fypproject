# Generated by Django 4.1.1 on 2023-03-18 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eduficationapp", "0017_quizsubmit_qs_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="bcf",
            name="bcf_status",
            field=models.CharField(default="In Progress", max_length=100),
        ),
    ]

# Generated by Django 4.1.1 on 2022-12-21 13:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("eduficationapp", "0012_quiz_quizquestion"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attendance",
            fields=[
                ("at_id", models.AutoField(primary_key=True, serialize=False)),
                ("at_name", models.CharField(max_length=255)),
                ("at_date", models.DateField()),
                (
                    "at_bcfid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="eduficationapp.bcf",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AttendanceRecord",
            fields=[
                ("atr_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "atr_option",
                    models.CharField(
                        choices=[
                            ("Present", "Present"),
                            ("Absent", "Absent"),
                            ("Late", "Late"),
                            ("Excused", "Excused"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "atr_atid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="eduficationapp.attendance",
                    ),
                ),
                (
                    "atr_studentid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

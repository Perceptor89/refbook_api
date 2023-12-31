# Generated by Django 4.2.4 on 2023-08-14 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Refbook",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=100, unique=True, verbose_name="Код"),
                ),
                ("name", models.CharField(max_length=300, verbose_name="Наименование")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
            ],
            options={
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="RefbookVersion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("version", models.CharField(max_length=50)),
                ("active_from", models.DateTimeField(unique=True)),
                (
                    "refbook",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="versions",
                        to="refbook.refbook",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RefbookElement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=100)),
                ("name", models.CharField(max_length=300)),
                (
                    "refbook_version",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="elements",
                        to="refbook.refbookversion",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="refbookelement",
            constraint=models.UniqueConstraint(
                fields=("refbook_version", "code"), name="unique_version_element_code"
            ),
        ),
    ]

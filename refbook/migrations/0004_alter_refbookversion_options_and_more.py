# Generated by Django 4.2.4 on 2023-08-15 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("refbook", "0003_alter_refbook_options_alter_refbookelement_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="refbookversion",
            options={"verbose_name": "Версия", "verbose_name_plural": "Версии"},
        ),
        migrations.AddConstraint(
            model_name="refbookversion",
            constraint=models.UniqueConstraint(
                fields=("refbook", "version"), name="unique_refbook_version"
            ),
        ),
    ]
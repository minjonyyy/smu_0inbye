# Generated by Django 4.2.13 on 2024-10-28 07:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api_app", "0003_pdffile_summary"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Document",
        ),
        migrations.DeleteModel(
            name="JsonDb",
        ),
        migrations.DeleteModel(
            name="PDFFile",
        ),
    ]

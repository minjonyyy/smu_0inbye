# Generated by Django 5.0.3 on 2024-08-20 16:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PDFFile",
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
                ("file_name", models.CharField(max_length=255)),
                ("file_data", models.BinaryField()),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="document",
            name="individual_fee",
        ),
        migrations.RemoveField(
            model_name="document",
            name="management_fee",
        ),
        migrations.RemoveField(
            model_name="document",
            name="mortgage",
        ),
        migrations.RemoveField(
            model_name="document",
            name="transaction_info",
        ),
        migrations.AddField(
            model_name="document",
            name="json_original_file_location",
            field=models.CharField(
                default=0, max_length=255, verbose_name="JSON 원본 파일 위치"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="address",
            name="full_address",
            field=models.CharField(default="입력되지 않음", max_length=255),
        ),
        migrations.AlterField(
            model_name="document",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="document",
            name="mager_info",
            field=models.CharField(max_length=50),
        ),
    ]
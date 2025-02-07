# Generated by Django 4.2.13 on 2024-10-29 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file_data',
            field=models.BinaryField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='file_name',
            field=models.CharField(default='noname.pdf', max_length=255),
        ),
        migrations.AddField(
            model_name='post',
            name='safety',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='summary',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

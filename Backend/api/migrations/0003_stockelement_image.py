# Generated by Django 5.0.2 on 2024-05-24 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_stockelement_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockelement',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='stock'),
        ),
    ]
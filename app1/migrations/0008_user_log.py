# Generated by Django 4.1.7 on 2023-04-02 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_remove_orders_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='log',
            field=models.JSONField(default=1),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.1.7 on 2023-04-02 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_remove_user_id_remove_user_log_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.BigIntegerField(),
        ),
    ]

# Generated by Django 4.1.7 on 2023-04-16 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0018_remove_category_description_remove_product_sub_ctg_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='log',
            field=models.JSONField(default=1, verbose_name={'order': 0}),
            preserve_default=False,
        ),
    ]

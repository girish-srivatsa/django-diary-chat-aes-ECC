# Generated by Django 3.1.1 on 2020-09-14 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20200913_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encrypt',
            name='iv_dek',
            field=models.BinaryField(default=b'\xe6\xe1N\xd4\x12ai\xda-@\xad\xaf\xa3\x93_\x08'),
        ),
        migrations.AlterField(
            model_name='encrypt',
            name='iv_kek',
            field=models.BinaryField(default=b'\x061\xd8\xb6\x88\xd7?%\x7f\xc9\x80)\xf7@AK'),
        ),
        migrations.AlterField(
            model_name='encrypt',
            name='salt_kek',
            field=models.BinaryField(default=b'\x95\xd86\x14\xae\xf5\xc8\x0f'),
        ),
    ]

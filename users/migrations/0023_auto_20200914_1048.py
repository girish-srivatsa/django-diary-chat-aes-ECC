# Generated by Django 3.1.1 on 2020-09-14 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20200914_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encrypt',
            name='iv_dek',
            field=models.BinaryField(default=b'\xb6q(\x04\x85`\xa3\x93I\x98\x96\xcd\xf7:\x8d\xf6'),
        ),
        migrations.AlterField(
            model_name='encrypt',
            name='iv_kek',
            field=models.BinaryField(default=b'\x94t)\xd2\x13l\x96\x03\x83\x93s\x8c\xb8\xc29+'),
        ),
        migrations.AlterField(
            model_name='encrypt',
            name='salt_kek',
            field=models.BinaryField(default=b"\x86t&\x8c\x92`'\xd2"),
        ),
    ]

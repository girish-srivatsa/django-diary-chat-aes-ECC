# Generated by Django 3.1.1 on 2020-09-14 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_auto_20200914_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatencrypt',
            name='iv_kek',
            field=models.BinaryField(default=b'\xfc\xb4\xf9`"\xf1\xfdTN)\x9b@9\xe6O\xde'),
        ),
        migrations.AlterField(
            model_name='chatencrypt',
            name='salt_kek',
            field=models.BinaryField(default=b'\xff\xfa\\\x12\xecD\xcct'),
        ),
        migrations.AlterField(
            model_name='encrypt',
            name='iv_dek',
            field=models.BinaryField(default=b'p\xef\xbc\xa4\x0e\x94)\x89\x03M0h \xe9=n'),
        ),
        migrations.AlterField(
            model_name='encrypt',
            name='iv_kek',
            field=models.BinaryField(default=b'a\xe4\xb0\x14y\xdbZ\xafN0\x03\xbfh\xcb\xceR'),
        ),
        migrations.AlterField(
            model_name='encrypt',
            name='salt_kek',
            field=models.BinaryField(default=b'$z\x03R%@\xa8.'),
        ),
    ]

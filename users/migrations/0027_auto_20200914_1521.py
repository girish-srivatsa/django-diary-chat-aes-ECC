# Generated by Django 3.1.1 on 2020-09-14 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_auto_20200914_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatencrypt',
            name='iv_kek',
            field=models.BinaryField(default=b'^\x8dv\x1a\xcaq24\xe0\xd4\xe3\xcad\x9c\xc1='),
        ),
        migrations.AlterField(
            model_name='chatencrypt',
            name='salt_kek',
            field=models.BinaryField(default=b'\xd3\x81\xe6\xa5\xc1\x86]\xe0'),
        ),
        migrations.AlterField(
            model_name='encrypt',
            name='iv_dek',
            field=models.BinaryField(default=b'\n\xd5\x166\xcda\x10\xf1\xb5kF6\x8em\x0c\xac'),
        ),
        migrations.AlterField(
            model_name='encrypt',
            name='iv_kek',
            field=models.BinaryField(default=b'\xde\xa5\xc5\x87w]\xf5>\xd1\x89p\xc5\xaf\xbc\x8f1'),
        ),
        migrations.AlterField(
            model_name='encrypt',
            name='salt_kek',
            field=models.BinaryField(default=b'$\xc8\xd5\x9e:~\xf1\xef'),
        ),
    ]

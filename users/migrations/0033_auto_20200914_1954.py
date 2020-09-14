# Generated by Django 3.1.1 on 2020-09-14 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_auto_20200914_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatencrypt',
            name='iv_kek',
            field=models.BinaryField(default=b'\xba9\xc07\xe4\re\x82a\x83}#5\xfbW\xcd'),
        ),
        migrations.AlterField(
            model_name='chatencrypt',
            name='public_x',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='chatencrypt',
            name='public_y',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='chatencrypt',
            name='salt_kek',
            field=models.BinaryField(default=b"\x16:5M\x9f'\xa8\x93"),
        ),
        migrations.AlterField(
            model_name='encrypt',
            name='iv_dek',
            field=models.BinaryField(default=b',vy\xf6\x92\x0c\x98\x97\xda\xb2~\x0f\xd3\xf7\x13\xa1'),
        ),
        migrations.AlterField(
            model_name='encrypt',
            name='iv_kek',
            field=models.BinaryField(default=b'\x82\xaf\xc6*\xcb\xd5\xc5\xb6Up\x12\x08\xab)1\xe9'),
        ),
        migrations.AlterField(
            model_name='encrypt',
            name='salt_kek',
            field=models.BinaryField(default=b'\xe4L@\xf9\xdeC\xbc@'),
        ),
    ]

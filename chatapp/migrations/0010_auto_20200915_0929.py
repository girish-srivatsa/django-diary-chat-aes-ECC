# Generated by Django 3.1.1 on 2020-09-15 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0009_chatp2p_iv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatp2p',
            name='iv',
            field=models.BinaryField(default=b'\xab\xf1\xe9A@\xfe\x1c\x0f\xd0\xbbKd\xcb\x9b\x9e,'),
        ),
    ]

# Generated by Django 3.1.1 on 2020-09-14 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0008_remove_chatmessage_message2'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatp2p',
            name='iv',
            field=models.BinaryField(default=b'\xf8\x97\xea\xab\x88\xee\x16\x15\xc1Y\xa7_\x81\xddj4'),
        ),
    ]

# Generated by Django 3.1.1 on 2020-09-14 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0005_auto_20200914_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatp2p',
            name='creator',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

# Generated by Django 3.1.2 on 2021-01-24 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aut', '0002_auto_20210124_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testrun_schritt',
            name='schritt_erwartetesergebnis',
            field=models.CharField(default=('f', 'fail'), max_length=128, null=True),
        ),
    ]

# Generated by Django 2.1.3 on 2018-11-30 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0005_auto_20181130_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='full_name',
            field=models.CharField(max_length=128, unique=True, verbose_name='surname, name, fathers'),
        ),
    ]
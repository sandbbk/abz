# Generated by Django 2.1.3 on 2018-11-30 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0002_auto_20181130_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='photo',
            field=models.ImageField(blank=True, help_text='jpg/png - file', upload_to='', verbose_name='Photo'),
        ),
    ]

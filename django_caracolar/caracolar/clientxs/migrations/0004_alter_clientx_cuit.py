# Generated by Django 3.2 on 2022-06-08 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientxs', '0003_alter_clientx_cuit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientx',
            name='cuit',
            field=models.CharField(default=1, max_length=11, unique=True, verbose_name='Cuit/Cuil'),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.2 on 2022-06-15 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0014_auto_20220615_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudcuidados',
            name='tipo',
            field=models.CharField(max_length=17, verbose_name='Tipo de servico'),
        ),
    ]

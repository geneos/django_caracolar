# Generated by Django 3.2 on 2022-07-04 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0022_auto_20220704_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudcuidados',
            name='tipo',
            field=models.CharField(default='Recurrente', editable=False, max_length=17, verbose_name='Tipo de servico'),
        ),
    ]

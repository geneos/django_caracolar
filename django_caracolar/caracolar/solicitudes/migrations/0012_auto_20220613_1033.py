# Generated by Django 3.2 on 2022-06-13 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0011_remove_solicitudcuidados_recurrencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudCuidadosProxy',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Solicitud de cuidados por fecha',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('solicitudes.solicitudcuidados',),
        ),
        migrations.AlterField(
            model_name='solicitudcuidados',
            name='tipo',
            field=models.IntegerField(choices=[(1, 'Recurrente'), (2, 'Porfecha')], default=1, verbose_name='Tipo de servico'),
        ),
    ]

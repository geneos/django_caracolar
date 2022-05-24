# Generated by Django 4.0.2 on 2022-04-13 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coops', '0003_asociadx_caracteristica_and_more'),
        ('clientxs', '0001_initial'),
        ('param', '0003_mediopago'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudCuidados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('recurrencia', models.BooleanField()),
                ('costo', models.FloatField()),
                ('montoPagado', models.FloatField()),
                ('estado', models.CharField(max_length=1)),
                ('clientx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientxs.clientx')),
                ('cooperativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.cooperativa')),
                ('medioPago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='param.mediopago')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.serviciocuidado')),
            ],
            options={
                'verbose_name_plural': 'Solicitudes de Cuidado',
            },
        ),
        migrations.CreateModel(
            name='SolicitudCuidadosRecurrencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(max_length=1)),
                ('horaInicio', models.TimeField()),
                ('horaFin', models.TimeField()),
                ('tiempo', models.IntegerField()),
                ('cooperativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.cooperativa')),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitudes.solicitudcuidados')),
            ],
            options={
                'verbose_name_plural': 'Recurrencia Solicitudes de Cuidado',
            },
        ),
        migrations.CreateModel(
            name='SolicitudCuidadosFechas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('horaInicio', models.TimeField()),
                ('horaFin', models.TimeField()),
                ('tiempo', models.IntegerField()),
                ('cooperativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.cooperativa')),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitudes.solicitudcuidados')),
            ],
            options={
                'verbose_name_plural': 'Fechas Solicitudes de Cuidado',
            },
        ),
        migrations.CreateModel(
            name='SolicitudCuidadosAsignacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asociadx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.asociadx')),
                ('cooperativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.cooperativa')),
                ('solicitudCuidados', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitudes.solicitudcuidados')),
            ],
            options={
                'verbose_name_plural': 'Asignación de Solicitudes',
            },
        ),
    ]
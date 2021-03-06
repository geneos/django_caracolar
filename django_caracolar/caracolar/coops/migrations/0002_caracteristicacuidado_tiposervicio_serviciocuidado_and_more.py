# Generated by Django 4.0.2 on 2022-04-13 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaracteristicaCuidado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
                ('descripcion', models.CharField(max_length=200, unique=True)),
                ('icono', models.CharField(max_length=200, unique=True)),
                ('cooperativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.cooperativa')),
            ],
            options={
                'verbose_name_plural': 'Configuración - Características de Cuidado',
            },
        ),
        migrations.CreateModel(
            name='TipoServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
                ('descripcion', models.CharField(max_length=200, unique=True)),
                ('icono', models.CharField(max_length=200, unique=True)),
                ('cooperativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.cooperativa')),
            ],
            options={
                'verbose_name_plural': 'Configuración - Tipos de Servicios',
            },
        ),
        migrations.CreateModel(
            name='ServicioCuidado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
                ('descripcion', models.CharField(max_length=200, unique=True)),
                ('icono', models.CharField(max_length=200, unique=True)),
                ('costoReferencia', models.FloatField()),
                ('cooperativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.cooperativa')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.tiposervicio')),
            ],
            options={
                'verbose_name_plural': 'Cooperativa - Servicios de Cuidado',
            },
        ),
        migrations.CreateModel(
            name='ServicioCaracteristicaCuidado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caracteristica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.caracteristicacuidado')),
                ('cooperativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.cooperativa')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.serviciocuidado')),
            ],
            options={
                'verbose_name_plural': 'Cooperativa - Características de Servicios de Cuidado',
            },
        ),
    ]

# Generated by Django 4.0.2 on 2022-04-13 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('param', '0002_alter_ciudad_options_alter_pais_options_and_more'),
        ('coops', '0002_caracteristicacuidado_tiposervicio_serviciocuidado_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asociadx',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('apellido', models.CharField(max_length=200)),
                ('cuit', models.CharField(max_length=11, unique=True)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=100)),
                ('ingreso', models.DateField()),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='param.ciudad')),
                ('cooperativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.cooperativa')),
            ],
            options={
                'verbose_name_plural': 'Asociadxs',
            },
        ),
        migrations.CreateModel(
            name='Caracteristica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
                ('cooperativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.cooperativa')),
            ],
            options={
                'verbose_name_plural': 'Características de Asociadx',
            },
        ),
        migrations.AlterModelOptions(
            name='caracteristicacuidado',
            options={'verbose_name_plural': 'Características de Cuidado'},
        ),
        migrations.AlterModelOptions(
            name='serviciocaracteristicacuidado',
            options={'verbose_name_plural': 'Características de Servicios de Cuidado'},
        ),
        migrations.AlterModelOptions(
            name='serviciocuidado',
            options={'verbose_name_plural': 'Servicios de Cuidado'},
        ),
        migrations.AlterModelOptions(
            name='tiposervicio',
            options={'verbose_name_plural': 'Tipos de Servicios'},
        ),
        migrations.CreateModel(
            name='CaracteristicaAsociadxs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asociadx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.asociadx')),
                ('caracteristica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.caracteristica')),
                ('cooperativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.cooperativa')),
            ],
            options={
                'verbose_name_plural': 'Asignación de Características de Asociadx',
            },
        ),
    ]

# Generated by Django 4.0.2 on 2022-04-13 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coops', '0003_asociadx_caracteristica_and_more'),
        ('param', '0002_alter_ciudad_options_alter_pais_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clientx',
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
                ('usuarix', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Clientxs',
            },
        ),
        migrations.CreateModel(
            name='CaracteristicaClientx',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caracteristica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.caracteristica')),
                ('clientx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientxs.clientx')),
                ('cooperativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coops.cooperativa')),
            ],
            options={
                'verbose_name_plural': 'Características de Clientxs',
            },
        ),
    ]
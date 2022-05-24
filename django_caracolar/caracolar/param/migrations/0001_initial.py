# Generated by Django 4.0.3 on 2022-04-13 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Configuración - Paises',
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='param.pais')),
            ],
            options={
                'verbose_name_plural': 'Configuración - Provincias',
            },
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='param.provincia')),
            ],
            options={
                'verbose_name_plural': 'Configuración - Ciudades',
            },
        ),
    ]

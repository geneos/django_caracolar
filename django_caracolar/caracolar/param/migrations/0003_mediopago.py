# Generated by Django 4.0.2 on 2022-04-13 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('param', '0002_alter_ciudad_options_alter_pais_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedioPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Medios de Pago',
            },
        ),
    ]

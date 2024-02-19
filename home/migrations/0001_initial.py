# Generated by Django 5.0.2 on 2024-02-17 21:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EncuestaEconomica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_encuesta', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('fecha', models.DateField()),
                ('encuestador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'encuesta',
            },
        ),
        migrations.CreateModel(
            name='GrupoPoblacional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.encuestaeconomica')),
            ],
        ),
        migrations.CreateModel(
            name='Apartado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.grupopoblacional')),
            ],
        ),
        migrations.CreateModel(
            name='PreguntaAntropometria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('grupo_poblacional', models.CharField(max_length=60)),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.encuestaeconomica')),
            ],
        ),
        migrations.CreateModel(
            name='PreguntaEconomica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('apartado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.apartado')),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.encuestaeconomica')),
            ],
        ),
        migrations.CreateModel(
            name='PreguntaRespuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('response', models.CharField(max_length=200)),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pregunta_respuesta', to='home.encuesta')),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaEconomica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=200)),
                ('valor', models.IntegerField()),
                ('predefinido', models.BooleanField(default=False)),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.preguntaeconomica')),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaNumerica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta_numerica', models.IntegerField()),
                ('sesion_encuesta', models.CharField(blank=True, max_length=64, null=True)),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.encuestaeconomica')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.preguntaantropometria')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sesion_encuesta', models.CharField(blank=True, max_length=64, null=True)),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.encuestaeconomica')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.preguntaeconomica')),
                ('respuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.respuestaeconomica')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
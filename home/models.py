from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.




class UserActivation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_activated = models.BooleanField(default=False)
    created_through_api = models.BooleanField(default=False)

class EncuestaEconomica(models.Model):
    nombre = models.CharField(max_length=200)


class GrupoPoblacional(models.Model):
    encuesta = models.ForeignKey(EncuestaEconomica, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)


class Apartado(models.Model):
    grupo = models.ForeignKey(GrupoPoblacional, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)


class PreguntaEconomica(models.Model):
    apartado = models.ForeignKey(Apartado, on_delete=models.CASCADE, null=True)
    encuesta = models.ForeignKey(EncuestaEconomica, on_delete=models.CASCADE)
    texto = models.TextField()


class RespuestaEconomica(models.Model):
    pregunta = models.ForeignKey(PreguntaEconomica, on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)
    valor = models.IntegerField()
    predefinido = models.BooleanField(default=False)


class RespuestaUsuario(models.Model):
    encuesta = models.ForeignKey(EncuestaEconomica, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(PreguntaEconomica, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(RespuestaEconomica, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    sesion_encuesta = models.CharField(max_length=64, blank=True, null=True)


class PreguntaAntropometria(models.Model):
    encuesta = models.ForeignKey(EncuestaEconomica, on_delete=models.CASCADE)
    texto = models.TextField()
    grupo_poblacional = models.CharField(max_length=60)  # campo para el grupo poblacional


class RespuestaNumerica(models.Model):
    encuesta = models.ForeignKey(EncuestaEconomica, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(PreguntaAntropometria, on_delete=models.CASCADE)
    respuesta_numerica = models.IntegerField()  # respuesta como número del 0 a 255
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    sesion_encuesta = models.CharField(max_length=64, blank=True, null=True)



class Encuesta(models.Model):
    id_encuesta = models.IntegerField(blank=False, null=False)
    encuestador = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    fecha = models.DateField()
    # Agrega tus otros campos aquí

    class Meta:
        db_table = 'encuesta'

class PreguntaRespuesta(models.Model):
    encuesta = models.ForeignKey(Encuesta, related_name='pregunta_respuesta', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    response = models.CharField(max_length=200)
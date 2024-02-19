from django.contrib.auth.models import User
from rest_framework import serializers
from home.models import Encuesta, PreguntaRespuesta, RespuestaUsuario
from datetime import datetime

class PreguntaRespuestaSerializer(serializers.Serializer):
    response = serializers.CharField()
    text = serializers.CharField()


class EncuestaSerializer(serializers.Serializer):
    encuestador = serializers.IntegerField()
    fecha = serializers.DateField(input_formats=['%d-%m-%Y',])
    id = serializers.IntegerField()
    name = serializers.CharField()
    questionResponse = PreguntaRespuestaSerializer(many=True)

    def create(self, validated_data):
        questionResponses = validated_data.pop('questionResponse')
        user_id = validated_data.pop('encuestador')
        user = User.objects.get(id=user_id)
        id_encuesta = validated_data.pop('id')
        encuesta = Encuesta.objects.create(encuestador=user,id_encuesta=id_encuesta, **validated_data)
        for qr_data in questionResponses:
            PreguntaRespuesta.objects.create(encuesta=encuesta, **qr_data)
        return encuesta

class EncuestaListSerializer(serializers.Serializer):
    data = EncuestaSerializer(many=True)

    def create(self, validated_data):
        data_items = validated_data.pop('data')

        results = []
        for d in data_items:
            encuesta_serializer = EncuestaSerializer(data=d)
            if encuesta_serializer.is_valid():
                encuesta = encuesta_serializer.save()   # Este es el objeto encuesta
                questionResponses = [{'text': qr.text, 'response': qr.response} for qr in encuesta.pregunta_respuesta.all()]
                results.append({
                    "encuestador": encuesta.encuestador.id,
                    "fecha": encuesta.fecha,
                    "id": encuesta.id_encuesta,
                    "name": encuesta.name,
                    "questionResponse": questionResponses
                })
            else:
                raise serializers.ValidationError(encuesta_serializer.errors)

        return {"data": results}  # Retorna la lista de encuestas creadas

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
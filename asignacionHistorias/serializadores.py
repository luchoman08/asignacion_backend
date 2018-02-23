from rest_framework import serializers
from modelosGenericos import models as modelos_genericos
class HistoriaSerializador(serializers.ModelSerializer):
    class Meta:
        model = modelos_genericos.Historia
        fields = ('nombre', 'proyecto', 'descripcion', 'puntuacionGeneral')

class DesarrolladorSerializador(serializers.ModelSerializer):
    class Meta:
        model = modelos_genericos.Desarrollador
        fields = ('nombre', 'horasDisponiblesSemana')

class ProyectoAgilSerializador(serializers.ModelSerializer):
    class Meta:
        model = modelos_genericos.ProyectoAgil
        fields = ('nombre', 'fechaInicio', 'fechaFinalizacion', "correspondenciaPuntosHoras")
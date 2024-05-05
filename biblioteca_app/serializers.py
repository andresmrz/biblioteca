from rest_framework import serializers
from .models import Libro, Usuario

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'año_publicacion', 'cantidad_en_stock']

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'correo_electronico', 'rol']

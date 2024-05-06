from rest_framework import serializers
from .models import Libro, Usuario, Prestamo

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'año_publicacion', 'cantidad_en_stock']

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'correo_electronico', 'rol']

class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = ['usuario', 'libro', 'fecha_entrega', 'fecha_devolucion_esperada', 'fecha_devolucion']
        read_only_fields = ['id', 'usuario', 'fecha_entrega', 'fecha_devolucion']

    def validate_fecha_devolucion_esperada(self, value):
        
        return value


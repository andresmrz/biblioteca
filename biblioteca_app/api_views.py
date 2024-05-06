from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsAdminUser
from .models import Libro, Prestamo
from .serializers import LibroSerializer, PrestamoSerializer
from django.utils import timezone

class LibroApiList(generics.ListAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [permissions.AllowAny]

class LibroApiDetail(generics.RetrieveAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [permissions.AllowAny]

class LibroApiCreate(generics.CreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAdminUser]

class LibroApiUpdate(generics.UpdateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAdminUser]

class LibroApiDelete(generics.DestroyAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAdminUser]

class PrestamoApi(generics.CreateAPIView):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        libro_id = self.kwargs.get('pk')  # Obtiene el ID del libro desde la URL
        libro = get_object_or_404(Libro, pk=libro_id)
        usuario = self.request.user

        # Verifica si ya existe un préstamo activo para el mismo libro y usuario
        if Prestamo.objects.filter(libro=libro, usuario=usuario, fecha_devolucion__isnull=True).exists():
            raise ValidationError({'error': 'Ya tienes un préstamo activo para este libro.'})

        # Verifica el stock antes de proceder
        if libro.cantidad_en_stock > 0:
            libro.cantidad_en_stock -= 1  # Reduce el stock
            libro.save()
            serializer.save(usuario=usuario, libro=libro)
        else:
            raise ValidationError({'error': 'Este libro no está disponible para préstamo.'})
    
class DevolverPrestamoApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        prestamo = get_object_or_404(Prestamo, pk=pk)
        
        # Verifica si el préstamo ya fue devuelto
        if prestamo.fecha_devolucion:
            return Response({'error': 'Este libro ya ha sido devuelto.'}, status=status.HTTP_400_BAD_REQUEST)

        prestamo.fecha_devolucion = timezone.now().date()  # Asume que solo necesitas la fecha
        prestamo.libro.cantidad_en_stock += 1
        prestamo.libro.save()
        prestamo.save()

        return Response({'message': 'Libro devuelto con éxito.'}, status=status.HTTP_200_OK)


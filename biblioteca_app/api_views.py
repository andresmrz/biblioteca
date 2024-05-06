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
    """
    API para listar todos los libros disponibles en la biblioteca.

    Esta API permite obtener una lista de todos los libros disponibles, accesible para cualquier usuario.

    Métodos:
        - GET: Devuelve una lista de todos los libros disponibles.

    Devuelve:
        Una respuesta JSON con una lista de libros.

    Ejemplo de Respuesta:
    {
        "libros": [
            {"id": 1, "titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", ...},
            ...
        ]
    }
    """
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [permissions.AllowAny]

class LibroApiDetail(generics.RetrieveAPIView):
    """
    API para obtener los detalles de un libro específico.

    Este endpoint proporciona información detallada sobre un libro en particular, accesible para cualquier usuario.

    Métodos:
        - GET: Recupera los detalles de un libro específico por su ID.

    Parámetros:
        - id (int): El identificador único del libro.

    Devuelve:
        Una respuesta JSON con los detalles completos del libro solicitado.

    Ejemplo de Respuesta:
    {
        "libro": {
            "id": 1,
            "titulo": "Cien años de soledad",
            "autor": "Gabriel García Márquez",
            "año_publicacion": "1981-05-20",
            "cantidad_en_stock": 20
        }
    }
    """
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [permissions.AllowAny]

class LibroApiCreate(generics.CreateAPIView):
    """
    API para crear un nuevo libro en la biblioteca.

    Este endpoint permite a los usuarios administradores agregar un nuevo libro al sistema.

    Métodos:
        - POST: Crea un nuevo libro en la base de datos.

    Parámetros de la solicitud:
        - título (str): El título del libro.
        - autor (str): El autor del libro.
        - año_publicacion (str): Año de publicación del libro.
        - cantidad_en_stock (int): La cantidad de libros disponibles en el stock.

    Devuelve:
        Una respuesta JSON con los detalles del libro creado.

    Ejemplo de Respuesta:
    {
        "libro": {
            "id": 25,
            "titulo": "El Aleph",
            "autor": "Jorge Luis Borges",
            "año_publicacion": "1981-05-20",
            "cantidad_en_stock": 5
        }
    }

    Nota:
    - Solo usuarios con el rol de 'administrador' pueden acceder a este endpoint.
    - La solicitud debe incluir todos los campos requeridos para la creación del libro.
    """
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAdminUser]

class LibroApiUpdate(generics.UpdateAPIView):
    """
    API para actualizar la información de un libro existente.

    Este endpoint permite a los administradores modificar los detalles de un libro. Solo accesible para usuarios con el rol de administrador.

    Métodos:
        - PUT/PATCH: Actualiza la información del libro especificado por su ID.

    Parámetros:
        - id (int): El ID del libro a actualizar.

    Devuelve:
        Una respuesta JSON con los detalles actualizados del libro.

    Ejemplo de Respuesta:
    {
        "libro": {
            "id": 1,
            "titulo": "Cien años de soledad editado",
            "autor": "Gabriel García Márquez",
            "año_publicacion": "1981-05-20",
            "cantidad_en_stock": 25
        }
    }

    Nota:
    - Solo los administradores pueden realizar actualizaciones.
    """
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAdminUser]

class LibroApiDelete(generics.DestroyAPIView):
    """
    API para eliminar un libro del sistema.

    Este endpoint permite a los administradores eliminar un libro por su ID. Accesible solo para usuarios con el rol de administrador.

    Métodos:
        - DELETE: Elimina el libro especificado.

    Parámetros:
        - id (int): El ID del libro a eliminar.

    Devuelve:
        Una respuesta JSON indicando el éxito de la operación.

    Ejemplo de Respuesta:
    {
        "message": "Libro eliminado con éxito."
    }

    Nota:
    - Esta acción es irreversible y requiere privilegios de administrador.
    """
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAdminUser]

class PrestamoApi(generics.CreateAPIView):
    """
    API para crear un nuevo préstamo de un libro.

    Este endpoint permite a los usuarios registrados realizar un préstamo de un libro, verificando la disponibilidad y el estado actual del inventario.

    Métodos:
        - POST: Registra un nuevo préstamo para el libro especificado.

    Parámetros:
        - libro_id (int): El ID del libro que se presta.
        - usuario_id (int): El ID del usuario que realiza el préstamo.

    Devuelve:
        Una respuesta JSON con los detalles del préstamo realizado.

    Ejemplo de Respuesta:
    {
        "prestamo": {
            "id": 10,
            "libro_id": 1,
            "usuario_id": 2,
            "fecha_prestamo": "2024-01-01",
            "fecha_devolucion": null
        }
    }

    Nota:
    - Verifica la disponibilidad del libro antes de completar el préstamo.
    - El préstamo se puede realizar solo si el libro está en stock.
    """
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
    """
    API para registrar la devolución de un libro prestado.

    Este endpoint permite a los usuarios autenticados marcar un libro como devuelto. Aumenta el stock del libro
    y registra la fecha de devolución.

    Métodos:
        - PATCH: Actualiza el estado del préstamo a devuelto.

    Parámetros:
        - pk (int): El ID del préstamo que se está devolviendo.

    Devuelve:
        Una respuesta JSON que indica el éxito de la operación.

    Ejemplo de Respuesta:
    {
        "message": "Libro devuelto con éxito."
    }

    Nota:
    - Este endpoint requiere que el usuario esté autenticado.
    - El préstamo debe existir y no debe haber sido devuelto previamente.
    """
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


from rest_framework import viewsets
from .models import Libro
from .serializers import LibroSerializer
from .permissions import IsAdminUser, IsRegularUser

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:  # Para acciones como create, update, delete
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class PrestarDevolverViewSet(viewsets.ViewSet):
    # lógica para prestar y devolver libros
    permission_classes = [IsRegularUser]

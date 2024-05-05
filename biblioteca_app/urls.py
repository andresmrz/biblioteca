
from django.urls import path
from .views import ListaLibrosView, DetalleLibroView, CrearLibroView, CrearEditarLibroView, PrestarDevolverLibroView, ListaLibrosPrestadosView

urlpatterns = [
    path('libros/', ListaLibrosView.as_view(), name='lista_libros'),
    path('libros/<int:pk>/', DetalleLibroView.as_view(), name='detalles_libro'),
    path('libros/crear/', CrearLibroView.as_view(), name='crear_libro'),
    path('libros/<int:pk>/editar/', CrearEditarLibroView.as_view(), name='editar_libro'),
    path('libros/prestamo/', PrestarDevolverLibroView.as_view(), name='tomar_devolver_libro'),
    path('libros/prestados/', ListaLibrosPrestadosView.as_view(), name='lista_libros_prestados'),
]

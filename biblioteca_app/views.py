from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Libro, Usuario, Prestamo
from .forms import LibroForm, PrestamoForm

class ListaLibrosView(ListView):
    model = Libro
    template_name = 'libros/lista_libros.html'
    context_object_name = 'libros' 
    paginate_by = 8

class DetalleLibroView(DetailView):
    model = Libro
    template_name = 'libros/detalles_libro.html'

class CrearLibroView(UserPassesTestMixin, CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libros/crear_libro.html'
    success_url = reverse_lazy('lista_libros')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'administrador'
    
class EditarLibroView(UserPassesTestMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libros/editar_libro.html'
    success_url = reverse_lazy('lista_libros')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'administrador'

class PrestarLibroView(DetailView):
    model = Libro
    template_name = 'libros/prestar_libro.html'
    context_object_name = 'libro'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'usuario_regular'

class ListaLibrosPrestadosView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'libros/lista_libros_prestados.html' 

    def get_queryset(self):
        return self.request.user.libros_prestados.all()

class HistorialLibroView(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name = 'libros/historial_libro.html'
    context_object_name = 'prestamos'

    def get_queryset(self):
        # Filtrar los préstamos por el usuario actual
        return Prestamo.objects.filter(usuario=self.request.user).select_related('libro')

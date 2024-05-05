from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Libro, Usuario
from .forms import LibroForm

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

class PrestarDevolverLibroView(LoginRequiredMixin, View):
    model = Usuario
    fields = ['libros_prestados']
    template_name = 'prestar_devolver_libro.html'

class ListaLibrosPrestadosView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'libros/lista_libros_prestados.html' 

    def get_queryset(self):
        return self.request.user.libros_prestados.all()

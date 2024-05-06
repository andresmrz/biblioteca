from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Libro, Usuario, Prestamo
from django.contrib.auth import login
from .forms import LibroForm, PrestamoForm, RegisterForm

class indexView(TemplateView):
    """
    Vista basada en plantilla para mostrar la página principal.
    """
    template_name = 'index.html'

class ListaLibrosView(ListView):
    """
    Vista para listar los libros disponibles. Utiliza paginación para manejar grandes cantidades de datos.
    """
    model = Libro
    template_name = 'libros/lista_libros.html'
    context_object_name = 'libros' 
    paginate_by = 8

class DetalleLibroView(DetailView):
    """
    Vista detallada de un libro específico. Muestra información más detallada sobre un libro seleccionado.
    """
    model = Libro
    template_name = 'libros/detalles_libro.html'

class CrearLibroView(UserPassesTestMixin, CreateView):
    """
    Restricción de acceso a la vista: solo usuarios autenticados con rol 'administrador' pueden acceder.
    """
    model = Libro
    form_class = LibroForm
    template_name = 'libros/crear_libro.html'
    success_url = reverse_lazy('lista_libros')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'administrador'
    
class EditarLibroView(UserPassesTestMixin, UpdateView):
    """
    Vista para editar un libro existente. Protegida para asegurar que solo administradores puedan modificar libros.
    """
    model = Libro
    form_class = LibroForm
    template_name = 'libros/editar_libro.html'
    success_url = reverse_lazy('lista_libros')

    def test_func(self):
        """
        Verifica que el usuario sea administrador antes de permitir el acceso a la función de edición.
        """
        return self.request.user.is_authenticated and self.request.user.rol == 'administrador'

class PrestarLibroView(DetailView):
    """
    Vista para mostrar la página de préstamo de un libro. Restringida a usuarios regulares.
    """
    model = Libro
    template_name = 'libros/prestar_libro.html'
    context_object_name = 'libro'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'usuario_regular'

class ListaLibrosPrestadosView(LoginRequiredMixin, ListView):
    """
    Vista que muestra una lista de libros actualmente prestados al usuario logueado.
    """
    model = Usuario
    template_name = 'libros/lista_libros_prestados.html' 

    def get_queryset(self):
        """
        Personaliza el queryset para retornar solo los libros prestados al usuario actual.
        """
        return self.request.user.libros_prestados.all()

class HistorialLibroView(LoginRequiredMixin, ListView):
    """
    Vista que muestra el historial de todos los préstamos hechos por el usuario.
    """
    model = Prestamo
    template_name = 'libros/historial_libro.html'
    context_object_name = 'prestamos'

    def get_queryset(self):
        """
        Filtra los préstamos por el usuario logueado y realiza un 'join' con la tabla de libros para eficiencia.
        """
        return Prestamo.objects.filter(usuario=self.request.user).select_related('libro')

def register(request):
    """
    Maneja el registro de nuevos usuarios. Si el formulario es válido, registra y loguea al usuario.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # loguea al usuario automáticamente después del registro
            return redirect('index')  # Redirige a la página de inicio después del registro
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


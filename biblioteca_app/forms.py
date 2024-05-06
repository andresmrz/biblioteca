from django import forms
from .models import Libro, Prestamo

class LibroForm(forms.ModelForm):
    titulo = forms.CharField(label='Título', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    autor = forms.CharField(label='Autor', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    año_publicacion = forms.IntegerField(label='Año de Publicación', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cantidad_en_stock = forms.IntegerField(label='Cantidad en Stock', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'año_publicacion', 'cantidad_en_stock']

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libro', 'fecha_devolucion_esperada']
        widgets = {
            'fecha_devolucion_esperada': forms.DateInput(attrs={'type': 'date'})
        }
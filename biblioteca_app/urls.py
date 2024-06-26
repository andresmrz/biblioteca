
from django.urls import path
from .views import ListaLibrosView, DetalleLibroView, CrearLibroView, EditarLibroView, PrestarLibroView, HistorialLibroView, indexView, register
from .api_views import LibroApiList, LibroApiDetail, LibroApiCreate, LibroApiUpdate, LibroApiDelete, PrestamoApi, DevolverPrestamoApi
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', indexView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('libros/', ListaLibrosView.as_view(), name='lista_libros'),
    path('libros/<int:pk>/', DetalleLibroView.as_view(), name='detalles_libro'),
    path('libros/crear/', CrearLibroView.as_view(), name='crear_libro'),
    path('libros/editar/<int:pk>/', EditarLibroView.as_view(), name='editar_libro'),
    path('libros/prestar/<int:pk>/', PrestarLibroView.as_view(), name='prestar_libro'),
    path('libros/historial/', HistorialLibroView.as_view(), name='historial_libro'),
    
    # Apis
    path('api/libros/', LibroApiList.as_view(), name='libro_api_list'),
    path('api/libros/<int:pk>/', LibroApiDetail.as_view(), name='libro_api_detail'),
    path('api/libros/crear/', LibroApiCreate.as_view(), name='libro_api_create'),
    path('api/libros/editar/<int:pk>/', LibroApiUpdate.as_view(), name='libro_api_update'),
    path('api/libros/eliminar/<int:pk>/', LibroApiDelete.as_view(), name='libro_api_delete'),
    path('api/libros/prestar/<int:pk>/', PrestamoApi.as_view(), name='libro_api_prestar'),
    path('api/libros/devolver/<int:pk>/', DevolverPrestamoApi.as_view(), name='libro_api_devolver'),
]

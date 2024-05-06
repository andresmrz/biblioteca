# Biblioteca en Django

Este es un proyecto de una biblioteca desarrollado en Django.

## Descripción del proyecto

La aplicación de la biblioteca tiene como objetivo proporcionar un sistema de gestión para libros y usuarios. Los principales componentes del proyecto son:

### Modelos

1. **Libro**: Cada libro tiene un título, autor, año de publicación y cantidad en stock.
2. **Usuario**: Cada usuario tiene un nombre, correo electrónico, una lista de libros que ha tomado prestados y un rol (que puede ser "usuario regular" o "administrador").

Se establece una relación de muchos a muchos entre Usuario y Libro para representar los libros que un usuario ha tomado prestados.

### Modos de funcionamiento

El proyecto cuenta con dos modos:

1. **Vistas**: Utiliza vistas para la interfaz de usuario.
2. **APIs**: Utiliza Django REST Framework para proporcionar una serie de APIs destinadas a ser consumidas externamente. Las APIs incluyen operaciones CRUD para libros (GET, POST, PUT), así como APIs para prestar y devolver libros.

### Tecnologías utilizadas

- Python Django 4.2.2
- Django REST Framework
- PostgreSQL (utilizando el servicio de Clever Cloud)
- Bootstrap
- Heroku
- GitHub

## Datos de acceso a la BD Postgrest

Host: bscuvdjg9ramzlycyqlg-postgresql.services.clever-cloud.com
Puerto: 50013
Nombre de Base de Datos: bscuvdjg9ramzlycyqlg
Usuario: u006yb63wrzvxvxg6h8k
Contraseña: MuVHk03wZyAdotxn50pPJLlqkq6kyf

## Instrucciones de instalación y ejecución

1. Clona este repositorio desde GitHub: 

git clone <https://github.com/andresmrz/biblioteca.git>

2. Crea un entorno virtual de Python para el proyecto:

python -m venv env

3. Activa el entorno virtual:

- En Windows:

  ```
  env\Scripts\activate
  ```

- En macOS y Linux:

  ```
  source env/bin/activate
  ```

4. Instala las dependencias del proyecto desde el archivo `requirements.txt`:

pip install -r requirements.txt

5. Ejecuta las migraciones para crear la estructura de la base de datos:

python manage.py migrate

6. Recopila los archivos estáticos:

python manage.py collectstatic

7. Inicia el servidor de desarrollo:

python manage.py runserver

8. Crear un super usuario

python manage.py createsuperuser

## Credenciales de Acceso en Producción

andresmauriciorz96@gmail.com
1234

# Documentación

El codigo se encuentra documentado en cada uno de sus metodos tanto de las apis como de las vistas. Con cada uno de sus parametros, su funcionamiento y lo que retorna.

Se añadio la libreria de Swagger para documentar las APIS, se pude acceder a ella atravez de:

- https://gestionbiblioteca-da0269634ede.herokuapp.com/swagger/
- https://gestionbiblioteca-da0269634ede.herokuapp.com/redoc/

Este proyecto fue creado por Andrés Mauricio Rodríguez como prueba tecnica para la empresa USEIT.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    año_publicacion = models.IntegerField()
    cantidad_en_stock = models.IntegerField()

    def __str__(self):
        return self.titulo

class UsuarioManager(BaseUserManager):
    def create_user(self, correo_electronico, nombre, password=None):
        if not correo_electronico:
            raise ValueError('Usuarios deben tener un correo electrónico')
        usuario = self.model(
            correo_electronico=self.normalize_email(correo_electronico),
            nombre=nombre
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo_electronico, nombre, password):
        usuario = self.create_user(
            correo_electronico,
            password=password,
            nombre=nombre
        )
        usuario.is_admin = True
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)

    libros_prestados = models.ManyToManyField('Libro', related_name='usuarios_prestados')

    ROL_CHOICES = (
        ('usuario regular', 'Usuario Regular'),
        ('administrador', 'Administrador'),
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='usuario_regular')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre']  # Agrega aquí los campos requeridos aparte del USERNAME_FIELD

    def __str__(self):
        return self.correo_electronico

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

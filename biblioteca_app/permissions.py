from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permite el acceso solo a los usuarios administradores.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'administrador'

class IsRegularUser(permissions.BasePermission):
    """
    Permite el acceso solo a los usuarios regulares.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'usuario_regular'

"""Clases para representar a los usuarios de la tienda."""

import uuid


class Usuario:
    """Clase padre de la que heredan Cliente y Administrador."""

    def __init__(self, nombre: str, email: str) -> None:
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.email: str = email

    def is_admin(self) -> bool:
        """Por defecto un usuario normal no tiene permisos de administrador."""
        return False

    def __str__(self) -> str:
        return f"[{self.id[:8]}] {self.nombre} ({self.email})"


class Cliente(Usuario):
    """Usuario que compra en la tienda; añade la direccion para los envios."""

    def __init__(self, nombre: str, email: str, direccion: str) -> None:
        super().__init__(nombre, email)
        self.direccion: str = direccion

    def __str__(self) -> str:
        return f"{super().__str__()} - Direccion: {self.direccion}"


class Administrador(Usuario):
    """Usuario gestor de la tienda, con permisos de administrador."""

    def is_admin(self) -> bool:
        return True

    def __str__(self) -> str:
        return f"{super().__str__()} - Rol: Administrador"

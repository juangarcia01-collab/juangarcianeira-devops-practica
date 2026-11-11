"""Clases para representar los productos de la tienda."""

import uuid


class Producto:
    """Clase padre de la que heredan todos los productos de la tienda."""

    def __init__(self, nombre: str, precio: float, stock: int) -> None:
        self.id: str = str(uuid.uuid4())  # id unico generado automaticamente
        self.nombre: str = nombre
        self.precio: float = precio
        self.stock: int = stock

    def hay_stock(self, cantidad: int) -> bool:
        """Devuelve True si hay unidades suficientes para servir la cantidad pedida."""
        return self.stock >= cantidad

    def actualizar_stock(self, cantidad: int) -> None:
        """Actualiza el stock. Un numero negativo descuenta (venta), uno positivo repone."""
        nuevo_stock = self.stock + cantidad
        if nuevo_stock < 0:
            raise ValueError(
                f"No hay stock suficiente de '{self.nombre}' "
                f"(disponibles: {self.stock}, pedidos: {-cantidad})"
            )
        self.stock = nuevo_stock

    def __str__(self) -> str:
        return f"[{self.id[:8]}] {self.nombre} - {self.precio:.2f}€ (stock: {self.stock})"


class ProductoElectronico(Producto):
    """Producto electronico: añade meses de garantia al producto base."""

    def __init__(self, nombre: str, precio: float, stock: int, meses_garantia: int) -> None:
        super().__init__(nombre, precio, stock)
        self.meses_garantia: int = meses_garantia

    def __str__(self) -> str:
        return f"{super().__str__()} - Garantia: {self.meses_garantia} meses"


class ProductoRopa(Producto):
    """Producto de ropa: añade talla y color al producto base."""

    def __init__(self, nombre: str, precio: float, stock: int, talla: str, color: str) -> None:
        super().__init__(nombre, precio, stock)
        self.talla: str = talla
        self.color: str = color

    def __str__(self) -> str:
        return f"{super().__str__()} - Talla: {self.talla}, Color: {self.color}"

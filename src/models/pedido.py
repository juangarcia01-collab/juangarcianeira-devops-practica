"""Clase Pedido: une un cliente con los productos que ha comprado."""

import uuid
from datetime import datetime
from typing import List, Tuple

from models.producto import Producto
from models.usuario import Cliente


class Pedido:
    """Representa un pedido de un cliente, con sus lineas de compra."""

    def __init__(self, cliente: Cliente, lineas: List[Tuple[Producto, int]]) -> None:
        self.id: str = str(uuid.uuid4())
        self.cliente: Cliente = cliente
        self.lineas: List[Tuple[Producto, int]] = lineas  # lista de (producto, cantidad)
        self.fecha: datetime = datetime.now()

    def calcular_total(self) -> float:
        """Suma precio * cantidad de todas las lineas del pedido."""
        return sum(producto.precio * cantidad for producto, cantidad in self.lineas)

    def __str__(self) -> str:
        fecha_str = self.fecha.strftime("%Y-%m-%d %H:%M")
        detalle = ", ".join(f"{cantidad}x {producto.nombre}" for producto, cantidad in self.lineas)
        return (
            f"Pedido [{self.id[:8]}] de {self.cliente.nombre} ({fecha_str}): "
            f"{detalle} - Total: {self.calcular_total():.2f}€"
        )

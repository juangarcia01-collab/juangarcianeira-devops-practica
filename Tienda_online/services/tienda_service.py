"""TiendaService: capa de servicios que centraliza toda la logica de la tienda."""

from typing import Dict, List, Optional, Tuple

from models.pedido import Pedido
from models.producto import Producto, ProductoElectronico, ProductoRopa
from models.usuario import Administrador, Cliente, Usuario


class TiendaService:
    """Actua como intermediario entre usuarios, productos y pedidos."""

    def __init__(self) -> None:
        self.usuarios: Dict[str, Usuario] = {}
        self.productos: Dict[str, Producto] = {}
        self.pedidos: List[Pedido] = []

    # --- usuarios ------------------------------------------------------

    def registrar_usuario(self, tipo: str, **kwargs) -> Usuario:
        """Crea un Cliente o un Administrador segun el tipo indicado."""
        tipo = tipo.strip().lower()
        if tipo == "cliente":
            usuario: Usuario = Cliente(**kwargs)
        elif tipo == "administrador":
            usuario = Administrador(**kwargs)
        else:
            raise ValueError(f"Tipo de usuario no reconocido: '{tipo}'")

        self.usuarios[usuario.id] = usuario
        return usuario

    def obtener_usuario(self, usuario_id: str) -> Optional[Usuario]:
        return self.usuarios.get(usuario_id)

    def listar_usuarios(self) -> List[Usuario]:
        return list(self.usuarios.values())

    # --- productos -------------------------------------------------------

    def anadir_producto(self, categoria: str, **kwargs) -> Producto:
        """Crea un producto (generico, electronico o ropa) y lo añade al inventario."""
        categoria = categoria.strip().lower()
        if categoria == "generico":
            producto: Producto = Producto(**kwargs)
        elif categoria == "electronico":
            producto = ProductoElectronico(**kwargs)
        elif categoria == "ropa":
            producto = ProductoRopa(**kwargs)
        else:
            raise ValueError(f"Categoria de producto no reconocida: '{categoria}'")

        self.productos[producto.id] = producto
        return producto

    def obtener_producto(self, producto_id: str) -> Optional[Producto]:
        return self.productos.get(producto_id)

    def eliminar_producto(self, producto_id: str) -> bool:
        """Elimina un producto del inventario. Devuelve False si no existia."""
        return self.productos.pop(producto_id, None) is not None

    def listar_productos(self) -> List[Producto]:
        return list(self.productos.values())

    # --- pedidos -----------------------------------------------------------

    def realizar_pedido(
        self, usuario_id: str, productos_cantidades: List[Tuple[str, int]]
    ) -> Optional[Pedido]:
        """Genera un pedido si el usuario existe, es cliente y hay stock suficiente."""
        usuario = self.usuarios.get(usuario_id)
        if usuario is None or not isinstance(usuario, Cliente):
            return None

        # primero comprobamos que todo el pedido se puede servir antes de tocar el stock
        lineas: List[Tuple[Producto, int]] = []
        for producto_id, cantidad in productos_cantidades:
            producto = self.productos.get(producto_id)
            if producto is None or not producto.hay_stock(cantidad):
                return None
            lineas.append((producto, cantidad))

        for producto, cantidad in lineas:
            producto.actualizar_stock(-cantidad)

        pedido = Pedido(cliente=usuario, lineas=lineas)
        self.pedidos.append(pedido)
        return pedido

    def listar_pedidos_usuario(self, usuario_id: str) -> List[Pedido]:
        """Devuelve los pedidos de un usuario ordenados por fecha."""
        pedidos_usuario = [p for p in self.pedidos if p.cliente.id == usuario_id]
        return sorted(pedidos_usuario, key=lambda p: p.fecha)

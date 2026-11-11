"""Esquemas Pydantic usados por la API para validar entrada y formatear salida."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# --- Usuarios -----------------------------------------------------------

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    tipo: str  # "cliente" o "administrador"
    direccion: Optional[str] = None  # solo se usa si tipo == "cliente"


class UsuarioRead(BaseModel):
    id: str
    nombre: str
    email: str
    es_admin: bool


# --- Productos ------------------------------------------------------------

class ProductoCreate(BaseModel):
    tipo: str  # "generico", "electronico" o "ropa"
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None  # solo si tipo == "electronico"
    talla: Optional[str] = None  # solo si tipo == "ropa"
    color: Optional[str] = None  # solo si tipo == "ropa"


class ProductoRead(BaseModel):
    id: str
    tipo: str
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None


# --- Pedidos ----------------------------------------------------------------

class PedidoItemCreate(BaseModel):
    producto_id: str
    cantidad: int


class PedidoCreate(BaseModel):
    cliente_id: str
    items: List[PedidoItemCreate]


class PedidoItemRead(BaseModel):
    producto_id: str
    nombre_producto: str
    cantidad: int
    subtotal: float


class PedidoRead(BaseModel):
    id: str
    fecha: datetime
    cliente_id: str
    total: float
    items: List[PedidoItemRead]

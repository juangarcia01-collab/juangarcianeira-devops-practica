"""API REST de la tienda online.

Expone la logica de TiendaService (clases de la Practica 1) a traves de FastAPI.
Ejecutar desde dentro de esta carpeta con: uvicorn main:app --reload
"""

from typing import List

from fastapi import FastAPI, HTTPException

from models.producto import Producto, ProductoElectronico, ProductoRopa
from models.usuario import Cliente, Usuario
from services.tienda_service import TiendaService
from schemas import (
    PedidoCreate,
    PedidoItemRead,
    PedidoRead,
    ProductoCreate,
    ProductoRead,
    UsuarioCreate,
    UsuarioRead,
)

app = FastAPI(title="Tienda Online API")

# instancia unica del servicio, en memoria mientras la app esta corriendo
tienda = TiendaService()


# --- conversores de los objetos de dominio a los esquemas de salida ---------

def usuario_a_read(usuario: Usuario) -> UsuarioRead:
    return UsuarioRead(
        id=usuario.id,
        nombre=usuario.nombre,
        email=usuario.email,
        es_admin=usuario.is_admin(),
    )


def producto_a_read(producto: Producto) -> ProductoRead:
    if isinstance(producto, ProductoElectronico):
        tipo = "electronico"
    elif isinstance(producto, ProductoRopa):
        tipo = "ropa"
    else:
        tipo = "generico"

    return ProductoRead(
        id=producto.id,
        tipo=tipo,
        nombre=producto.nombre,
        precio=producto.precio,
        stock=producto.stock,
        meses_garantia=getattr(producto, "meses_garantia", None),
        talla=getattr(producto, "talla", None),
        color=getattr(producto, "color", None),
    )


def pedido_a_read(pedido) -> PedidoRead:
    items = [
        PedidoItemRead(
            producto_id=producto.id,
            nombre_producto=producto.nombre,
            cantidad=cantidad,
            subtotal=producto.precio * cantidad,
        )
        for producto, cantidad in pedido.lineas
    ]
    return PedidoRead(
        id=pedido.id,
        fecha=pedido.fecha,
        cliente_id=pedido.cliente.id,
        total=pedido.calcular_total(),
        items=items,
    )


# --- usuarios ------------------------------------------------------------

@app.post("/usuarios", response_model=UsuarioRead, status_code=201)
def crear_usuario(datos: UsuarioCreate):
    tipo = datos.tipo.lower()

    if tipo == "cliente" and not datos.direccion:
        raise HTTPException(status_code=400, detail="Un cliente necesita una direccion postal")

    try:
        if tipo == "cliente":
            usuario = tienda.registrar_usuario(
                tipo, nombre=datos.nombre, email=datos.email, direccion=datos.direccion
            )
        else:
            usuario = tienda.registrar_usuario(tipo, nombre=datos.nombre, email=datos.email)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return usuario_a_read(usuario)


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def leer_usuario(usuario_id: str):
    usuario = tienda.obtener_usuario(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_a_read(usuario)


@app.get("/usuarios", response_model=List[UsuarioRead])
def listar_usuarios():
    return [usuario_a_read(u) for u in tienda.listar_usuarios()]


# --- productos -------------------------------------------------------------

@app.post("/productos", response_model=ProductoRead, status_code=201)
def crear_producto(datos: ProductoCreate):
    tipo = datos.tipo.lower()

    if tipo == "electronico" and datos.meses_garantia is None:
        raise HTTPException(status_code=400, detail="Un producto electronico necesita meses_garantia")
    if tipo == "ropa" and (not datos.talla or not datos.color):
        raise HTTPException(status_code=400, detail="Un producto de ropa necesita talla y color")

    try:
        if tipo == "electronico":
            producto = tienda.anadir_producto(
                tipo, nombre=datos.nombre, precio=datos.precio, stock=datos.stock,
                meses_garantia=datos.meses_garantia,
            )
        elif tipo == "ropa":
            producto = tienda.anadir_producto(
                tipo, nombre=datos.nombre, precio=datos.precio, stock=datos.stock,
                talla=datos.talla, color=datos.color,
            )
        else:
            producto = tienda.anadir_producto(
                "generico", nombre=datos.nombre, precio=datos.precio, stock=datos.stock
            )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return producto_a_read(producto)


@app.get("/productos", response_model=List[ProductoRead])
def listar_productos():
    return [producto_a_read(p) for p in tienda.listar_productos()]


@app.get("/productos/{producto_id}", response_model=ProductoRead)
def leer_producto(producto_id: str):
    producto = tienda.obtener_producto(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto_a_read(producto)


@app.delete("/productos/{producto_id}", status_code=204)
def borrar_producto(producto_id: str):
    if not tienda.eliminar_producto(producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")


# --- pedidos -----------------------------------------------------------------

@app.post("/pedidos", response_model=PedidoRead, status_code=201)
def crear_pedido(datos: PedidoCreate):
    cliente = tienda.obtener_usuario(datos.cliente_id)
    if cliente is None or not isinstance(cliente, Cliente):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    for item in datos.items:
        producto = tienda.obtener_producto(item.producto_id)
        if producto is None:
            raise HTTPException(status_code=404, detail=f"Producto {item.producto_id} no encontrado")
        if not producto.hay_stock(item.cantidad):
            raise HTTPException(status_code=400, detail=f"Stock insuficiente de '{producto.nombre}'")

    productos_cantidades = [(item.producto_id, item.cantidad) for item in datos.items]
    pedido = tienda.realizar_pedido(datos.cliente_id, productos_cantidades)
    if pedido is None:
        raise HTTPException(status_code=400, detail="No se pudo crear el pedido")

    return pedido_a_read(pedido)


@app.get("/usuarios/{cliente_id}/pedidos", response_model=List[PedidoRead])
def pedidos_de_cliente(cliente_id: str):
    cliente = tienda.obtener_usuario(cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return [pedido_a_read(p) for p in tienda.listar_pedidos_usuario(cliente_id)]

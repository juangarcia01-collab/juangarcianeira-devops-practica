# juangarcianeira-devops-practica

**Autor:** Juan García Neira

## Descripción

API REST de una tienda online hecha con Python y FastAPI, desarrollada para la asignatura de Arquitectura del Software (UIE).

El proyecto simula el backend de una tienda: gestiona usuarios (clientes y administradores), productos (genéricos, electrónicos y de ropa) y pedidos, reutilizando la lógica de dominio de la Práctica 1 (`Producto`, `Usuario`, `Pedido`, `TiendaService`) y exponiéndola como endpoints HTTP con FastAPI y Pydantic (Práctica 2).

Este repositorio se usa también en las prácticas de la Unidad III para trabajar control de versiones con Git/GitHub (Práctica 3.1) y para contenerizar la aplicación con Docker (Práctica 3.2).

## Estructura

```
src/
  main.py       # API FastAPI (endpoints de usuarios, productos y pedidos)
  schemas.py    # Esquemas Pydantic
  models/       # Clases de dominio (Producto, Usuario, Pedido)
  services/     # TiendaService
requirements.txt
dockerfile
.dockerignore
```

## Cómo ejecutarlo en local (sin Docker)

```bash
cd src
pip install -r ../requirements.txt
uvicorn main:app --reload
```

Después abre `http://127.0.0.1:8000/docs` para probar la API.

## Docker

### Construir la imagen

Desde la raíz del repositorio (donde está el `dockerfile`):

```bash
docker build -f dockerfile -t tienda-online:1.0 .
```

### Ejecutar el contenedor

```bash
docker run -d --name tienda-online -p 8000:8000 tienda-online:1.0
```

Esto mapea el puerto 8000 del contenedor al 8000 de tu máquina. La API queda disponible en `http://127.0.0.1:8000`.

Para pararlo y eliminarlo:

```bash
docker stop tienda-online
docker rm tienda-online
```

### Variables de entorno

La aplicación no requiere ninguna variable de entorno obligatoria: toda la "base de datos" es en memoria, se reinicia con cada arranque del contenedor.

### Cómo probar que funciona

Con el contenedor corriendo:

1. Abre `http://127.0.0.1:8000/docs` en el navegador. Debe cargar la interfaz Swagger con los 9 endpoints (usuarios, productos, pedidos).
2. Prueba un flujo básico:
   - `POST /usuarios` con `{"nombre": "Ana Perez", "email": "ana@example.com", "tipo": "cliente", "direccion": "Calle Mayor 1"}` → debe devolver `201` y un usuario con `id`.
   - `POST /productos` con `{"tipo": "electronico", "nombre": "Portatil", "precio": 899, "stock": 10, "meses_garantia": 24}` → `201` con el producto creado.
   - `POST /pedidos` usando los `id` anteriores → `201` con el pedido y el total calculado.
3. También puedes comprobarlo por terminal, sin abrir el navegador:

```bash
curl http://127.0.0.1:8000/usuarios
# [] -> la lista empieza vacía en cada contenedor nuevo
```

### Publicar la imagen en un registry

```bash
docker login
docker tag tienda-online:1.0 <tu-usuario-dockerhub>/tienda-online:1.0
docker push <tu-usuario-dockerhub>/tienda-online:1.0
```

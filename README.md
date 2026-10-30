# juangarcianeira-devops-practica

**Autor:** Juan García Neira

## Descripción

API REST de una tienda online hecha con Python y FastAPI, desarrollada para la asignatura de Arquitectura del Software (UIE).

El proyecto simula el backend de una tienda: gestiona usuarios (clientes y administradores), productos (genéricos, electrónicos y de ropa) y pedidos, reutilizando la lógica de dominio de la Práctica 1 (`Producto`, `Usuario`, `Pedido`, `TiendaService`) y exponiéndola como endpoints HTTP con FastAPI y Pydantic (Práctica 2).

Este repositorio se usa también en las prácticas de la Unidad III para trabajar control de versiones con Git/GitHub y, en la rama `feature/docker`, para contenerizar la aplicación con Docker.

## Estructura

```
Tienda_online/
  main.py            # API FastAPI (endpoints de usuarios, productos y pedidos)
  schemas.py          # Esquemas Pydantic
  models/              # Clases de dominio (Producto, Usuario, Pedido)
  services/            # TiendaService
requirements.txt
```

## Cómo ejecutarlo

```bash
cd Tienda_online
pip install -r ../requirements.txt
uvicorn main:app --reload
```

Después abre `http://127.0.0.1:8000/docs` para probar la API.

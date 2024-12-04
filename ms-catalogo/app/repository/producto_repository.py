from app import db
from app.models.producto import Producto

def guardar_producto(data):
    nuevo_producto = Producto(
        nombre = data["nombre"],
        precio = data["precio"],
        activo = data.get("activo", True) #Por defecto se setea en true
    )
    db.session.add(nuevo_producto)
    db.session.commit()
    return {
        "id": nuevo_producto.id,
        "nombre": nuevo_producto.nombre,
        "precio": nuevo_producto.precio,
        "activo": nuevo_producto.activo
    }

def obtener_por_id(id):
    producto = Producto.query.get(id)
    if producto is None or not producto.activo:
        return None
    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "activo": producto.activo
    }


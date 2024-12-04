from app import cache
from app.repository.producto_repository import guardar_producto, obtener_por_id

class ProductoService:

    @cache.memoize(timeout=90)
    def obtener_producto_id(self, id):
        producto = obtener_por_id(id)
        if not producto:
            raise ValueError(f"No se encontro el producto con el id {id}")
        return producto

    @staticmethod
    def crear_producto(data):
        if not data or 'nombre' not in data or 'precio' not in data:
            raise ValueError("Datos incompletos: nombre y precio obligatorios")
        
        nuevo_producto = {
            "nombre": data["nombre"],
            "precio": data["precio"],
            "activo": data.get("activo", True)
        }
        return guardar_producto(nuevo_producto)
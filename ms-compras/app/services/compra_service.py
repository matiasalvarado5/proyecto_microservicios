from app.repository.compra_repository import guardar_compra, cancelar_compra

class CompraService:
    @staticmethod
    def crear_compra(data):
        if not data or 'producto_id' not in data or 'cantidad' not in data:
            raise ValueError("Datos incompletos")
        
        nueva_compra = {
            "producto_id": data["producto_id"],
            "cantidad" : data["cantidad"],
            "direccion_envio": data["direccion_envio"]
        }
        return guardar_compra(nueva_compra)

    @staticmethod
    def compensar_compra(compra_id):
        return cancelar_compra(compra_id)
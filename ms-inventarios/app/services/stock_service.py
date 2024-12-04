from app.repository.stock_repository import cancelar_transaccion, obtener_stock_actual, registrar_entrada_salida

class StockService:
    @staticmethod
    def crear_registro_transaccion(data):
        if not data:
            raise ValueError("Datos incompletos")
        if data["cantidad"] <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        nueva_transaccion = {
            "producto_id": data["producto_id"],
            "cantidad": data["cantidad"],
            "entrada_salida": data["entrada_salida"]
        }
        return registrar_entrada_salida(nueva_transaccion)

    @staticmethod
    def compensar_transaccion(transaccion_id):
        return cancelar_transaccion(transaccion_id)

    @staticmethod
    def obtener_stock(id):
        stock = obtener_stock_actual(id)
        if not stock:
            raise ValueError(f"No se encontro el producto con el id {id}")
        return stock
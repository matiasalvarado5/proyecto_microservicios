from app.repository.pago_repository import guardar_pago, obtener_todos, cancelar_pago

class PagoService:
    @staticmethod
    def crear_pago(data):
        if not data or 'monto' not in data or 'metodo' not in data:
            raise ValueError("Datos incompletos")

        nuevo_pago = {
            "monto": data["monto"],
            "metodo": data["metodo"],
            "descripcion": data.get("descripcion", "")
        }
        return guardar_pago(nuevo_pago)

    @staticmethod
    def compensar_pago(pago_id):
        return cancelar_pago(pago_id)

    @staticmethod
    def listar_pagos():
        return obtener_todos()

import pybreaker
from app import COMPRAS_SERVICE_URL
from app.services.api_requests import forward_request

class CompraService:

    compra_circuit_breaker = pybreaker.CircuitBreaker(fail_max = 3, reset_timeout = 5)
    @staticmethod
    def crear_compra(data):
        """Crea la compra en el microservicio de compras"""
        url = f"{COMPRAS_SERVICE_URL}/"
        try:
            response, status_code = CompraService.compra_circuit_breaker.call(forward_request, url, "POST", data=data)
            if status_code == 201:
                compra = response.get("compra")
                if not compra or "id" not in compra:
                    raise ValueError("Respuesta inesperada del microservicio de compras: falta el campo id")
                compra_id = compra["id"]
                data["compra_id"] = compra_id
                return {"compra_id": compra_id, **data}
            raise ValueError("Error al crear la compra")
        except pybreaker.CircuitBreakerError:
            return {"error": "Servicio de compras no disponible"}, 503

    @staticmethod
    def compensar_compra(compra_id):
        """Compensa la compra (en caso de error en el flujo)"""
        url = f"{COMPRAS_SERVICE_URL}/compensar/{compra_id}"
        response, status_code = forward_request(url, "DELETE")
        return {"status": "Compensacion completada"} if status_code == 200 else None
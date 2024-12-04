import pybreaker
from app import cache, CATALOGO_SERVICE_URL
from app.services.api_requests import forward_request

class CatalogoService:

    catalogo_circuit_breaker = pybreaker.CircuitBreaker(fail_max = 3, reset_timeout = 5)

    @cache.memoize(timeout=90)
    def obtener_producto(self, id):
        url = f"{CATALOGO_SERVICE_URL}/{id}"
        try:
            response, status_code = CatalogoService.catalogo_circuit_breaker.call(forward_request, url, "GET")
            if status_code == 200:
                return response
            else:
                return None
        except pybreaker.CircuitBreakerError:
            return {"error": "Servicio de catalogo no disponible"}, 503
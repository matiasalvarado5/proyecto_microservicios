from flask import Blueprint, request, jsonify
from app.services.producto_service import ProductoService

catalogo_bp = Blueprint('catalogo', __name__)
producto_service = ProductoService()

@catalogo_bp.route('/', methods = ['POST'])
def crear_producto_route():
    """Recibe una solicitud POST y la redirige al microservicio de catalogo"""
    data = request.get_json()
    try:
        producto = producto_service.crear_producto(data)
        return jsonify({
            "mensaje": "Producto creado exitosamente",
            "producto": producto
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@catalogo_bp.route('/<int:id>', methods = ['GET'])
def obtener_producto_id_route(id):
    try:
        producto = producto_service.obtener_producto_id(id)
        if producto is None:
            return jsonify({"mensaje": "No se encontro el producto."}), 404
        return jsonify(producto), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
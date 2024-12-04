from flask import Blueprint, request, jsonify
from app.services.stock_service import StockService

inventario_bp = Blueprint('inventario', __name__)
stock_service = StockService() 

@inventario_bp.route('/', methods = ["POST"])
def crear_registro_route():
    data = request.get_json()
    try:
        registro = stock_service.crear_registro_transaccion(data)
        if registro is None:
            return jsonify({"mensaje": "Transaccion fallida. No hay stock suficiente"}), 400
        if registro == 404:
            return jsonify({"message": "Transaccion fallida. No existe la ID del producto"}), 400
        return jsonify({
            "mensaje": "Transaccion registrada exitosamente",
            "transaccion": registro
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@inventario_bp.route('/compensar/<int:id>', methods = ["DELETE"])
def compensar_transaccion_route(id):
    try:
        resultado = stock_service.compensar_transaccion(id)
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@inventario_bp.route('/<int:id>', methods = ["GET"])
def obtener_stock_route(id):
    try:
        stock = stock_service.obtener_stock(id)
        return jsonify(stock), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
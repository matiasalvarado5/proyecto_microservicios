from flask import Blueprint, request, jsonify
from app.services.compra_service import CompraService

compra_bp = Blueprint('compras', __name__)
compra_service = CompraService()

@compra_bp.route('/', methods = ["POST"])
def crear_compra_route():
    data = request.get_json()
    try:
        compra = compra_service.crear_compra(data)
        return jsonify({
            "mensaje": "Compra creada exitosamente",
            "compra": compra
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@compra_bp.route('/compensar/<int:id>', methods = ["DELETE"])
def compensar_compra_route(id):
    try:
        resultado = compra_service.compensar_compra(id)
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
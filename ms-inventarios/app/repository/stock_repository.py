from flask import jsonify
import requests
from app import db, cache, CATALOGO_SERVICE_URL
from app.models.stock import Stock
import datetime

@cache.memoize(timeout=90)
def obtener_producto(id):
    try:
        producto_response = requests.get(f"{CATALOGO_SERVICE_URL}/{id}")
        return producto_response.json(), producto_response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Servicio no disponible", "detalles": str(e)}), 503
    
def registrar_entrada_salida(data):
    fecha = datetime.datetime.now()
    # Controlo que lo que retiro no sea mayor al stock actual
    id = data["producto_id"]
    producto_response, producto_status_code = obtener_producto(id)
    if producto_status_code == 404:
        return 404
    if producto_response is None:
        return None
    if data["entrada_salida"] == 2:
        stock = obtener_stock_actual(data["producto_id"])
        if stock is None:
            return None
        if int(data["cantidad"]) > stock["stock"]:
            return None
    
    nuevo_registro = Stock(
        producto_id = data["producto_id"],
        cantidad = data["cantidad"],
        entrada_salida = data["entrada_salida"],
        fecha_transaccion = fecha
    )
    db.session.add(nuevo_registro)
    db.session.commit()
    return {
        "id": nuevo_registro.id,
        "producto_id": nuevo_registro.producto_id,
        "cantidad": nuevo_registro.cantidad,
        "entrada_salida": nuevo_registro.entrada_salida,
        "fecha_transaccion": nuevo_registro.fecha_transaccion.strftime("%Y-%m-%d %H:%M:%S")
    }

def cancelar_transaccion(transaccion_id):
    transaccion = db.session.query(Stock).get(transaccion_id)
    if transaccion:
        db.session.delete(transaccion)
        db.session.commit()
        return jsonify({"mensaje": f"Transaccion {transaccion_id} eliminada"})
    else:
        raise ValueError(f"No se encontro la transaccion {transaccion_id}")

def obtener_stock_actual(producto_id):
    stock = db.session.query(Stock).filter(Stock.producto_id == producto_id).first() # Verifico existencia de stock
    if not stock:
        return {
            "producto_id": producto_id,
            "stock": 0
        }
    
    entradas = db.session.query(db.func.sum(Stock.cantidad)).filter(
        Stock.producto_id == producto_id,
        Stock.entrada_salida == 1 # 1 = Entrada
    ).scalar() or 0

    salidas = db.session.query(db.func.sum(Stock.cantidad)).filter(
        Stock.producto_id == producto_id,
        Stock.entrada_salida == 2 # 2 = Salida
    ).scalar() or 0

    return {
        "producto_id": producto_id,
        "stock": entradas - salidas
    }
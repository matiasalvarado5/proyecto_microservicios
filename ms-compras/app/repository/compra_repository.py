from app import db
from app.models.compra import Compra
import datetime

def guardar_compra(data):
    fecha = datetime.datetime.now()
    nueva_compra = Compra(
        producto_id = data["producto_id"],
        cantidad = data["cantidad"],
        direccion_envio = data["direccion_envio"],
        fecha_compra = fecha
    )
    db.session.add(nueva_compra)
    db.session.commit()
    return {
        "id": nueva_compra.id,
        "producto_id": nueva_compra.producto_id,
        "cantidad": nueva_compra.cantidad,
        "fecha_compra": nueva_compra.fecha_compra.strftime("%Y-%m-%d %H:%M:%S"),
        "direccion_envio": nueva_compra.direccion_envio
    }

def cancelar_compra(compra_id):
    compra = db.session.query(Compra).get(compra_id)
    if compra:
        db.session.delete(compra)
        db.session.commit()
        return {"mensaje": f"Compra {compra_id} eliminada"}
    else:
        raise ValueError(f"No se encontro la compra con id {compra_id}")
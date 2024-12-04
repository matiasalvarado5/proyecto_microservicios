from app import db
from app.models.pago import Pago

def guardar_pago(data):
    nuevo_pago = Pago(
        monto=data["monto"],
        metodo=data["metodo"],
        descripcion=data["descripcion"]
    )
    db.session.add(nuevo_pago)
    db.session.commit()
    return {
        "id": nuevo_pago.id,
        "monto": nuevo_pago.monto,
        "metodo": nuevo_pago.metodo,
        "descripcion": nuevo_pago.descripcion
    }

def cancelar_pago(pago_id):
    pago = db.session.query(Pago).get(pago_id)
    if pago:
        db.session.delete(pago)
        db.session.commit()
        return {"mensaje": f"Pago {pago_id} eliminado"}
    else:
        raise ValueError(f"No se encontro el pago con id {pago_id}")
    
def obtener_todos():
    pagos = Pago.query.all()
    return [
        {"id": p.id, 
         "monto": p.monto, 
         "metodo": p.metodo, 
         "descripcion": p.descripcion}
        for p in pagos
    ]

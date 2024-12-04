import http from 'k6/http';
import {check, sleep} from 'k6';

//configuracion
export const options ={
    vus: 60, //numero de usuarios
    duration: '7s', //duracion de la prueba
};

export default function (){
    const url = __ENV.MAIN_COMMERCE_COMPRA_URL; 
    const payload = JSON.stringify({
        producto_id: 1,
        cantidad:5,
        direccion_envio: "Calle 123",
        metodo: "tarjeta"
    });
    const params ={
        headers:{
            'Content-Type': 'application/json'
        },
    };
    const res = http.post(url, payload, params);
    check (res, {
        'Compras con exito': (r) => r.status === 201,
    });

    sleep(1);
}
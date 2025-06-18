from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tarifas = [
    {"origen": "Bogotá", "destino": "Cali", "tarifa": 2400},
    {"origen": "Bogotá", "destino": "Medellín", "tarifa": 2900},
    {"origen": "Bogotá", "destino": "Barranquilla", "tarifa": 2900},
    {"origen": "Bogotá", "destino": "Cartagena", "tarifa": 2400},
    {"origen": "Medellín", "destino": "Bogotá", "tarifa": 2900},
    {"origen": "Medellín", "destino": "Cali", "tarifa": 2900},
    {"origen": "Medellín", "destino": "Barranquilla", "tarifa": 2900},
    {"origen": "Cali", "destino": "Bogotá", "tarifa": 2400},
    {"origen": "Cali", "destino": "Medellín", "tarifa": 2900},
    {"origen": "Cali", "destino": "Barranquilla", "tarifa": 2900},
    {"origen": "Barranquilla", "destino": "Bogotá", "tarifa": 2900},
    {"origen": "Barranquilla", "destino": "Cali", "tarifa": 2900},
    {"origen": "Barranquilla", "destino": "Medellín", "tarifa": 2900},
]

class FleteInput(BaseModel):
    origen: str
    destino: str
    peso: float

@app.post("/calcular-flete")
def calcular_flete(datos: FleteInput):
    tarifa = next((t["tarifa"] for t in tarifas if t["origen"] == datos.origen and t["destino"] == datos.destino), None)
    if tarifa is None:
        raise HTTPException(status_code=404, detail="Ruta no disponible")
    iva = round(tarifa * 0.19, 2)
    total = round(datos.peso * tarifa + iva, 2)
    return {
        "origen": datos.origen,
        "destino": datos.destino,
        "peso": datos.peso,
        "tarifa_por_kg": tarifa,
        "iva_19": iva,
        "total_flete": total
    }

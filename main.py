from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- BASE DE DATOS ---------

def init_db():
    conn = sqlite3.connect("papeleria.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT,
            nombre TEXT,
            compra REAL,
            porcentaje REAL,
            venta REAL,
            cantidad_existente INTEGER,
            cantidad_comprar INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --------- MODELO ---------

class Producto(BaseModel):
    codigo: str
    nombre: str
    compra: float
    porcentaje: float
    venta: float
    cantidad_existente: int
    cantidad_comprar: int

# --------- RUTAS ---------

@app.get("/")
def home():
    return {"mensaje":"API funcionando"}

@app.get("/productos")
def obtener_productos():
    conn = sqlite3.connect("papeleria.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    data = cursor.fetchall()
    conn.close()
    return data

@app.post("/productos")
def agregar_producto(producto: Producto):
    conn = sqlite3.connect("papeleria.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO productos 
        (codigo,nombre,compra,porcentaje,venta,cantidad_existente,cantidad_comprar)
        VALUES (?,?,?,?,?,?,?)
    """, (
        producto.codigo,
        producto.nombre,
        producto.compra,
        producto.porcentaje,
        producto.venta,
        producto.cantidad_existente,
        producto.cantidad_comprar
    ))
    conn.commit()
    conn.close()
    return {"mensaje":"Producto guardado"}

@app.delete("/productos/{id}")
def eliminar_producto(id:int):
    conn = sqlite3.connect("papeleria.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return {"mensaje":"Eliminado"}

# --------- BUSCAR EN EXCEL ---------

@app.get("/buscar_producto/{codigo}")
def buscar_producto(codigo:str):
    try:
        df = pd.read_excel("productos.xlsx")
        fila = df[df["codigo"].astype(str) == codigo]

        if not fila.empty:
            nombre = fila.iloc[0]["nombre"]
            return {"nombre":nombre}

        return {"nombre":""}

    except Exception as e:
        return {"error":str(e)}

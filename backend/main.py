from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI()

# ==========================
# CORS
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# BASE DE DATOS
# ==========================
DB_PATH = os.path.join(os.getcwd(), "productos.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tabla básica si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            codigo TEXT PRIMARY KEY,
            nombre TEXT,
            piezas INTEGER
        )
    """)

    # Agregar columnas nuevas si no existen
    try:
        cursor.execute("ALTER TABLE productos ADD COLUMN precio_compra REAL DEFAULT 0")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE productos ADD COLUMN porcentaje REAL DEFAULT 0")
    except:
        pass

    try:
        cursor.execute("ALTER TABLE productos ADD COLUMN precio_venta REAL DEFAULT 0")
    except:
        pass

    conn.commit()
    conn.close()

init_db()

def get_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# ==========================
# RUTA PRINCIPAL
# ==========================
@app.get("/")
def home():
    return {"status": "API Papelería OK"}

# ==========================
# GUARDAR PRODUCTO
# ==========================
@app.post("/guardar")
def guardar(p: dict):
    precio_compra = float(p.get("precio_compra", 0))
    porcentaje = float(p.get("porcentaje", 0))

    precio_venta = precio_compra + (precio_compra * porcentaje / 100)

    conn = get_db()
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO productos 
        (codigo, nombre, piezas, precio_compra, porcentaje, precio_venta)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        p.get("codigo"),
        p.get("nombre"),
        p.get("piezas"),
        precio_compra,
        porcentaje,
        precio_venta
    ))
    conn.commit()
    conn.close()

    return {"ok": True, "precio_venta": precio_venta}

# ==========================
# LISTA DE FALTANTES
# ==========================
@app.get("/faltantes")
def faltantes():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT codigo, nombre, piezas, precio_compra, porcentaje, precio_venta
        FROM productos
        WHERE piezas <= 5
        ORDER BY piezas ASC
    """)
    rows = c.fetchall()
    conn.close()

    return [
        {
            "codigo": r[0],
            "nombre": r[1],
            "piezas": r[2],
            "precio_compra": r[3],
            "porcentaje": r[4],
            "precio_venta": r[5]
        }
        for r in rows
    ]

# ==========================
# ELIMINAR PRODUCTO
# ==========================
@app.delete("/eliminar/{codigo}")
def eliminar_producto(codigo: str):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))
    conn.commit()
    conn.close()
    return {"ok": True}

# ==========================
# BUSCAR POR CÓDIGO
# ==========================
@app.get("/buscar_codigo/{codigo}")
def buscar_codigo(codigo: str):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT codigo, nombre, piezas, precio_compra, porcentaje, precio_venta FROM productos WHERE codigo = ?",
        (codigo,)
    )
    r = c.fetchone()
    conn.close()

    if r:
        return {
            "codigo": r[0],
            "nombre": r[1],
            "piezas": r[2],
            "precio_compra": r[3],
            "porcentaje": r[4],
            "precio_venta": r[5]
        }
    return {}

# ==========================
# BUSCAR POR NOMBRE
# ==========================
@app.get("/buscar_nombre/{texto}")
def buscar_nombre(texto: str):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT codigo, nombre, piezas, precio_compra, porcentaje, precio_venta FROM productos WHERE nombre LIKE ?",
        (f"%{texto}%",)
    )
    rows = c.fetchall()
    conn.close()

    return [
        {
            "codigo": r[0],
            "nombre": r[1],
            "piezas": r[2],
            "precio_compra": r[3],
            "porcentaje": r[4],
            "precio_venta": r[5]
        }
        for r in rows
    ]

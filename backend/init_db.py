def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            codigo TEXT PRIMARY KEY,
            nombre TEXT,
            piezas INTEGER,
            precio_compra REAL DEFAULT 0,
            porcentaje REAL DEFAULT 0,
            precio_venta REAL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

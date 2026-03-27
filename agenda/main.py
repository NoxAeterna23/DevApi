from fastapi import FastAPI, HTTPException
import sqlite3
import time
import pytest
import requests


app = FastAPI()
nombreDB = "agenda.db"

def conectar_db():
    conn = sqlite3.connect(nombreDB)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/", status_code=202) # Mensaje de bienvenida
def read_root():
    return {
        "message": "MENSAJE DE BIENVENIDA",
        "datetime": time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())
    }

@app.get("/v1/contactos", status_code=202)
def get_contactos(limit: int = 10, skip: int = 0):

    if limit < 0 or skip < 0: # Verifica que limit y skip sean mayores a 0 para que no devuelva todos los registros en caso de numero negativo.
        raise HTTPException(status_code=400, detail="limit y skip deben ser positivos")

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM contactos LIMIT ? OFFSET ?",
        (limit, skip)
    )

    rows = cursor.fetchall()

    contactos = [dict(row) for row in rows]

    return {
        "table": "contactos",
        "items": contactos,
        "count": len(contactos),
        "datetime": time.strftime("%m/%d/%Y, %H:%M:%S"),
        "message": "Datos consultados exitosamente",
        "limit": limit,
        "skip": skip
    }
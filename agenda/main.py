from fastapi import FastAPI, HTTPException
import sqlite3
import time
from pydantic import BaseModel


app = FastAPI()
nombreDB = "agenda.db"

def conectar_db():
    conn = sqlite3.connect(nombreDB)
    conn.row_factory = sqlite3.Row
    return conn

@app.get(
        "/", 
         status_code=202, 
         summary="Raiz/Bienvenida del Endpoint",
         description="Muestra el mensaje de bienvenida de la API"
) # Mensaje de bienvenida
def read_root():
    return {
        "message": "Bienvenido a la Api :D",
        "datetime": time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())
    }

@app.get(
        "/v1/contactos", 
         status_code=202,
         summary="Consulta de los contactos",
         description="Obtiene una consulta paginada de los contactos, con limit y skip"
)
def get_contactos(limit: int = 10, skip: int = 0):

    if limit < 0 or skip < 0: # Verifica que limit y skip sean mayores a 0 para que no devuelva todos los registros en caso de numero negativo.
        raise HTTPException(status_code=400, detail="limit y skip deben ser valores positivos")

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM contactos LIMIT ? OFFSET ?",
        (limit, skip)
    )

    contactos = cursor.fetchall() 

    contactos = [dict(row) for row in contactos] # mete los contactos en un diccionario para su visualización más comoda abajo.

    return {
        "table": "contactos",
        "items": contactos,
        "count": len(contactos),
        "datetime": time.strftime("%m/%d/%Y, %H:%M:%S"),
        "message": "Datos consultados exitosamente",
        "limit": limit,
        "skip": skip
    }

@app.get(
        "/v1/contacto", 
        status_code=202,
        summary="Endpoint para obtener un contacto",
        description="Endpoint que obtiene un solo contacto al pasarle la id o el nombre."
)
def get_contacto(id: int = None, nombre: str = None):
    conn = conectar_db()
    cursor = conn.cursor()

    if id:
        cursor.execute("SELECT * FROM contactos WHERE id_contacto=?", (id,))
    elif nombre:
        cursor.execute("SELECT * FROM contactos WHERE nombre=?", (nombre,))
    else:
        raise HTTPException(status_code=400, detail="Se debe ingresar un id o un nombre.")
    
    contacto = cursor.fetchone()

    if not contacto:
        raise HTTPException(status_code=400, detail="Contacto no encontrado.")
    
    return {"message": "Contacto encontrado",
            "item": contacto
    }

class Contacto(BaseModel): # Se crea una clase Contacto con una librería que le ayuda a validar automaticamente los datos insertados sin extraer manualmente
    nombre: str             # el JSON, y con el esqueleto de lo que se le va a pasar a SQL para insertar los datos.
    telefono: str
    email: str

@app.post(
        "/v1/contacto", 
        status_code=202,
        summary="Endpoint crea contacto",
        description="Se utiliza para crear un contacto dandole nombre, numero y un email."
)
def create_contacto(contacto: Contacto): # Le paso la clase con el esqueleto

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contactos (nombre, telefono, email) VALUES (?, ?, ?)", (contacto.nombre, contacto.telefono, contacto.email)
    )

    conn.commit()

    return {"message": "Contacto Creado."}

@app.put(
        "/v1/contacto", 
        status_code=202,
        summary="Endpoint actualiza contacto",
        description="Actualiza un contacto de la lista de contactos."
)
def update_contacto(id: int, contacto: Contacto):

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE contactos SET nombre=?, telefono=?, email=? WHERE id_contacto=?", (contacto.nombre, contacto.telefono, contacto.email, id,))

    conn.commit()

    return {"message": "Contacto actualizado"}

@app.delete("/v1/contacto", status_code=202)
def delete_contacto(id: int):

    conn = conectar_db
    cursor = conn.cursor

    cursor.execute("DELETE FROM contactos WHERE id_contacto=?", (id,))

    return {"message": "Contacto eliminado"}


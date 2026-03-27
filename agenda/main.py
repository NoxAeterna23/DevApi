from fastapi import FastAPI, HTTPException
import sqlite3
import time
import csv

app = FastAPI()

def conectar_db():
    conn = sqlite3.connect("agenda.db")
    conn.row_factory = sqlite3.Row
    return conn


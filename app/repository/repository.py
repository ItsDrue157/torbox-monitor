import os
import sqlite3
from pathlib import Path


DB_PATH = Path(os.getenv("DB_PATH", "app/database/downloads.db"))

def connect_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def criar_tabela_downloads():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS downloads (torbox_id INTEGER PRIMARY KEY,name TEXT NOT NULL,download_state TEXT,progress REAL,eta INTEGER,download_speed INTEGER);")


def salvar_downloads(download):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO downloads (torbox_id, name, download_state, progress, eta) VALUES (?, ?, ?, ?, ?)",(download["id"],download["name"],download["download_state"], download["progress"],download["eta"]))
    return True



def buscar_download(torbox_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT download_state FROM downloads WHERE torbox_id = ?", (torbox_id,))
        resultado = cursor.fetchone()
    if resultado:
        download_state = resultado[0]
        return download_state
    else:
        return None

def atualizar_download(download):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE downloads SET download_state = ?, progress = ?, eta = ? WHERE torbox_id = ?", (download["download_state"], download["progress"],download["eta"], download["id"]))
    return True


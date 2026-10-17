import sqlite3

DB_NAME = 'termos.db'

def criar_tabela():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT,
            idioma TEXT,
            abusivas TEXT,
            resumo TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def salvar_analise(texto, idioma, abusivas, resumo):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analises (texto, idioma, abusivas, resumo)
        VALUES (?, ?, ?, ?)
    ''', (texto, idioma, str(abusivas), resumo)
    )
    conn.commit()
    conn.close()

def listar_analises():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, idioma, resumo, data FROM analises ORDER BY data DESC')
    resultados = cursor.fetchall()
    conn.close()
    return resultados
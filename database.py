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

def criar_tabela_termos_abusivos():
    # Abre (ou cria) a base de dados 'termos.db'
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Cria a tabela 'termos_abusivos' se ainda não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS termos_abusivos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   -- chave única
            clausula TEXT,                          -- texto da cláusula abusiva
            nivel TEXT,                             -- nivel (grave ou moderado)
            fonte TEXT                              -- site ou documento de onde veio
        )
    """)

    conn.commit()   # grava as alterações
    conn.close()    # fecha a ligação (IMPORTANTE para não deixar ficheiro bloqueado)


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
    cursor.execute('SELECT id, texto, idioma, resumo, data FROM analises ORDER BY data DESC')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obter_analise(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, texto, idioma, abusivas, resumo, data FROM analises WHERE id = ?', (id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def inserir_termo_abusivo(clausula, nivel, fonte):
    """
    Insere uma cláusula abusiva na tabela termos_abusivos.
    clausula -> texto da cláusula
    nivel -> 'grave' ou 'moderado'
    fonte -> origem (site, artigo, manual)
    """
    conn = sqlite3.connect(DB_NAME)   # abre ligação ao ficheiro da base
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO termos_abusivos (clausula, nivel, fonte)
        VALUES (?, ?, ?)
    """, (clausula, nivel, fonte))

    conn.commit()   # grava alterações
    conn.close()    # fecha ligação

def listar_termos_abusivos():
    """
    Retorna todos os termos abusivos guardados na base.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, clausula, nivel, fonte FROM termos_abusivos")
    resultados = cursor.fetchall()

    conn.close()
    return resultados

import sqlite3
from flask import g # g funciona COMO UM DICIONÁRIO
import os

# abrindo caminho para o banco de dados:
# isso serve para o código rodar em qualquer máquina
DATABASE = os.path.join(os.path.dirname(__file__), 'wayne.db')
# file é uma variável especial python que guarda o caminho do arquivo atual
# os.path.dirname(file) pega a pasta desse caminho e remove o nome do arquivo
# depois juntamos a pasta com o nome do banco de dados com o os.path.join

def get_db():
# conexão com o banco de dados
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE) # atributo especial do flask (g) para guardar dados durante 
        # a requisição (.db é só um nome que escolhi), ligado aos atrbutos do python

        g.db.row_factory = sqlite3.Row  # para retornar resultados como dicionários
    return g.db

# fechar a conexão com o banco de dados
# pop remove o atributo db de g e retorna ele, se não tiver retorna None:

def close_db(e=None):
    db = g.pop('db', None) 
    if db is not None:
        db.close()
    
def init_db():
    # inicializar o banco de dados com as tabelas se não tiver
    db = get_db()

        # Tabela de usuários
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Tabela de armas
    db.execute('''
        CREATE TABLE IF NOT EXISTS weapons(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    # Tabela de veículos
    db.execute('''
        CREATE TABLE IF NOT EXISTS vehicles(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            plate TEXT UNIQUE NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    # Tabela de itens
    db.execute('''
        CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')

    # agora vms verificar se possui algum usuário admin:

    cursor = db.execute('SELECT COUNT(*) as count FROM users WHERE role = "admin"')
    if cursor.fetchone()['count'] == 0: #fetchone pega a primeira linha do resultado
        # se não tiver, cria um admin padrão
        db.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                   ('admin', 'admin123', 'admin'))
    db.commit()
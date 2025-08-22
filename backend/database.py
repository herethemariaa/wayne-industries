import sqlite3

def create_tables():
    conn = sqlite3.connect("wayne.db")  # conecta no database
    cursor = conn.cursor()  # cria o cursor para navegar no database

    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Tabela de armas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weapons(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    # Tabela de veículos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            plate TEXT UNIQUE NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    # Tabela de itens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')

    conn.commit()  # salva as alterações
    conn.close()   # fecha a conexão

if __name__ == "__main__":
    create_tables()
    print("Banco de dados criado com sucesso!")

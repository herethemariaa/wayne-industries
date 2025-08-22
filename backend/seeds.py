import sqlite3

def seed_data():
    conn = sqlite3.connect("wayne.db")
    cursor = conn.cursor()

    #usuario teste de admin
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
                   ("admin", "admin123", "admin"))
    #testar weapons
    cursor.execute("INSERT OR IGNORE INTO weapons (name, category, date) VALUES (?, ?, ?)",
                   ("Batarang", "Gadgets", "2023-10-01"))
    #testar vehicles
    cursor.execute("INSERT OR IGNORE INTO vehicles (model, plate, date) VALUES (?, ?, ?)",
                   ("Batmobile", "BAT-1234", "2023-10-01"))
    #testar items
    cursor.execute("INSERT OR IGNORE INTO items (name, category, date, quantity) VALUES (?, ?, ?, ?)",
                   ("Grapple Gun", "Gadgets", "2023-10-01", 10))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_data()
    print("Dados semeados com sucesso!")
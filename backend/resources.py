# CRUD dos recursos (arsenal, veículos, etc)
from flask import Blueprint, request, jsonify
from database import get_db
from auth import login_required
from datetime import datetime

resources_bp = Blueprint('resources', __name__)

# CRUD PARA ARMAS VIA ROTAS:

@resources_bp.route('/weapons', methods=['GET'])
@login_required
def get_weapons():
    conn = get_db()
    weapons = conn.execute('SELECT * FROM weapons').fetchall()
    conn.close()
    return jsonify([dict(weapon) for weapon in weapons])

@resources_bp.route('/weapons', methods=['POST'])
@login_required #só admin pode criar

def add_weapon():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO weapons (name, category, date) VALUES (?, ?, ?)',
                   (data['name'], data['category'], datetime.now().strftime('%Y-%m-%d'))
                   )
    conn.commit()
    weapon_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': "Arma adicionada com sucesso", 'id': weapon_id})

resources_bp.rout('/weapons/<int:id', methods=['PUT'])
@login_required

def update_weapon(id):
    data = request.get_json()
    conn = get_db()
    conn.execute('UPDATE weapons SET name = ?, category = ? WHERE id = ?',
                 (data['name'], data['category'], id)
                 )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Atualização efetuada.'})

def delete_weapon(id):
    conn = get_db()
    conn.execute('DELETE FROM weapons WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Arma deletada.'})

# CRUD PARA VEÍCULOS VIA ROTAS:
@resources_bp.route('/vehicles', methods=['GET'])
@login_required
def get_vehicles():
    conn = get_db()
    vehicles = conn.execute('SELECT * FROM vehicles').fetchall()
    conn.close()
    return jsonify([dict(vehicle) for vehicle in vehicles])

@resources_bp.route('/vehicles', methods=['POST'])
@login_required

def add_vehicle():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO vehicles (model, plate, date) VALUES (?, ?, ?)',
                   (data['model'], data['plate'], datetime.now().strftime('%Y-%m-%d'))
                   )
    conn.commit()
    vehicle_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': "Veículo adicionado com sucesso", 'id': vehicle_id})

@resources_bp.route('/vehicles/<int:id>', methods=['PUT'])
@login_required

def update_vehicle(id):
    data = request.get_json()
    conn = get_db()
    conn.execute('UPDATE vehicles SET model = ?, plate = ? WHERE id = ?',
                 (data['model'], data['plate'], id)
                 )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Atualização efetuada.'})

@resources_bp.route('/vehicles/<int:id>', methods=['DELETE'])
@login_required

def delete_vehicle(id):
    conn = get_db()
    conn.execute('DELETE FROM vehicles WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Veículo deletado.'})

# CRUD PARA ITENS VIA ROTAS:
@resources_bp.route('/items', methods=['GET'])
@login_required

def get_items():
    conn = get_db()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return jsonify([dict(item) for item in items])

@resources_bp.route('/items', methods=['POST'])
@login_required

def add_item():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO items (name, category, date, quantity) VALUES (?, ?, ?, ?)',
                   (data['name'], data['category'], datetime.now().strftime('%Y-%m-%d'), data['quantity'])
                   )
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': "Item adicionado com sucesso", 'id': item_id})

@resources_bp.route('/items/<int:id>', methods=['PUT'])
@login_required

def update_item(id):
    data = request.get_json()
    conn = get_db()
    conn.execute('UPDATE items SET name = ?, category = ?, quantity = ? WHERE id = ?',
                 (data['name'], data['category'], data['quantity'], id)
                 )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Atualização efetuada.'})

@resources_bp.route('/items/<int:id>', methods=['DELETE'])
@login_required

def delete_item(id):
    conn = get_db()
    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Item deletado.'})


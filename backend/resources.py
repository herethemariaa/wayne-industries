# resources.py
from flask import Blueprint, request, jsonify, session
from database import get_db
from auth import login_required
from datetime import datetime

resources_bp = Blueprint('resources', __name__)

# -------------------------------
# FUNÇÃO PARA CHECAR ADMIN
# -------------------------------
def check_admin():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Acesso negado'}), 403
    return None

# -------------------------------
# CRUD ARMAS
# -------------------------------
@resources_bp.route('/weapons', methods=['GET'])
@login_required
def get_weapons():
    with get_db() as conn:
        weapons = conn.execute('SELECT * FROM weapons').fetchall()
    return jsonify([dict(weapon) for weapon in weapons])

@resources_bp.route('/weapons', methods=['POST'])
@login_required
def add_weapon():
    if check_admin():
        return check_admin()

    data = request.get_json()
    with get_db() as conn:
        cursor = conn.execute(
            'INSERT INTO weapons (name, category, date) VALUES (?, ?, ?)',
            (data['name'], data['category'], datetime.now().strftime('%Y-%m-%d'))
        )
        conn.commit()
        weapon_id = cursor.lastrowid
    return jsonify({'message': "Arma adicionada com sucesso", 'id': weapon_id})

@resources_bp.route('/weapons/<int:id>', methods=['PUT'])
@login_required
def update_weapon(id):
    if check_admin():
        return check_admin()

    data = request.get_json()
    with get_db() as conn:
        cursor = conn.execute(
            'UPDATE weapons SET name = ?, category = ? WHERE id = ?',
            (data['name'], data['category'], id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Arma não encontrada'}), 404
    return jsonify({'message': 'Atualização efetuada.'})

@resources_bp.route('/weapons/<int:id>', methods=['DELETE'])
@login_required
def delete_weapon(id):
    if check_admin():
        return check_admin()

    with get_db() as conn:
        cursor = conn.execute('DELETE FROM weapons WHERE id = ?', (id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Arma não encontrada'}), 404
    return jsonify({'message': 'Arma deletada.'})

# -------------------------------
# CRUD VEÍCULOS
# -------------------------------
@resources_bp.route('/vehicles', methods=['GET'])
@login_required
def get_vehicles():
    with get_db() as conn:
        vehicles = conn.execute('SELECT * FROM vehicles').fetchall()
    return jsonify([dict(vehicle) for vehicle in vehicles])

@resources_bp.route('/vehicles', methods=['POST'])
@login_required
def add_vehicle():
    if check_admin():
        return check_admin()

    data = request.get_json()
    with get_db() as conn:
        cursor = conn.execute(
            'INSERT INTO vehicles (model, plate, date) VALUES (?, ?, ?)',
            (data['model'], data['plate'], datetime.now().strftime('%Y-%m-%d'))
        )
        conn.commit()
        vehicle_id = cursor.lastrowid
    return jsonify({'message': "Veículo adicionado com sucesso", 'id': vehicle_id})

@resources_bp.route('/vehicles/<int:id>', methods=['PUT'])
@login_required
def update_vehicle(id):
    if check_admin():
        return check_admin()

    data = request.get_json()
    with get_db() as conn:
        cursor = conn.execute(
            'UPDATE vehicles SET model = ?, plate = ? WHERE id = ?',
            (data['model'], data['plate'], id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Veículo não encontrado'}), 404
    return jsonify({'message': 'Atualização efetuada.'})

@resources_bp.route('/vehicles/<int:id>', methods=['DELETE'])
@login_required
def delete_vehicle(id):
    if check_admin():
        return check_admin()

    with get_db() as conn:
        cursor = conn.execute('DELETE FROM vehicles WHERE id = ?', (id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Veículo não encontrado'}), 404
    return jsonify({'message': 'Veículo deletado.'})

# -------------------------------
# CRUD ITENS
# -------------------------------
@resources_bp.route('/items', methods=['GET'])
@login_required
def get_items():
    with get_db() as conn:
        items = conn.execute('SELECT * FROM items').fetchall()
    return jsonify([dict(item) for item in items])

@resources_bp.route('/items', methods=['POST'])
@login_required
def add_item():
    if check_admin():
        return check_admin()

    data = request.get_json()
    with get_db() as conn:
        cursor = conn.execute(
            'INSERT INTO items (name, category, date, quantity) VALUES (?, ?, ?, ?)',
            (data['name'], data['category'], datetime.now().strftime('%Y-%m-%d'), data['quantity'])
        )
        conn.commit()
        item_id = cursor.lastrowid
    return jsonify({'message': "Item adicionado com sucesso", 'id': item_id})

@resources_bp.route('/items/<int:id>', methods=['PUT'])
@login_required
def update_item(id):
    if check_admin():
        return check_admin()

    data = request.get_json()
    with get_db() as conn:
        cursor = conn.execute(
            'UPDATE items SET name = ?, category = ?, quantity = ? WHERE id = ?',
            (data['name'], data['category'], data['quantity'], id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Item não encontrado'}), 404
    return jsonify({'message': 'Atualização efetuada.'})

@resources_bp.route('/items/<int:id>', methods=['DELETE'])
@login_required
def delete_item(id):
    if check_admin():
        return check_admin()

    with get_db() as conn:
        cursor = conn.execute('DELETE FROM items WHERE id = ?', (id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Item não encontrado'}), 404
    return jsonify({'message': 'Item deletado.'})
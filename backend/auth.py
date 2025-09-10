from flask import Blueprint, request, jsonify, session
from database import get_db
import functools

auth_bp = Blueprint('auth', __name__)

def login_required(view):
    @functools.wraps(view) #decorator 
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Acesso não autorizado'}), 401
        return view(**kwargs)
    return wrapped_view

@auth_bp.route('/login', methods=['POST']) #cria uma rota login que aceita somente o método post (envia dados)
def login():
    data = request.get_json() #pega os dados enviados em json pelo front-end
    username = data.get('username')
    password = data.get('password')

    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', #? é um placeholder para evitar ataques de SQL injection
                        (username, password)
                        ).fetchone() #pega somente um resultado
    conn.close()

    if user:
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']

        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'role': user['role']
            }
        })
    else:
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout realizado com sucesso'}) 

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': session['user_id'],
                'username': session['username'],
                'role': session['role']
            }
        })
    return jsonify({'authenticated': False})

@auth_bp.route('/register', methods=['POST'])
@login_required
def register():
    # só admin pode cadastrar novos usuários
    if session.get('role') != 'admin':
        return jsonify({'error': 'Acesso negado'}), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')  # 'manager' ou 'contributor'

    if not username or not password or not role:
        return jsonify({'error': 'Preencha todos os campos'}), 400

    conn = get_db()
    # verifica se usuário já existe
    existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if existing_user:
        conn.close()
        return jsonify({'error': 'Usuário já existe'}), 400

    # insere usuário
    conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                 (username, password, role))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Usuário cadastrado com sucesso'})

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
import hashlib
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'database/users.db'

# Hierarquia de permissões
ROLES = {
    'OWNER': 4,
    'SUPER_ADMIN': 3,
    'ADMIN': 2,
    'USER': 1
}

def get_db():
    """Conecta ao banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa o banco de dados"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Criar tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            active INTEGER DEFAULT 1,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # Criar tabela de logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Verificar se já existe um OWNER
    cursor.execute("SELECT * FROM users WHERE role = 'OWNER'")
    owner = cursor.fetchone()
    
    if not owner:
        # Criar usuário OWNER padrão
        password = hashlib.sha256('pato123'.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ('pato', password, 'OWNER')
        )
        print("Usuário OWNER criado: pato / pato123")
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Cria hash da senha"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    """Decorator para verificar se usuário está logado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(min_role):
    """Decorator para verificar nível de permissão"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            
            user_role = session.get('role')
            if ROLES.get(user_role, 0) < ROLES.get(min_role, 0):
                flash('Você não tem permissão para acessar esta página.', 'error')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def log_action(user_id, action, details=''):
    """Registra ação no log"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (user_id, action, details) VALUES (?, ?, ?)",
        (user_id, action, details)
    )
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Redireciona para login ou dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND active = 1",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user and user['password'] == hash_password(password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            log_action(user['id'], 'LOGIN', f'Usuário {username} fez login')
            
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Faz logout do usuário"""
    user_id = session.get('user_id')
    username = session.get('username')
    
    if user_id:
        log_action(user_id, 'LOGOUT', f'Usuário {username} fez logout')
    
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal do sistema"""
    return render_template('dashboard.html')

@app.route('/admin')
@role_required('ADMIN')
def admin_panel():
    """Painel administrativo"""
    conn = get_db()
    cursor = conn.cursor()
    
    user_role = session.get('role')
    user_id = session.get('user_id')
    
    # Filtrar usuários baseado na hierarquia
    if user_role == 'OWNER':
        cursor.execute("SELECT * FROM users ORDER BY id DESC")
    elif user_role == 'SUPER_ADMIN':
        cursor.execute("SELECT * FROM users WHERE role IN ('ADMIN', 'USER') ORDER BY id DESC")
    elif user_role == 'ADMIN':
        cursor.execute("SELECT * FROM users WHERE role = 'USER' ORDER BY id DESC")
    else:
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    
    users = cursor.fetchall()
    conn.close()
    
    return render_template('admin.html', users=users)

@app.route('/admin/create_user', methods=['POST'])
@role_required('ADMIN')
def create_user():
    """Cria novo usuário"""
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    
    user_role = session.get('role')
    user_id = session.get('user_id')
    
    # Verificar permissões de criação
    if user_role == 'ADMIN' and role != 'USER':
        flash('Você só pode criar usuários do tipo USER.', 'error')
        return redirect(url_for('admin_panel'))
    
    if user_role == 'SUPER_ADMIN' and role not in ['ADMIN', 'USER']:
        flash('Você só pode criar usuários do tipo ADMIN ou USER.', 'error')
        return redirect(url_for('admin_panel'))
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, role, created_by) VALUES (?, ?, ?, ?)",
            (username, hash_password(password), role, user_id)
        )
        conn.commit()
        conn.close()
        
        log_action(user_id, 'CREATE_USER', f'Criou usuário {username} com role {role}')
        flash(f'Usuário {username} criado com sucesso!', 'success')
    except sqlite3.IntegrityError:
        flash('Usuário já existe!', 'error')
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/edit_user/<int:user_id>', methods=['POST'])
@role_required('ADMIN')
def edit_user(user_id):
    """Edita usuário existente"""
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    
    current_user_role = session.get('role')
    current_user_id = session.get('user_id')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Verificar se pode editar este usuário
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    target_user = cursor.fetchone()
    
    if not target_user:
        flash('Usuário não encontrado!', 'error')
        conn.close()
        return redirect(url_for('admin_panel'))
    
    # Verificar hierarquia
    if current_user_role == 'ADMIN' and target_user['role'] != 'USER':
        flash('Você só pode editar usuários do tipo USER.', 'error')
        conn.close()
        return redirect(url_for('admin_panel'))
    
    if current_user_role == 'SUPER_ADMIN' and target_user['role'] not in ['ADMIN', 'USER']:
        flash('Você só pode editar usuários do tipo ADMIN ou USER.', 'error')
        conn.close()
        return redirect(url_for('admin_panel'))
    
    # Atualizar usuário
    if password:
        cursor.execute(
            "UPDATE users SET username = ?, password = ?, role = ? WHERE id = ?",
            (username, hash_password(password), role, user_id)
        )
    else:
        cursor.execute(
            "UPDATE users SET username = ?, role = ? WHERE id = ?",
            (username, role, user_id)
        )
    
    conn.commit()
    conn.close()
    
    log_action(current_user_id, 'EDIT_USER', f'Editou usuário {username} (ID: {user_id})')
    flash(f'Usuário {username} atualizado com sucesso!', 'success')
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@role_required('ADMIN')
def delete_user(user_id):
    """Deleta usuário"""
    current_user_role = session.get('role')
    current_user_id = session.get('user_id')
    
    if user_id == current_user_id:
        flash('Você não pode deletar sua própria conta!', 'error')
        return redirect(url_for('admin_panel'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Verificar se pode deletar este usuário
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    target_user = cursor.fetchone()
    
    if not target_user:
        flash('Usuário não encontrado!', 'error')
        conn.close()
        return redirect(url_for('admin_panel'))
    
    # Verificar hierarquia
    if current_user_role == 'ADMIN' and target_user['role'] != 'USER':
        flash('Você só pode deletar usuários do tipo USER.', 'error')
        conn.close()
        return redirect(url_for('admin_panel'))
    
    if current_user_role == 'SUPER_ADMIN' and target_user['role'] not in ['ADMIN', 'USER']:
        flash('Você só pode deletar usuários do tipo ADMIN ou USER.', 'error')
        conn.close()
        return redirect(url_for('admin_panel'))
    
    username = target_user['username']
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    log_action(current_user_id, 'DELETE_USER', f'Deletou usuário {username} (ID: {user_id})')
    flash(f'Usuário {username} deletado com sucesso!', 'success')
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/logs')
@role_required('SUPER_ADMIN')
def view_logs():
    """Visualiza logs do sistema"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT logs.*, users.username 
        FROM logs 
        LEFT JOIN users ON logs.user_id = users.id 
        ORDER BY logs.timestamp DESC 
        LIMIT 100
    ''')
    logs = cursor.fetchall()
    conn.close()
    
    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

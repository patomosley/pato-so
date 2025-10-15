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
    """Inicializa o banco de dados com sistema de grupos"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Criar tabela de grupos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
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
            last_seen TIMESTAMP,
            is_online INTEGER DEFAULT 0,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # Criar tabela de relação usuário-grupo (muitos para muitos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            assigned_by INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE,
            FOREIGN KEY (assigned_by) REFERENCES users (id),
            UNIQUE(user_id, group_id)
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
        password = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ('admin', password, 'OWNER')
        )
        owner_id = cursor.lastrowid
        
        # Criar grupo padrão
        cursor.execute(
            "INSERT INTO groups (name, description, created_by) VALUES (?, ?, ?)",
            ('Grupo Padrão', 'Grupo inicial do sistema', owner_id)
        )
        group_id = cursor.lastrowid
        
        # Adicionar OWNER ao grupo padrão
        cursor.execute(
            "INSERT INTO user_groups (user_id, group_id, assigned_by) VALUES (?, ?, ?)",
            (owner_id, group_id, owner_id)
        )
        
        print("Usuário OWNER criado: admin / admin123")
        print("Grupo Padrão criado")
    
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

def update_user_status(user_id, is_online=True):
    """Atualiza status online do usuário"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET is_online = ?, last_seen = CURRENT_TIMESTAMP WHERE id = ?",
        (1 if is_online else 0, user_id)
    )
    conn.commit()
    conn.close()

def get_user_groups(user_id):
    """Retorna os grupos do usuário"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT g.* FROM groups g
        INNER JOIN user_groups ug ON g.id = ug.group_id
        WHERE ug.user_id = ?
    ''', (user_id,))
    groups = cursor.fetchall()
    conn.close()
    return groups

def get_group_users(group_id):
    """Retorna usuários de um grupo"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT u.* FROM users u
        INNER JOIN user_groups ug ON u.id = ug.user_id
        WHERE ug.group_id = ? AND u.active = 1
        ORDER BY u.role DESC, u.username
    ''', (group_id,))
    users = cursor.fetchall()
    conn.close()
    return users

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
            
            update_user_status(user['id'], True)
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
        update_user_status(user_id, False)
        log_action(user_id, 'LOGOUT', f'Usuário {username} fez logout')
    
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal do sistema com painel de grupos"""
    user_id = session.get('user_id')
    user_role = session.get('role')
    
    # Atualizar status online
    update_user_status(user_id, True)
    
    # Obter grupos do usuário
    user_groups = get_user_groups(user_id)
    
    # Obter usuários dos grupos
    groups_data = []
    for group in user_groups:
        group_users = get_group_users(group['id'])
        groups_data.append({
            'group': group,
            'users': group_users
        })
    
    return render_template('dashboard.html', groups_data=groups_data)

@app.route('/padroes-saski')
@login_required
def padroes_saski():
    """Página de Padrões SASKI (Gerador de Chamados)"""
    user_id = session.get('user_id')
    update_user_status(user_id, True)
    return render_template('padroes_saski.html')

@app.route('/admin/groups')
@role_required('OWNER')
def manage_groups():
    """Gerenciar grupos (apenas OWNER)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM groups ORDER BY name")
    groups = cursor.fetchall()
    conn.close()
    
    return render_template('manage_groups.html', groups=groups)

@app.route('/admin/groups/create', methods=['POST'])
@role_required('OWNER')
def create_group():
    """Criar novo grupo"""
    name = request.form.get('name')
    description = request.form.get('description')
    user_id = session.get('user_id')
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO groups (name, description, created_by) VALUES (?, ?, ?)",
            (name, description, user_id)
        )
        conn.commit()
        conn.close()
        
        log_action(user_id, 'CREATE_GROUP', f'Criou grupo {name}')
        flash(f'Grupo "{name}" criado com sucesso!', 'success')
    except sqlite3.IntegrityError:
        flash('Grupo já existe!', 'error')
    
    return redirect(url_for('manage_groups'))

@app.route('/admin')
@role_required('ADMIN')
def admin_panel():
    """Painel administrativo com filtro por grupo"""
    conn = get_db()
    cursor = conn.cursor()
    
    user_role = session.get('role')
    user_id = session.get('user_id')
    
    if user_role == 'OWNER':
        # OWNER vê todos os usuários
        cursor.execute("SELECT * FROM users ORDER BY id DESC")
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM groups ORDER BY name")
        all_groups = cursor.fetchall()
    else:
        # Super Admin e Admin veem apenas usuários dos seus grupos
        user_groups = get_user_groups(user_id)
        group_ids = [g['id'] for g in user_groups]
        
        if group_ids:
            placeholders = ','.join('?' * len(group_ids))
            
            if user_role == 'SUPER_ADMIN':
                cursor.execute(f'''
                    SELECT DISTINCT u.* FROM users u
                    INNER JOIN user_groups ug ON u.id = ug.user_id
                    WHERE ug.group_id IN ({placeholders})
                    AND u.role IN ('ADMIN', 'USER')
                    ORDER BY u.id DESC
                ''', group_ids)
            else:  # ADMIN
                cursor.execute(f'''
                    SELECT DISTINCT u.* FROM users u
                    INNER JOIN user_groups ug ON u.id = ug.user_id
                    WHERE ug.group_id IN ({placeholders})
                    AND u.role = 'USER'
                    ORDER BY u.id DESC
                ''', group_ids)
            
            users = cursor.fetchall()
            cursor.execute(f"SELECT * FROM groups WHERE id IN ({placeholders}) ORDER BY name", group_ids)
            all_groups = cursor.fetchall()
        else:
            users = []
            all_groups = []
    
    # Obter grupos de cada usuário
    users_with_groups = []
    for user in users:
        user_groups_list = get_user_groups(user['id'])
        users_with_groups.append({
            'user': user,
            'groups': user_groups_list
        })
    
    conn.close()
    
    return render_template('admin.html', users_with_groups=users_with_groups, all_groups=all_groups)

@app.route('/admin/create_user', methods=['POST'])
@role_required('ADMIN')
def create_user():
    """Cria novo usuário e atribui aos grupos"""
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    group_ids = request.form.getlist('groups')  # Lista de grupos
    
    user_role = session.get('role')
    user_id = session.get('user_id')
    
    # Verificar permissões de criação
    if user_role == 'ADMIN' and role != 'USER':
        flash('Você só pode criar usuários do tipo USER.', 'error')
        return redirect(url_for('admin_panel'))
    
    if user_role == 'SUPER_ADMIN' and role not in ['ADMIN', 'USER']:
        flash('Você só pode criar usuários do tipo ADMIN ou USER.', 'error')
        return redirect(url_for('admin_panel'))
    
    # OWNER pode criar qualquer cargo, incluindo outros OWNERs
    
    # Se não for OWNER, usar grupos do criador
    if user_role != 'OWNER':
        creator_groups = get_user_groups(user_id)
        group_ids = [str(g['id']) for g in creator_groups]
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, role, created_by) VALUES (?, ?, ?, ?)",
            (username, hash_password(password), role, user_id)
        )
        new_user_id = cursor.lastrowid
        
        # Adicionar usuário aos grupos
        for group_id in group_ids:
            cursor.execute(
                "INSERT INTO user_groups (user_id, group_id, assigned_by) VALUES (?, ?, ?)",
                (new_user_id, int(group_id), user_id)
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
    group_ids = request.form.getlist('groups')
    
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
    
    # Verificar hierarquia (OWNER pode editar qualquer um, incluindo outros OWNERs)
    if current_user_role == 'ADMIN' and target_user['role'] != 'USER':
        flash('Você só pode editar usuários do tipo USER.', 'error')
        conn.close()
        return redirect(url_for('admin_panel'))
    
    if current_user_role == 'SUPER_ADMIN' and target_user['role'] not in ['ADMIN', 'USER']:
        flash('Você só pode editar usuários do tipo ADMIN ou USER.', 'error')
        conn.close()
        return redirect(url_for('admin_panel'))
    
    # OWNER pode editar qualquer cargo, incluindo outros OWNERs
    
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
    
    # Atualizar grupos (apenas OWNER pode alterar)
    if current_user_role == 'OWNER' and group_ids:
        # Remover grupos antigos
        cursor.execute("DELETE FROM user_groups WHERE user_id = ?", (user_id,))
        
        # Adicionar novos grupos
        for group_id in group_ids:
            cursor.execute(
                "INSERT INTO user_groups (user_id, group_id, assigned_by) VALUES (?, ?, ?)",
                (user_id, int(group_id), current_user_id)
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
    
    # Verificar hierarquia (OWNER pode deletar qualquer um, incluindo outros OWNERs)
    if current_user_role == 'ADMIN' and target_user['role'] != 'USER':
        flash('Você só pode deletar usuários do tipo USER.', 'error')
        conn.close()
        return redirect(url_for('admin_panel'))
    
    if current_user_role == 'SUPER_ADMIN' and target_user['role'] not in ['ADMIN', 'USER']:
        flash('Você só pode deletar usuários do tipo ADMIN ou USER.', 'error')
        conn.close()
        return redirect(url_for('admin_panel'))
    
    # OWNER pode deletar qualquer cargo, incluindo outros OWNERs
    
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

@app.route('/api/group_users/<int:group_id>')
@login_required
def api_group_users(group_id):
    """API para obter usuários de um grupo com status online"""
    users = get_group_users(group_id)
    users_list = []
    for user in users:
        users_list.append({
            'id': user['id'],
            'username': user['username'],
            'role': user['role'],
            'is_online': user['is_online'],
            'last_seen': user['last_seen']
        })
    return jsonify(users_list)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)


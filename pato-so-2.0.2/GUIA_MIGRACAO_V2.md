# 🔄 Guia de Migração - Versão 2.0

## ⚠️ Importante: Leia Antes de Atualizar

A **Versão 2.0** introduz mudanças significativas no banco de dados. Este guia ajudará você a migrar do sistema antigo para o novo.

---

## 📋 O Que Mudou

A principal mudança é a introdução do **Sistema de Grupos**:

- Banco de dados foi reestruturado
- Novas tabelas: `groups` e `user_groups`
- Tabela `users` ganhou campos `last_seen` e `is_online`
- Hierarquia de permissões agora considera grupos

---

## 🚀 Passo a Passo da Migração

### Opção 1: Instalação Limpa (Recomendado)

Se você está começando ou não tem muitos usuários:

1. **Pare o servidor antigo:**
   ```bash
   # Identifique o processo
   ps aux | grep python | grep app.py
   
   # Mate o processo (substitua PID pelo número encontrado)
   kill -9 PID
   ```

2. **Faça backup do banco antigo:**
   ```bash
   cd /seu/caminho/pato-so-system
   cp -r database database_backup_v1
   ```

3. **Remova o banco antigo:**
   ```bash
   rm -rf database
   mkdir database
   ```

4. **Substitua os arquivos:**
   - Descompacte o `pato-so-system-v2.zip`
   - Substitua todos os arquivos

5. **Inicie o novo servidor:**
   ```bash
   python3 app.py
   ```

6. **Faça login:**
   - Usuário: `admin`
   - Senha: `admin123`

7. **Configure os grupos:**
   - Acesse "Gerenciar Grupos"
   - Crie os grupos necessários
   - Recrie os usuários e atribua aos grupos

---

### Opção 2: Migração Manual de Dados

Se você tem muitos usuários e quer preservar os dados:

#### Passo 1: Exportar Usuários Antigos

Execute este script Python para exportar:

```python
import sqlite3
import json

conn = sqlite3.connect('database_backup_v1/users.db')
cursor = conn.cursor()
cursor.execute("SELECT username, role FROM users")
users = cursor.fetchall()

with open('users_backup.json', 'w') as f:
    json.dump([{'username': u[0], 'role': u[1]} for u in users], f, indent=2)

print(f"Exportados {len(users)} usuários")
conn.close()
```

#### Passo 2: Iniciar Sistema Novo

```bash
# Remover banco antigo
rm -rf database
mkdir database

# Iniciar servidor (cria banco novo)
python3 app.py
```

#### Passo 3: Importar Usuários

Execute este script para importar:

```python
import sqlite3
import hashlib
import json

# Ler backup
with open('users_backup.json', 'r') as f:
    users = json.load(f)

# Conectar ao novo banco
conn = sqlite3.connect('database/users.db')
cursor = conn.cursor()

# Obter ID do OWNER e grupo padrão
cursor.execute("SELECT id FROM users WHERE role = 'OWNER'")
owner_id = cursor.fetchone()[0]

cursor.execute("SELECT id FROM groups WHERE name = 'Grupo Padrão'")
group_id = cursor.fetchone()[0]

# Importar usuários (exceto admin que já existe)
for user in users:
    if user['username'] == 'admin':
        continue
    
    # Senha padrão: username123
    password = hashlib.sha256(f"{user['username']}123".encode()).hexdigest()
    
    try:
        # Criar usuário
        cursor.execute(
            "INSERT INTO users (username, password, role, created_by) VALUES (?, ?, ?, ?)",
            (user['username'], password, user['role'], owner_id)
        )
        user_id = cursor.lastrowid
        
        # Adicionar ao grupo padrão
        cursor.execute(
            "INSERT INTO user_groups (user_id, group_id, assigned_by) VALUES (?, ?, ?)",
            (user_id, group_id, owner_id)
        )
        
        print(f"✓ Importado: {user['username']} ({user['role']})")
    except sqlite3.IntegrityError:
        print(f"✗ Já existe: {user['username']}")

conn.commit()
conn.close()
print("\n✅ Migração concluída!")
```

---

## 🔐 Senhas Padrão

Após a migração, todos os usuários terão senhas padrão:

- **Formato:** `{username}123`
- **Exemplo:** Usuário `joao` → Senha `joao123`

**Importante:** Peça aos usuários para alterarem suas senhas!

---

## ✅ Checklist Pós-Migração

- [ ] Servidor iniciou sem erros
- [ ] Login com admin/admin123 funciona
- [ ] "Grupo Padrão" aparece no banco
- [ ] Consegue criar novos grupos
- [ ] Consegue criar novos usuários
- [ ] Dashboard mostra painel de grupos
- [ ] Status online/offline funciona
- [ ] Todos os usuários foram recriados
- [ ] Permissões estão corretas

---

## 🐛 Problemas Comuns

### Erro: "Table already exists"

**Solução:** O banco antigo não foi removido.
```bash
rm -rf database
mkdir database
python3 app.py
```

### Erro: "No such table: groups"

**Solução:** O banco não foi criado corretamente.
```bash
# Pare o servidor
# Delete o banco
rm database/users.db
# Reinicie
python3 app.py
```

### Não consigo fazer login

**Solução:** Use as credenciais padrão:
- Usuário: `admin`
- Senha: `admin123`

### Painel de grupos não aparece

**Solução:** 
1. Verifique se o usuário está em algum grupo
2. Acesse "Gerenciar Grupos" (OWNER)
3. Verifique se há grupos criados

---

## 📊 Estrutura do Novo Banco

### Tabelas

```
users
├── id
├── username
├── password
├── role
├── created_at
├── created_by
├── active
├── last_seen (NOVO)
└── is_online (NOVO)

groups (NOVO)
├── id
├── name
├── description
├── created_at
└── created_by

user_groups (NOVO)
├── id
├── user_id
├── group_id
├── assigned_at
└── assigned_by

logs
├── id
├── user_id
├── action
├── details
└── timestamp
```

---

## 🔄 Rollback (Voltar para V1)

Se algo der errado e você quiser voltar:

1. **Pare o servidor V2**
2. **Restaure o backup:**
   ```bash
   rm -rf database
   cp -r database_backup_v1 database
   ```
3. **Restaure os arquivos antigos**
4. **Inicie o servidor antigo**

---

## 💡 Dicas

### Criar Grupos Estratégicos

Pense na estrutura da sua organização:

- **Por Departamento:** TI, RH, Financeiro, Operações
- **Por Localização:** Matriz, Filial A, Filial B
- **Por Projeto:** Projeto X, Projeto Y, Projeto Z
- **Por Turno:** Manhã, Tarde, Noite

### Atribuir Múltiplos Grupos

Um usuário pode estar em vários grupos:

- Exemplo: João pode estar em "TI" e "Projeto X"
- Ele verá usuários de ambos os grupos no dashboard

### Hierarquia Recomendada

```
OWNER (1 pessoa)
└── SUPER ADMIN (2-3 pessoas por área)
    └── ADMIN (5-10 pessoas por setor)
        └── USER (todos os demais)
```

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique o arquivo `server.log`
2. Consulte o `CHANGELOG_V2.md`
3. Leia o `README.md`

---

**Boa migração! 🚀**


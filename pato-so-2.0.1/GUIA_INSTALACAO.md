# 📘 Guia de Instalação e Uso - PATO SO

## 🎯 Visão Geral

O **PATO SO** é um sistema completo de gerenciamento com autenticação, controle de permissões hierárquico e dashboard integrado para gerenciar chamados e acessar sistemas corporativos.

## 🔧 Instalação

### Passo 1: Requisitos do Sistema

Certifique-se de ter instalado:
- Python 3.7 ou superior
- pip3 (gerenciador de pacotes Python)

### Passo 2: Instalar Dependências

```bash
pip3 install flask
```

### Passo 3: Executar o Sistema

```bash
cd /home/ubuntu/pato-so-system
python3 app.py
```

O sistema iniciará em: **http://localhost:5000**

### Passo 4: Primeiro Acesso

Use as credenciais padrão:
- **Usuário:** `admin`
- **Senha:** `admin123`

⚠️ **IMPORTANTE:** Altere a senha após o primeiro login!

## 👥 Hierarquia de Usuários

### 🔴 OWNER (Proprietário)
**Permissões:**
- ✅ Criar, editar e excluir TODOS os usuários
- ✅ Gerenciar Super Admins, Admins e Users
- ✅ Acesso total aos logs do sistema
- ✅ Controle completo do sistema

**Casos de Uso:**
- Administrador principal do sistema
- Configuração inicial
- Gerenciamento de Super Admins

### 🟣 SUPER ADMIN (Super Administrador)
**Permissões:**
- ✅ Criar, editar e excluir Admins e Users
- ✅ Acesso aos logs do sistema
- ❌ Não pode gerenciar OWNER

**Casos de Uso:**
- Gerente de TI
- Coordenador de equipe
- Gestão de administradores regionais

### 🔵 ADMIN (Administrador)
**Permissões:**
- ✅ Criar, editar e excluir apenas Users
- ✅ Acesso ao painel administrativo
- ❌ Não pode gerenciar Super Admins ou OWNER

**Casos de Uso:**
- Supervisor de equipe
- Líder de projeto
- Gestão de usuários operacionais

### ⚪ USER (Usuário)
**Permissões:**
- ✅ Acesso ao dashboard e funcionalidades do sistema
- ❌ Não pode gerenciar outros usuários

**Casos de Uso:**
- Operadores
- Técnicos
- Usuários finais do sistema

## 🚀 Como Usar

### 1. Login no Sistema

1. Acesse **http://localhost:5000**
2. Digite seu usuário e senha
3. Clique em **Entrar**

### 2. Dashboard Principal

Após o login, você verá:
- **Menu lateral** com todas as categorias
- **Gerador de chamados SASKI**
- **Botão de tema** (claro/escuro) no canto superior direito

### 3. Gerar Chamado SASKI

1. Preencha o **Nome do Cliente**
2. Digite o **Código de Contrato**
3. Selecione o **Setor**
4. Escolha o **Tipo de Solicitação**
5. Clique em **Gerar Chamado**
6. Use os botões de copiar para título e descrição

### 4. Gerenciar Usuários (Admin+)

#### Criar Novo Usuário

1. Acesse **Gerenciar Usuários** no menu
2. Clique em **➕ Criar Novo Usuário**
3. Preencha:
   - Usuário
   - Senha
   - Cargo (conforme sua permissão)
4. Clique em **Criar Usuário**

#### Editar Usuário

1. Na lista de usuários, localize o usuário
2. Clique em **✏️ Editar**
3. Modifique os dados necessários
4. Deixe a senha em branco para manter a atual
5. Clique em **Salvar Alterações**

#### Deletar Usuário

1. Na lista de usuários, localize o usuário
2. Clique em **🗑️ Deletar**
3. Confirme a exclusão

⚠️ **Atenção:** A exclusão é permanente!

### 5. Visualizar Logs (Super Admin+)

1. Acesse **Logs do Sistema** no menu
2. Visualize todas as ações realizadas:
   - Logins
   - Criação de usuários
   - Edição de usuários
   - Exclusão de usuários

## 🎨 Personalização

### Tema Claro/Escuro

- Clique no botão **🌙** (lua) para ativar tema escuro
- Clique no botão **☀️** (sol) para ativar tema claro
- A preferência é salva automaticamente

### Adicionar Novos Setores

Edite o arquivo `static/js/dashboard.js`:

```javascript
const tipos = {
    "NOVO_SETOR": ["TIPO1", "TIPO2", "TIPO3"]
};

const descricoes = {
    "NOVO_SETOR": {
        "TIPO1": "Descrição completa do tipo 1"
    }
};
```

### Adicionar Links no Menu

Edite o arquivo `templates/sidebar.html`:

```html
<div class="menu-category">
    <h3 onclick="toggleMenu(this)">
        <span class="menu-icon">🔗</span>
        <span class="menu-text">Nova Categoria</span>
        <span class="arrow">▼</span>
    </h3>
    <div class="submenu">
        <a href="/seu-link">Nome do Link</a>
    </div>
</div>
```

## 🔒 Segurança

### Boas Práticas

1. **Altere a senha padrão** imediatamente
2. **Use senhas fortes** (mínimo 8 caracteres)
3. **Não compartilhe credenciais** entre usuários
4. **Revise os logs** regularmente
5. **Remova usuários inativos** periodicamente

### Recuperação de Senha

Se esquecer a senha do OWNER:

1. Pare o servidor
2. Delete o banco de dados:
   ```bash
   rm database/users.db
   ```
3. Reinicie o servidor (criará novo OWNER com senha padrão)

## 📊 Estrutura de Dados

### Tabela de Usuários

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | ID único do usuário |
| username | TEXT | Nome de usuário (único) |
| password | TEXT | Hash SHA-256 da senha |
| role | TEXT | Cargo (OWNER/SUPER_ADMIN/ADMIN/USER) |
| created_at | TIMESTAMP | Data de criação |
| created_by | INTEGER | ID do criador |
| active | INTEGER | Status (1=ativo, 0=inativo) |

### Tabela de Logs

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | ID único do log |
| user_id | INTEGER | ID do usuário |
| action | TEXT | Tipo de ação |
| details | TEXT | Detalhes da ação |
| timestamp | TIMESTAMP | Data/hora da ação |

## 🐛 Solução de Problemas

### Erro: "Address already in use"

**Problema:** Porta 5000 já está em uso

**Solução:**
```bash
# Encontrar processo usando a porta
lsof -i :5000

# Matar o processo
kill -9 [PID]

# Ou alterar a porta no app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Erro: "No module named 'flask'"

**Problema:** Flask não está instalado

**Solução:**
```bash
pip3 install flask
```

### Banco de Dados Corrompido

**Problema:** Erros ao acessar o banco

**Solução:**
```bash
# Backup do banco atual
cp database/users.db database/users.db.backup

# Remover banco corrompido
rm database/users.db

# Reiniciar servidor (cria novo banco)
python3 app.py
```

### Não Consigo Fazer Login

**Problema:** Credenciais não funcionam

**Solução:**
1. Verifique se está usando as credenciais corretas
2. Verifique se o usuário está ativo
3. Consulte os logs do servidor
4. Em último caso, recrie o banco de dados

## 📱 Acesso Remoto

Para acessar de outros dispositivos na rede:

1. Descubra o IP do servidor:
   ```bash
   hostname -I
   ```

2. Acesse de outro dispositivo:
   ```
   http://[IP_DO_SERVIDOR]:5000
   ```

## 🔄 Atualização do Sistema

Para atualizar o sistema:

1. Faça backup do banco de dados:
   ```bash
   cp database/users.db database/users.db.backup
   ```

2. Substitua os arquivos do sistema

3. Reinicie o servidor

## 📞 Suporte

Para problemas ou dúvidas:
- Consulte os logs em `server.log`
- Verifique a documentação em `README.md`
- Entre em contato com o administrador do sistema

## ✅ Checklist de Instalação

- [ ] Python 3.7+ instalado
- [ ] Flask instalado
- [ ] Sistema executando sem erros
- [ ] Acesso à página de login funcionando
- [ ] Login com credenciais padrão bem-sucedido
- [ ] Senha padrão alterada
- [ ] Primeiro usuário adicional criado
- [ ] Temas claro/escuro funcionando
- [ ] Gerador de chamados testado
- [ ] Links do menu acessíveis

## 🎓 Próximos Passos

Após a instalação:

1. ✅ Altere a senha do OWNER
2. ✅ Crie usuários Super Admin
3. ✅ Configure os setores necessários
4. ✅ Adicione links personalizados
5. ✅ Teste todas as funcionalidades
6. ✅ Treine os usuários
7. ✅ Configure backup automático

---

**Versão:** 1.0  
**Data:** Outubro 2025  
**Sistema:** PATO SO - Padrões para Chamados SASKI

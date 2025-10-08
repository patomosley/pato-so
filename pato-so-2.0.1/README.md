# PATO SO - Sistema de Gerenciamento com Autenticação

Sistema completo de login e gerenciamento de usuários com hierarquia de permissões e dashboard integrado.

## 🚀 Características

### Sistema de Autenticação
- Login seguro com hash SHA-256
- Banco de dados SQLite
- Sessões persistentes
- Sistema de logs de atividades

### Hierarquia de Permissões

#### 🔴 OWNER
- Controle total do sistema
- Criar, editar e excluir todos os tipos de usuários
- Acesso a todos os logs
- Gerenciar Super Admins, Admins e Users

#### 🟣 SUPER ADMIN
- Gerenciar usuários Admin e User
- Criar, editar e excluir Admins e Users
- Acesso aos logs do sistema
- Não pode gerenciar OWNER

#### 🔵 ADMIN
- Gerenciar apenas usuários User
- Criar, editar e excluir Users
- Acesso ao painel administrativo
- Não pode gerenciar Super Admins ou OWNER

#### ⚪ USER
- Acesso apenas ao sistema principal
- Não pode gerenciar outros usuários
- Acesso ao dashboard e funcionalidades do PATO SO

### Dashboard Moderno
- Menu lateral responsivo com categorias
- Tema claro/escuro
- Integração com sistemas existentes:
  - Sistemas Revan
  - Suporte e Monitoramento
  - Sistema de Consulta
  - Solicitações de Material
  - SDWAN Fortinet
  - Solicitação SAP
- Gerador de chamados SASKI

## 📦 Instalação

### Requisitos
- Python 3.7+
- Flask

### Passos

1. Instalar dependências:
```bash
pip3 install flask
```

2. Executar o sistema:
```bash
cd /home/ubuntu/pato-so-system
python3 app.py
```

3. Acessar no navegador:
```
http://localhost:5000
```

## 🔐 Credenciais Padrão

**Usuário OWNER:**
- Usuário: `admin`
- Senha: `admin123`

⚠️ **IMPORTANTE:** Altere a senha padrão após o primeiro login!

## 📁 Estrutura do Projeto

```
pato-so-system/
├── app.py                 # Aplicação Flask principal
├── database/
│   └── users.db          # Banco de dados SQLite
├── templates/
│   ├── login.html        # Página de login
│   ├── dashboard.html    # Dashboard principal
│   ├── admin.html        # Painel administrativo
│   ├── logs.html         # Visualização de logs
│   └── sidebar.html      # Menu lateral compartilhado
├── static/
│   ├── css/
│   │   └── style.css     # Estilos principais
│   ├── js/
│   │   ├── dashboard.js  # Scripts do dashboard
│   │   └── admin.js      # Scripts do admin
│   └── images/
│       └── pato.png      # Ícone do sistema
└── README.md             # Este arquivo
```

## 🎨 Funcionalidades do Dashboard

### Gerador de Chamados SASKI
- Seleção de setor e tipo de solicitação
- Geração automática de título e descrição
- Copiar título e descrição separadamente
- Templates pré-configurados para cada tipo de chamado

### Setores Disponíveis
- GPON
- Monitoramento Suporte
- NOC-Engenharia
- NOC-OM
- NOC-SO
- Telefonia

## 👥 Gerenciamento de Usuários

### Criar Usuário
1. Acessar "Gerenciar Usuários"
2. Clicar em "Criar Novo Usuário"
3. Preencher dados (usuário, senha, cargo)
4. Confirmar criação

### Editar Usuário
1. Na lista de usuários, clicar em "Editar"
2. Modificar dados necessários
3. Deixar senha em branco para manter a atual
4. Salvar alterações

### Deletar Usuário
1. Na lista de usuários, clicar em "Deletar"
2. Confirmar exclusão
3. Usuário será removido permanentemente

## 📊 Logs do Sistema

Disponível para Super Admin e OWNER:
- Registro de logins
- Criação de usuários
- Edição de usuários
- Exclusão de usuários
- Timestamp de cada ação

## 🔒 Segurança

- Senhas armazenadas com hash SHA-256
- Validação de hierarquia em todas as operações
- Proteção contra auto-exclusão
- Sessões seguras com chave secreta
- Logs de auditoria completos

## 🎨 Temas

O sistema suporta tema claro e escuro:
- Botão de alternância no canto superior direito
- Preferência salva no localStorage
- Cores otimizadas para ambos os temas

## 📱 Responsividade

- Layout adaptável para mobile e desktop
- Menu lateral colapsável em telas pequenas
- Tabelas com scroll horizontal
- Modais otimizados para todas as telas

## 🔧 Personalização

### Adicionar Novos Setores
Editar `static/js/dashboard.js`:
```javascript
const tipos = {
    "NOVO_SETOR": ["TIPO1", "TIPO2", "TIPO3"]
};

const descricoes = {
    "NOVO_SETOR": {
        "TIPO1": "Descrição do tipo 1"
    }
};
```

### Adicionar Novos Links no Menu
Editar `templates/sidebar.html`:
```html
<div class="menu-category">
    <h3 onclick="toggleMenu(this)">
        <span class="menu-icon">🔗</span>
        <span class="menu-text">Nova Categoria</span>
        <span class="arrow">▼</span>
    </h3>
    <div class="submenu">
        <a href="/link">Nome do Link</a>
    </div>
</div>
```

## 🐛 Solução de Problemas

### Banco de dados não inicializa
```bash
rm database/users.db
python3 app.py
```

### Erro de permissão
Verificar se o usuário tem permissão para criar arquivos no diretório.

### Porta já em uso
Alterar a porta no final de `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📝 Licença

Sistema desenvolvido para uso interno.

## 👨‍💻 Suporte

Para dúvidas ou problemas, entre em contato com o administrador do sistema.

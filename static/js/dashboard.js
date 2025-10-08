// Dados de tipos por setor
const tipos = {
    "GPON": ["ATUALIZAR ONU", "CONFIGURAR VLAN", "TESTE DE P2P", "TESTE P2P L2L", "VERIFICAÇÃO DE ONU"],
    "MONITORAMENTO SUPORTE": ["ALTERAÇÃO IP UNIDADE CADASTRADA", "CADASTRO DE CIRCUITO"],
    "NOC-ENGENHARIA": ["VIABILIDADE PARA ATIVAÇÃO", "VIABILIDADE PARA UPGRADE"],
    "NOC-OM": ["ATIVAÇÃO DE INTERFACE", "RESERVA DE INTERFACE"],
    "NOC-SO": ["ALTERAR CONFIGURAÇÃO", "ALTERAR PLANO", "CANCELAMENTO DE CLIENTE", "CONFIGURAR IPT", "CONFIGURAR IPT SENCINET", "CONFIGURAR L2VPN", "CONFIGURAR L3VPN", "CONFIGURAR L3VPN ETICE", "BLOCO IP DE FORMA DIRETA", "BLOCO IP DE FORMA ROTEADA", "LIBERAR PREFIXOS", "REDE DE GERENCIA", "REMOVER FILTRO", "REVISAO DE CONFIGURAÇÃO", "SITE SEM ACESSO"],
    "TELEFONIA": ["ALTERAÇÃO DE LIMITE", "ATIVAÇÃO DE CLIENTE", "BLOQUEIO LIGAÇÕES INTERNACIONAIS", "BLOQUEIO LIGAÇÕES PARA NUMERO ESPECIFICO", "BLOQUEIO PARA LIGAÇÕES 0300/0500", "CANCELAMENTO", "DESBLOQUEIO LIGAÇÕES INTERNACIONAIS", "DESBLOQUEIO LIGAÇÕES PARA NUMERO ESPECIFICO", "DESBLOQUEIO PARA LIGAÇÕES 0300/0500", "EDD DOWN", "FALHA DE AUTENTICAÇÃO", "HISTORICO DE LIGAÇÕES", "LIMITADOR DE CONSUMO", "LIGAÇÃO FEITA FALHANDO", "NAO EFETUA LIGAÇÃO", "NAO RECEBE LIGAÇÕES", "SUPORTE INTERNO"]
};

// Descrições personalizadas por tipo e setor
const descricoes = {
    "GPON": {
        "ATUALIZAR ONU": "Verificar se ONU possui atualizações disponíveis, caso sim, realizar atualização da mesma\n\n*ONU:\n*OLT:",
        "CONFIGURAR VLAN": "Realizar configuração de VLAN\n\n*LAN:\n*VLAN:\n*OLT:",
        "TESTE DE P2P": "Configurar Rede na ONU e realizar teste de conexão entre o HOST e GW\n\n*REDE:\n*HOST:\n*GATEWAY:\n*VLAN:",
        "TESTE P2P L2L": "Realizar configuração de uma rede nas ONUs e realizar teste de ICMP entre as mesmas para testarmos a comunicação.\n\n*REDE:\n\nPONTA A\n*ONU:\n*VLAN:\n*HOST:\n\nPONTA B\n*ONU:\n*VLAN:\n*HOST:",
        "VERIFICAÇÃO DE ONU": "Peço para que seja realizada a verificação da ONU\nMotivo da verificação:"
    },
    "MONITORAMENTO SUPORTE": {
        "ALTERAÇÃO IP UNIDADE CADASTRADA": "Por gentileza, realizar alteração de monitoramento da unidade que já atendemos.",
        "CADASTRO DE CIRCUITO": "Realizar cadastro de unidade no monitoramento."
    },
    "NOC-ENGENHARIA": {
        "VIABILIDADE PARA ATIVAÇÃO": "    CNPJ:\n\nCOD CONTRATO:\n\nPor favor verificar se temos capacidade para atender ativação mediante dados informados.",
        "VIABILIDADE PARA UPGRADE": "CNPJ:\n\nCOD CONTRATO:\n\nPor favor verificar se temos capacidade para atender upgrade mediante dados informados."
    },
    "NOC-OM": {
        "ATIVAÇÃO DE INTERFACE": "Por gentileza, realizar configuração da interface, segue dados abaixo.\n\n*SWITCH:\n*INTERFACE:",
        "RESERVA DE INTERFACE": "Por gentileza, realizar reserva de interface para ativação do cliente."
    },
    "NOC-SO": {
        "ALTERAR CONFIGURAÇÃO": "Por favor realizar alteração de configuração\n\nMotivo:\n\n*DEVICE\n*INTERFACE:\n*VLAN:",
        "ALTERAR PLANO": "Realizar alteração de Plano do Cliente\n\n*VLAN:",
        "CANCELAMENTO DE CLIENTE": "Peço que seja removida a configuração do cliente mediante os dados informados\n\n*VLAN:",
        "CONFIGURAR IPT": "Peço que seja configurado o circuito BGP de acordo com os dados descritos\n\n*VLAN: A Definir\n*Cap. de Tráfego:\n*ASN:\n*CIDR v4:\n*CIDR v6:\n*Routing Table:\n*Radb:",
        "CONFIGURAR IPT SENCINET": "Peço para que seja realizado configuração do IPT do cliente Sencient\n\n*VLAN: A DEFINIR\n\n*LOCAL-PEER: \n*LOCAL-AS: 64999\n*REMOTE PEER:\n*REMOTE AS: 64765\n\n*LIMITE PREFIXO: 10",
        "CONFIGURAR L2VPN": "Peço que seja configurado o L2VPN com base nas informações descritas.\n\n*Vlan: A definir\n\nPonta A:\n*Cód Contrato:\n*Device:\n*Interface:\n\nPonta B:",
        "CONFIGURAR L3VPN": "Peço que seja configurado o L3VPN com base nas informações descritas.\n\n*Vlan: A Definir\n*Rede lan:",
        "CONFIGURAR L3VPN ETICE": "Peço que seja configurado o L3VPN com base nas informações descritas.\n\n*VRF:\n*Vlan: A Definir\n*Rede lan:",
        "BLOCO IP DE FORMA DIRETA": "Peço que seja configurado circuito IP de forma direta com base nas informações descritas\n\nVlan: A definir\nPeer Valido: A definir\nMáscara:",
        "BLOCO IP DE FORMA ROTEADA": "Peço que seja configurado circuito IP de forma roteada em um peer privado com base nas informações descritas\n\nVlan: A definir\nPeer Valido: A definir\nMáscara:\n\nPeer Privado: A Definir",
        "LIBERAR PREFIXOS": "Peço que sejam liberados os prefixos descritos abaixo:\n\n*ASN:\n*PREFIX V4:\n*PREFIX V6:\n*RADB:\n\nLiberar na policy do cliente a seguir\n\n*CLIENTE:\n*ASN:\n*VLAN:",
        "REDE DE GERENCIA": "Peço que seja configurado o circuito de gerência com base nas informações descritas\n\n*Vlan: A definir\n*Rede lan:",
        "REMOVER FILTRO": "Peço que seja removido o filtro do cliente mediante os dados informados\n\n*VLAN:",
        "REVISAO DE CONFIGURAÇÃO": "Peço que seja revisada a configuração do cliente mediante os dados informados\n\n*VLAN:",
        "SITE SEM ACESSO": "Peço que seja verificado o motivo do site estar sem acesso\n\n*VLAN:"
    },
    "TELEFONIA": {
        "ALTERAÇÃO DE LIMITE": "Peço que seja alterado o limite de consumo do cliente\n\n*LIMITE:",
        "ATIVAÇÃO DE CLIENTE": "Peço que seja ativado o cliente\n\n*RAMAL:\n*SENHA:",
        "BLOQUEIO LIGAÇÕES INTERNACIONAIS": "Peço que seja bloqueado as ligações internacionais do cliente",
        "BLOQUEIO LIGAÇÕES PARA NUMERO ESPECIFICO": "Peço que seja bloqueado as ligações para o número específico\n\n*NÚMERO:",
        "BLOQUEIO PARA LIGAÇÕES 0300/0500": "Peço que seja bloqueado as ligações para 0300/0500 do cliente",
        "CANCELAMENTO": "Peço que seja cancelado o cliente",
        "DESBLOQUEIO LIGAÇÕES INTERNACIONAIS": "Peço que seja desbloqueado as ligações internacionais do cliente",
        "DESBLOQUEIO LIGAÇÕES PARA NUMERO ESPECIFICO": "Peço que seja desbloqueado as ligações para o número específico\n\n*NÚMERO:",
        "DESBLOQUEIO PARA LIGAÇÕES 0300/0500": "Peço que seja desbloqueado as ligações para 0300/0500 do cliente",
        "EDD DOWN": "Peço que seja verificado o motivo do EDD estar down",
        "FALHA DE AUTENTICAÇÃO": "Peço que seja verificado o motivo da falha de autenticação",
        "HISTORICO DE LIGAÇÕES": "Peço que seja enviado o histórico de ligações do cliente",
        "LIMITADOR DE CONSUMO": "Peço que seja verificado o limitador de consumo do cliente",
        "LIGAÇÃO FEITA FALHANDO": "Peço que seja verificado o motivo da ligação estar falhando",
        "NAO EFETUA LIGAÇÃO": "Peço que seja verificado o motivo do cliente não conseguir efetuar ligação",
        "NAO RECEBE LIGAÇÕES": "Peço que seja verificado o motivo do cliente não conseguir receber ligação",
        "SUPORTE INTERNO": "Peço suporte interno para a telefonia"
    }
};

// Função para atualizar os tipos com base no setor selecionado
function atualizarTipos() {
    const setorSelecionado = document.getElementById('setor').value;
    const tipoSelect = document.getElementById('tipo');
    tipoSelect.innerHTML = '<option value="">Selecionar Opção</option>';

    if (setorSelecionado && tipos[setorSelecionado]) {
        tipos[setorSelecionado].forEach(tipo => {
            const option = document.createElement('option');
            option.value = tipo;
            option.textContent = tipo;
            tipoSelect.appendChild(option);
        });
    }
}

// Função para gerar o chamado e exibir no modal
function gerarChamado() {
    const cliente = document.getElementById('cliente').value.trim().toUpperCase();
    const codigo = document.getElementById('codigo').value.trim().toUpperCase();
    const setor = document.getElementById('setor').value.trim().toUpperCase();
    const tipo = document.getElementById('tipo').value.trim().toUpperCase();

    if (!cliente || !codigo || !setor || !tipo) {
        showAlert('Por favor, preencha todos os campos.');
        return;
    }

    const titulo = `${setor} - ${tipo} - ${cliente} - ${codigo}`;
    const descricao = descricoes[setor]?.[tipo] || 'Descrição não encontrada.';

    document.getElementById('titulo').textContent = titulo;
    document.getElementById('descricao').textContent = descricao;
    document.getElementById('modal').classList.add('show');
}

// Função para limpar o formulário
function limparFormulario() {
    document.getElementById('cliente').value = '';
    document.getElementById('codigo').value = '';
    document.getElementById('setor').value = '';
    document.getElementById('tipo').innerHTML = '<option value="">Selecionar Opção</option>';
}

// Função para fechar o modal
function fecharModal() {
    document.getElementById('modal').classList.remove('show');
}

// Função para copiar texto para a área de transferência
async function copiarTextoParaClipboard(text, type) {
    if (!navigator.clipboard) {
        try {
            const textArea = document.createElement("textarea");
            textArea.value = text;
            textArea.style.position = "fixed";
            textArea.style.opacity = "0";
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showNotification(`${type} copiado com sucesso!`);
        } catch (err) {
            console.error('Fallback: Oops, não foi possível copiar', err);
            showNotification(`Erro ao copiar ${type}.`);
        }
        return;
    }
    try {
        await navigator.clipboard.writeText(text);
        showNotification(`${type} copiado com sucesso!`);
    } catch (err) {
        console.error('Erro ao copiar texto: ', err);
        showNotification(`Erro ao copiar ${type}.`);
    }
}

// Função para copiar apenas o título
function copiarTitulo() {
    const titulo = document.getElementById('titulo').textContent;
    copiarTextoParaClipboard(titulo, 'Título');
}

// Função para copiar apenas a descrição
function copiarDescricao() {
    const descricao = document.getElementById('descricao').textContent;
    copiarTextoParaClipboard(descricao, 'Descrição');
}

// Função para exibir notificação
function showNotification(message) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.style.display = 'block';
    setTimeout(() => {
        if (notification.style.display === 'block') {
            notification.style.display = 'none';
        }
    }, 2900);
}

// Função para exibir alerta
function showAlert(message) {
    const alertPopup = document.getElementById('alertPopup');
    alertPopup.textContent = message;
    alertPopup.style.display = 'block';
    setTimeout(() => {
        if (alertPopup.style.display === 'block') {
            alertPopup.style.display = 'none';
        }
    }, 2900);
}

// Função para alternar submenus
function toggleMenu(element) {
    const submenu = element.nextElementSibling;
    const isActive = submenu.classList.contains('active');
    
    // Fecha todos os submenus abertos
    document.querySelectorAll('.submenu.active').forEach(openSubmenu => {
        if (openSubmenu !== submenu) {
            openSubmenu.classList.remove('active');
            openSubmenu.previousElementSibling.classList.remove('active');
        }
    });

    // Abre ou fecha o submenu clicado
    submenu.classList.toggle('active');
    element.classList.toggle('active');
}

// Theme toggle
const themeToggle = document.getElementById('themeToggle');
const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;

if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);
    if (currentTheme === 'dark') {
        themeToggle.textContent = '☀️';
    }
}

themeToggle.addEventListener('click', () => {
    let theme = document.documentElement.getAttribute('data-theme');
    if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
        themeToggle.textContent = '🌙';
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        themeToggle.textContent = '☀️';
    }
});

// Fechar modal ao clicar fora
window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target == modal) {
        fecharModal();
    }
}

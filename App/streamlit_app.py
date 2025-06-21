import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuração da API
API_URL = "http://api:5000"
token = None

# Função para fazer login
def login(login_user, senha):
    try:
        response = requests.post(f"{API_URL}/login", json={"login": login_user, "senha": senha})
        if response.status_code == 200:
            data = response.json()
            return data["token"], data["usuario"]
        return None, None
    except:
        st.error("Erro ao conectar com a API")
        return None, None

# Interface de login
def login_page():
    st.title("Sistema de Gerenciamento Escolar")
    
    login_input = st.text_input("Login")
    senha = st.text_input("Senha", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login"):
            token, usuario = login(login_input, senha)
            if token:
                st.session_state["token"] = token
                st.session_state["usuario"] = usuario
                st.session_state["page"] = "dashboard"
                st.experimental_rerun()
            else:
                st.error("Email ou senha incorretos")
    
    with col2:
        if st.button("Registrar nova conta"):
            st.session_state["page"] = "register"
            st.experimental_rerun()

# Interface de registro de usuário
def register_page():
    st.title("Registro de Novo Usuário")
    
    login_input = st.text_input("Login")
    senha = st.text_input("Senha", type="password")
    confirmar_senha = st.text_input("Confirmar Senha", type="password")
    nivel_acesso = st.selectbox("Nível de Acesso", ["admin", "secretaria", "professor"])
    
    if st.button("Registrar"):
        if senha != confirmar_senha:
            st.error("As senhas não coincidem!")
            return
            
        try:
            response = requests.post(f"{API_URL}/register", json={
                "login": login_input,
                "senha": senha,
                "nivel_acesso": nivel_acesso
            })
            
            if response.status_code == 201:
                st.success("Usuário registrado com sucesso! Faça login para continuar.")
                st.session_state["page"] = "login"
                st.experimental_rerun()
            else:
                st.error(f"Erro ao registrar: {response.json().get('message', 'Erro desconhecido')}")
        except Exception as e:
            st.error(f"Erro ao conectar com a API: {e}")
    
    if st.button("Já tem uma conta? Faça login"):
        st.session_state["page"] = "login"
        st.experimental_rerun()

# Dashboard principal
def dashboard():
    st.title(f"Bem-vindo ao Sistema Escolar")
    
    menu = st.sidebar.selectbox(
        "Menu", 
        ["Dashboard", "Alunos", "Turmas", "Pagamentos", "Presenças", "Atividades", "ChatBot"]
    )
    
    if menu == "Dashboard":
        st.header("Dashboard")
        st.write("Bem-vindo ao Sistema de Gerenciamento Escolar Infantil")
        st.write("Selecione uma opção no menu lateral para começar")
            
    elif menu == "Alunos":
        alunos_page()
    elif menu == "Turmas":
        turmas_page()
    elif menu == "Pagamentos":
        pagamentos_page()
    elif menu == "Presenças":
        presencas_page()
    elif menu == "Atividades":
        atividades_page()
    elif menu == "ChatBot":
        chatbot_page()
    
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

# Página de alunos
def alunos_page():
    st.header("Gerenciamento de Alunos")
    
    # Listar alunos existentes
    try:
        headers = {"Authorization": f"Bearer {st.session_state.get('token', '')}"}
        response = requests.get(f"{API_URL}/alunos", headers=headers)
        
        if response.status_code == 200:
            alunos = response.json()
            if alunos:
                df = pd.DataFrame(alunos)
                st.dataframe(df)
            else:
                st.info("Nenhum aluno cadastrado")
        else:
            st.error("Erro ao carregar alunos")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
    
    # Adicionar aluno
    with st.expander("Adicionar Aluno"):
        with st.form("novo_aluno"):
            nome = st.text_input("Nome Completo")
            data_nascimento = st.date_input("Data de Nascimento")
            id_turma = st.number_input("ID da Turma", min_value=1)
            nome_responsavel = st.text_input("Nome do Responsável")
            telefone_responsavel = st.text_input("Telefone do Responsável")
            email_responsavel = st.text_input("Email do Responsável")
            
            if st.form_submit_button("Adicionar"):
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.get('token', '')}"}
                    response = requests.post(
                        f"{API_URL}/alunos", 
                        json={
                            "nome_completo": nome,
                            "data_nascimento": data_nascimento.strftime("%Y-%m-%d"),
                            "id_turma": id_turma,
                            "nome_responsavel": nome_responsavel,
                            "telefone_responsavel": telefone_responsavel,
                            "email_responsavel": email_responsavel
                        },
                        headers=headers
                    )
                    
                    if response.status_code == 201:
                        st.success("Aluno adicionado com sucesso!")
                    else:
                        st.error(f"Erro ao adicionar aluno: {response.json().get('message', 'Erro desconhecido')}")
                except Exception as e:
                    st.error(f"Erro ao conectar com a API: {e}")

# Página de turmas
def turmas_page():
    st.header("Gerenciamento de Turmas")
    
    # Listar turmas existentes
    try:
        headers = {"Authorization": f"Bearer {st.session_state.get('token', '')}"}
        response = requests.get(f"{API_URL}/turmas", headers=headers)
        
        if response.status_code == 200:
            turmas = response.json()
            if turmas:
                df = pd.DataFrame(turmas)
                st.dataframe(df)
            else:
                st.info("Nenhuma turma cadastrada")
        else:
            st.error("Erro ao carregar turmas")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
    
    # Adicionar turma
    with st.expander("Adicionar Turma"):
        with st.form("nova_turma"):
            nome_turma = st.text_input("Nome da Turma")
            id_professor = st.number_input("ID do Professor", min_value=1, value=1)
            horario = st.text_input("Horário")
            
            if st.form_submit_button("Adicionar"):
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.get('token', '')}"}
                    response = requests.post(
                        f"{API_URL}/turmas", 
                        json={
                            "nome_turma": nome_turma,
                            "id_professor": id_professor,
                            "horario": horario
                        },
                        headers=headers
                    )
                    
                    if response.status_code == 201:
                        st.success("Turma adicionada com sucesso!")
                    else:
                        st.error(f"Erro ao adicionar turma: {response.json().get('message', 'Erro desconhecido')}")
                except Exception as e:
                    st.error(f"Erro ao conectar com a API: {e}")

# Página de pagamentos
def pagamentos_page():
    st.header("Gerenciamento de Pagamentos")
    
    # Listar pagamentos existentes
    try:
        headers = {"Authorization": f"Bearer {st.session_state.get('token', '')}"}
        response = requests.get(f"{API_URL}/pagamentos", headers=headers)
        
        if response.status_code == 200:
            pagamentos = response.json()
            if pagamentos:
                df = pd.DataFrame(pagamentos)
                st.dataframe(df)
            else:
                st.info("Nenhum pagamento registrado")
        else:
            st.error("Erro ao carregar pagamentos")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
    
    # Registrar pagamento
    with st.expander("Registrar Pagamento"):
        with st.form("novo_pagamento"):
            id_aluno = st.number_input("ID do Aluno", min_value=1)
            valor = st.number_input("Valor", min_value=0.0, format="%.2f")
            data = st.date_input("Data do Pagamento")
            forma_pagamento = st.selectbox("Forma de Pagamento", ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Transferência", "Boleto"])
            referencia = st.text_input("Referência (ex: Mensalidade Junho)")
            status = st.selectbox("Status", ["pendente", "pago"])
            
            if st.form_submit_button("Registrar"):
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.get('token', '')}"}
                    response = requests.post(
                        f"{API_URL}/pagamentos", 
                        json={
                            "id_aluno": id_aluno,
                            "data_pagamento": data.strftime("%Y-%m-%d"),
                            "valor_pago": valor,
                            "forma_pagamento": forma_pagamento,
                            "referencia": referencia,
                            "status": status
                        },
                        headers=headers
                    )
                    
                    if response.status_code == 201:
                        st.success("Pagamento registrado com sucesso!")
                    else:
                        st.error(f"Erro ao registrar pagamento: {response.json().get('message', 'Erro desconhecido')}")
                except Exception as e:
                    st.error(f"Erro ao conectar com a API: {e}")

# Página de presenças
def presencas_page():
    st.header("Controle de Presenças")
    
    # Listar presenças existentes
    try:
        headers = {"Authorization": f"Bearer {st.session_state.get('token', '')}"}
        response = requests.get(f"{API_URL}/presencas", headers=headers)
        
        if response.status_code == 200:
            presencas = response.json()
            if presencas:
                df = pd.DataFrame(presencas)
                st.dataframe(df)
            else:
                st.info("Nenhuma presença registrada")
        else:
            st.error("Erro ao carregar presenças")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
    
    # Registrar presença
    with st.expander("Registrar Presença"):
        with st.form("nova_presenca"):
            id_aluno = st.number_input("ID do Aluno", min_value=1)
            data = st.date_input("Data")
            presente = st.checkbox("Presente")
            
            if st.form_submit_button("Registrar"):
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.get('token', '')}"}
                    response = requests.post(
                        f"{API_URL}/presencas", 
                        json={
                            "id_aluno": id_aluno,
                            "data_presenca": data.strftime("%Y-%m-%d"),
                            "presente": presente
                        },
                        headers=headers
                    )
                    
                    if response.status_code == 201:
                        st.success("Presença registrada com sucesso!")
                    else:
                        st.error(f"Erro ao registrar presença: {response.json().get('message', 'Erro desconhecido')}")
                except Exception as e:
                    st.error(f"Erro ao conectar com a API: {e}")

# Página de atividades
def atividades_page():
    st.header("Gerenciamento de Atividades")
    
    # Listar atividades existentes
    try:
        headers = {"Authorization": f"Bearer {st.session_state.get('token', '')}"}
        response = requests.get(f"{API_URL}/atividades", headers=headers)
        
        if response.status_code == 200:
            atividades = response.json()
            if atividades:
                df = pd.DataFrame(atividades)
                st.dataframe(df)
            else:
                st.info("Nenhuma atividade registrada")
        else:
            st.error("Erro ao carregar atividades")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
    
    # Adicionar atividade
    with st.expander("Adicionar Atividade"):
        with st.form("nova_atividade"):
            descricao = st.text_area("Descrição")
            data = st.date_input("Data de Realização")
            id_turma = st.number_input("ID da Turma", min_value=1)
            
            if st.form_submit_button("Adicionar"):
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.get('token', '')}"}
                    response = requests.post(
                        f"{API_URL}/atividades", 
                        json={
                            "descricao": descricao,
                            "data_realizacao": data.strftime("%Y-%m-%d"),
                            "id_turma": id_turma,
                            "id_alunos": []  # Associar a todos os alunos da turma
                        },
                        headers=headers
                    )
                    
                    if response.status_code == 201:
                        st.success("Atividade adicionada com sucesso!")
                    else:
                        st.error(f"Erro ao adicionar atividade: {response.json().get('message', 'Erro desconhecido')}")
                except Exception as e:
                    st.error(f"Erro ao conectar com a API: {e}")

# Página do ChatBot
def chatbot_page():
    st.header("ChatBot")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Exibir mensagens anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Campo para nova mensagem
    prompt = st.chat_input("Digite sua mensagem...")
    
    if prompt:
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Enviar para o ChatBot
        try:
            headers = {"Authorization": f"Bearer {st.session_state.get('token', '')}"}
            response = requests.post(
                f"{API_URL}/chatbot", 
                json={
                    "query": prompt,
                    "user_id": st.session_state.get("usuario", {}).get("id_usuario")
                },
                headers=headers
            )
            
            if response.status_code == 200:
                bot_response = response.json().get("response", "Desculpe, não consegui processar sua mensagem.")
            else:
                bot_response = "Desculpe, ocorreu um erro ao processar sua mensagem."
        except Exception as e:
            bot_response = f"Erro ao conectar com o ChatBot: {e}"
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.write(bot_response)

# Função principal
def main():
    # Configuração da página
    st.set_page_config(
        page_title="Sistema Escolar",
        page_icon="🏫",
        layout="wide"
    )
    
    # Verificar qual página mostrar
    if "page" not in st.session_state:
        st.session_state["page"] = "login"
    
    if st.session_state["page"] == "login":
        login_page()
    elif st.session_state["page"] == "register":
        register_page()
    elif st.session_state["page"] == "dashboard":
        dashboard()

if __name__ == "__main__":
    main()
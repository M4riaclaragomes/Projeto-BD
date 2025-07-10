import streamlit as st
import requests
from datetime import datetime

API_URL = 'http://127.0.0.1:5000'

st.set_page_config(page_title="Sistema Restaurante", layout='wide')

# Tema escuro manual
st.markdown(
    """
    <style>
    .css-18e3th9 {background-color: #121212;}
    .css-1d391kg {color: white;}
    </style>
    """, unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu", ["Clientes", "Funcionários", "Terceirizados", "Veículos", "Pratos", "Pedidos"])

if menu == "Clientes":
    st.title("Cadastro de Clientes")
    with st.form("form_cliente"):
        nome = st.text_input("Nome")
        telefone = st.text_input("Telefone")
        email = st.text_input("E-mail")
        endereco = st.text_area("Endereço")
        submitted = st.form_submit_button("Cadastrar")
        if submitted:
            if not nome or not endereco:
                st.error("Nome e endereço são obrigatórios.")
            else:
                res = requests.post(f"{API_URL}/clientes", json={
                    "nome": nome,
                    "telefone": telefone,
                    "email": email,
                    "endereco": endereco
                })
                if res.status_code == 201:
                    st.success("Cliente cadastrado!")
                else:
                    st.error("Erro ao cadastrar cliente")

    st.subheader("Clientes cadastrados")
    res = requests.get(f"{API_URL}/clientes")
    if res.status_code == 200:
        clientes = res.json()
        for c in clientes:
            st.write(f"ID: {c['id']} - Nome: {c['nome']} - Telefone: {c.get('telefone')} - Endereço: {c.get('endereco')}")

elif menu == "Funcionários":
    st.title("Cadastro de Funcionários")
    with st.form("form_funcionario"):
        nome = st.text_input("Nome")
        cpf = st.text_input("CPF")
        telefone = st.text_input("Telefone")
        endereco = st.text_area("Endereço")
        sexo = st.selectbox("Sexo", ["M", "F", "O"])
        salario = st.number_input("Salário", min_value=0.0, format="%.2f")
        horario_trabalho = st.text_input("Horário de trabalho")
        data_contratacao = st.date_input("Data de contratação")
        classificacao = st.selectbox("Classificação", ["gerente", "atendente", "cozinheiro", "entregador_fixo"])
        submitted = st.form_submit_button("Cadastrar")
        if submitted:
            if not nome or not cpf or not classificacao:
                st.error("Nome, CPF e classificação são obrigatórios.")
            else:
                res = requests.post(f"{API_URL}/funcionarios", json={
                    "nome": nome,
                    "cpf": cpf,
                    "telefone": telefone,
                    "endereco": endereco,
                    "sexo": sexo,
                    "salario": salario,
                    "horario_trabalho": horario_trabalho,
                    "data_contratacao": data_contratacao.strftime("%Y-%m-%d"),
                    "classificacao": classificacao
                })
                if res.status_code == 201:
                    st.success("Funcionário cadastrado!")
                else:
                    st.error("Erro ao cadastrar funcionário")

    st.subheader("Funcionários cadastrados")
    res = requests.get(f"{API_URL}/funcionarios")
    if res.status_code == 200:
        funcionarios = res.json()
        for f in funcionarios:
            st.write(f"ID: {f['id']} - Nome: {f['nome']} - CPF: {f['cpf']} - Classificação: {f['classificacao']}")

elif menu == "Terceirizados":
    st.title("Cadastro de Terceirizados")
    with st.form("form_terceirizado"):
        nome = st.text_input("Nome")
        cpf_cnpj = st.text_input("CPF/CNPJ")
        telefone = st.text_input("Telefone")
        taxa_cobrada = st.number_input("Taxa Cobrada", min_value=0.0, format="%.2f")
        horario_contratado = st.text_input("Horário Contratado")
        classificacao = st.selectbox("Classificação", ["fornecedor", "entregador_app"])
        veiculo = None
        placa = None
        plataforma = None
        if classificacao == "entregador_app":
            veiculo = st.text_input("Veículo")
            placa = st.text_input("Placa")
            plataforma = st.text_input("Plataforma (iFood, UberEats, etc.)")
        submitted = st.form_submit_button("Cadastrar")
        if submitted:
            if not nome or not cpf_cnpj or not classificacao:
                st.error("Nome, CPF/CNPJ e classificação são obrigatórios.")
            else:
                res = requests.post(f"{API_URL}/terceirizados", json={
                    "nome": nome,
                    "cpf_cnpj": cpf_cnpj,
                    "telefone": telefone,
                    "taxa_cobrada": taxa_cobrada,
                    "horario_contratado": horario_contratado,
                    "classificacao": classificacao,
                    "veiculo": veiculo,
                    "placa": placa,
                    "plataforma": plataforma
                })
                if res.status_code == 201:
                    st.success("Terceirizado cadastrado!")
                else:
                    st.error("Erro ao cadastrar terceirizado")

    st.subheader("Terceirizados cadastrados")
    res = requests.get(f"{API_URL}/terceirizados")
    if res.status_code == 200:
        terceirizados = res.json()
        for t in terceirizados:
            st.write(f"ID: {t['id']} - Nome: {t['nome']} - Classificação: {t['classificacao']}")

elif menu == "Veículos":
    st.title("Cadastro de Veículos")
    with st.form("form_veiculo"):
        tipo = st.text_input("Tipo")
        placa = st.text_input("Placa")
        submitted = st.form_submit_button("Cadastrar")
        if submitted:
            if not tipo or not placa:
                st.error("Tipo e placa são obrigatórios.")
            else:
                res = requests.post(f"{API_URL}/veiculos", json={"tipo": tipo, "placa": placa})
                if res.status_code == 201:
                    st.success("Veículo cadastrado!")
                else:
                    st.error("Erro ao cadastrar veículo")

    st.subheader("Veículos cadastrados")
    res = requests.get(f"{API_URL}/veiculos")
    if res.status_code == 200:
        veiculos = res.json()
        for v in veiculos:
            st.write(f"ID: {v['id']} - Tipo: {v['tipo']} - Placa: {v['placa']} - Disponível: {'Sim' if v['disponivel'] else 'Não'}")

elif menu == "Pratos":
    st.title("Cadastro de Pratos")
    with st.form("form_prato"):
        nome = st.text_input("Nome do prato")
        preco = st.number_input("Preço", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Cadastrar")
        if submitted:
            if not nome:
                st.error("Nome do prato é obrigatório.")
            else:
                res = requests.post(f"{API_URL}/pratos", json={"nome": nome, "preco": preco})
                if res.status_code == 201:
                    st.success("Prato cadastrado!")
                else:
                    st.error("Erro ao cadastrar prato")

    st.subheader("Pratos cadastrados")
    res = requests.get(f"{API_URL}/pratos")
    if res.status_code == 200:
        pratos = res.json()
        for p in pratos:
            st.write(f"ID: {p['id']} - Nome: {p['nome']} - Preço: R$ {p['preco']:.2f}")

elif menu == "Pedidos":
    st.title("Pedidos")

    # Listar pedidos
    res = requests.get(f"{API_URL}/pedidos")
    if res.status_code == 200:
        pedidos = res.json()
        for pedido in pedidos:
            with st.expander(f"Pedido #{pedido['id']} - Cliente: {pedido.get('cliente_nome', 'N/A')}"):
                st.write(f"Data: {pedido['data']} Hora: {pedido['hora']}")
                st.write(f"Forma pagamento: {pedido['forma_pagamento']}")
                st.write(f"Tipo pedido: {pedido['tipo_pedido']}")
                st.write(f"Forma entrega: {pedido.get('forma_entrega', 'N/A')}")
                st.write(f"Entregador: {pedido.get('entregador_nome', 'Nenhum')}")
                st.write("Pratos:")
                for prato in pedido['pratos']:
                    st.write(f"- {prato['nome']} x {prato['quantidade']} (Obs: {prato.get('observacoes', '')})")

                # Atualizar status
                novo_status = st.selectbox(
                    "Atualizar status",
                    ["aguardando", "em_preparacao", "concluido"],
                    index=0,
                    key=f"status_{pedido['id']}"
                )
                if st.button("Salvar status", key=f"btn_status_{pedido['id']}"):
                    res_put = requests.put(f"{API_URL}/pedidos", json={"id": pedido['id'], "status": novo_status})
                    if res_put.status_code == 200:
                        st.success("Status atualizado!")
                    else:
                        st.error("Erro ao atualizar status")
    else:
        st.error("Erro ao carregar pedidos do backend.")

    # Formulário para criar pedido
    st.subheader("Criar novo pedido")
    with st.form("form_pedido"):
        clientes_res = requests.get(f"{API_URL}/clientes")
        pratos_res = requests.get(f"{API_URL}/pratos")
        funcionarios_res = requests.get(f"{API_URL}/funcionarios")

        clientes = clientes_res.json() if clientes_res.status_code == 200 else []
        pratos = pratos_res.json() if pratos_res.status_code == 200 else []
        funcionarios = funcionarios_res.json() if funcionarios_res.status_code == 200 else []

        cliente_id = st.selectbox("Cliente", options=[(c['id'], c['nome']) for c in clientes], format_func=lambda x: x[1]) if clientes else None
        tipo_pedido = st.selectbox("Tipo de pedido", ["local", "delivery"])
        endereco_entrega = None
        forma_entrega = None
        entregador_id = None

        if tipo_pedido == "delivery":
            endereco_entrega = st.text_area("Endereço de entrega")
            forma_entrega = st.selectbox("Forma de entrega", ["retirada_local", "entregador_fixo", "entregador_app"])

            if forma_entrega == "entregador_fixo":
                entregadores_fixos = [f for f in funcionarios if f['classificacao'] == 'entregador_fixo']
                if entregadores_fixos:
                    entregador_id = st.selectbox("Escolher entregador fixo", options=[(e['id'], e['nome']) for e in entregadores_fixos], format_func=lambda x: x[1])
                else:
                    st.warning("Nenhum entregador fixo disponível. Será solicitado entregador por aplicativo.")

            elif forma_entrega == "entregador_app":
                st.info("Será solicitado entregador por aplicativo.")

        forma_pagamento = st.selectbox("Forma de pagamento", ["dinheiro", "cartao", "pix"])

        pratos_pedido = []
        with st.expander("Adicionar pratos ao pedido"):
            for i in range(5):
                prato_sel = st.selectbox(f"Prato {i+1}", options=[(p['id'], p['nome']) for p in pratos], format_func=lambda x: x[1], key=f"prato_{i}")
                quantidade = st.number_input(f"Quantidade {i+1}", min_value=0, max_value=20, step=1, key=f"qtd_{i}")
                obs = st.text_input(f"Observações {i+1}", key=f"obs_{i}")
                if prato_sel and quantidade > 0:
                    pratos_pedido.append({
                        "prato_id": prato_sel[0],
                        "quantidade": quantidade,
                        "observacoes": obs
                    })

        submitted = st.form_submit_button("Criar pedido")

        if submitted:
            if not cliente_id:
                st.error("Selecione um cliente.")
            elif tipo_pedido == "delivery" and (not endereco_entrega or not forma_entrega):
                st.error("Preencha o endereço e forma de entrega para pedidos delivery.")
            elif not pratos_pedido:
                st.error("Adicione pelo menos um prato ao pedido.")
            else:
                agora = datetime.now()
                data = agora.strftime("%Y-%m-%d")
                hora = agora.strftime("%H:%M:%S")
                entrega_id = entregador_id[0] if entregador_id else None

                pedido_data = {
                    "cliente_id": cliente_id[0],
                    "data": data,
                    "hora": hora,
                    "endereco_entrega": endereco_entrega,
                    "forma_pagamento": forma_pagamento,
                    "tipo_pedido": tipo_pedido,
                    "entregador_id": entrega_id,
                    "forma_entrega": forma_entrega,
                    "pratos": pratos_pedido
                }

                res_post = requests.post(f"{API_URL}/pedidos", json=pedido_data)
                if res_post.status_code == 201:
                    st.success("Pedido criado com sucesso!")
                else:
                    st.error("Erro ao criar pedido.")

import sqlite3

def create_tables():
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()

    # Clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            email TEXT,
            endereco TEXT NOT NULL
        )
    ''')

    # Funcionários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Funcionario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            telefone TEXT,
            endereco TEXT,
            sexo TEXT CHECK(sexo IN ('M','F','O')),
            salario REAL,
            horario_trabalho TEXT,
            data_contratacao TEXT,
            data_demissao TEXT,
            classificacao TEXT CHECK(classificacao IN ('gerente', 'atendente', 'cozinheiro', 'entregador_fixo')) NOT NULL
        )
    ''')

    # Terceirizados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Terceirizado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf_cnpj TEXT UNIQUE NOT NULL,
            telefone TEXT,
            taxa_cobrada REAL,
            horario_contratado TEXT,
            classificacao TEXT CHECK(classificacao IN ('fornecedor', 'entregador_app')) NOT NULL,
            veiculo TEXT,
            placa TEXT,
            plataforma TEXT
        )
    ''')

    # Veículos dos entregadores fixos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Veiculo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            placa TEXT UNIQUE NOT NULL,
            disponivel INTEGER NOT NULL DEFAULT 1
        )
    ''')

    # Ingredientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ingrediente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0
        )
    ''')

    # Pratos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Prato (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL
        )
    ''')

    # Pedidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL,
            endereco_entrega TEXT,
            forma_pagamento TEXT NOT NULL,
            taxa_servico REAL DEFAULT 0,
            taxa_entrega REAL DEFAULT 0,
            taxa_couvert REAL DEFAULT 0,
            tipo_pedido TEXT CHECK(tipo_pedido IN ('local', 'delivery')) NOT NULL,
            entregador_id INTEGER,
            forma_entrega TEXT CHECK(forma_entrega IN ('retirada_local', 'entregador_fixo', 'entregador_app')),
            status TEXT CHECK(status IN ('aguardando', 'em_preparacao', 'concluido')) DEFAULT 'aguardando',
            FOREIGN KEY(cliente_id) REFERENCES Cliente(id),
            FOREIGN KEY(entregador_id) REFERENCES Funcionario(id)
        )
    ''')

    # Relação pratos no pedido
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pedido_Prato (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            prato_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            observacoes TEXT,
            FOREIGN KEY(pedido_id) REFERENCES Pedido(id),
            FOREIGN KEY(prato_id) REFERENCES Prato(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Tabelas criadas com sucesso!")

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = 'restaurante.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Clientes
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        clientes = cursor.execute('SELECT * FROM Cliente').fetchall()
        result = [dict(row) for row in clientes]
        conn.close()
        return jsonify(result)

    if request.method == 'POST':
        data = request.json
        cursor.execute('INSERT INTO Cliente (nome, telefone, email, endereco) VALUES (?, ?, ?, ?)',
                       (data['nome'], data.get('telefone'), data.get('email'), data['endereco']))
        conn.commit()
        conn.close()
        return jsonify({"msg": "Cliente criado"}), 201

# Funcionários
@app.route('/funcionarios', methods=['GET', 'POST'])
def funcionarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        funcionarios = cursor.execute('SELECT * FROM Funcionario').fetchall()
        result = [dict(row) for row in funcionarios]
        conn.close()
        return jsonify(result)

    if request.method == 'POST':
        data = request.json
        cursor.execute('''
            INSERT INTO Funcionario (nome, cpf, telefone, endereco, sexo, salario, horario_trabalho, data_contratacao, classificacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (data['nome'], data['cpf'], data.get('telefone'), data.get('endereco'), data.get('sexo'),
                        data.get('salario'), data.get('horario_trabalho'), data.get('data_contratacao'), data['classificacao']))
        conn.commit()
        conn.close()
        return jsonify({"msg": "Funcionario criado"}), 201

# Terceirizados
@app.route('/terceirizados', methods=['GET', 'POST'])
def terceirizados():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        terceirizados = cursor.execute('SELECT * FROM Terceirizado').fetchall()
        result = [dict(row) for row in terceirizados]
        conn.close()
        return jsonify(result)

    if request.method == 'POST':
        data = request.json
        cursor.execute('''
            INSERT INTO Terceirizado (nome, cpf_cnpj, telefone, taxa_cobrada, horario_contratado, classificacao, veiculo, placa, plataforma)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (data['nome'], data['cpf_cnpj'], data.get('telefone'), data.get('taxa_cobrada'), data.get('horario_contratado'),
                        data['classificacao'], data.get('veiculo'), data.get('placa'), data.get('plataforma')))
        conn.commit()
        conn.close()
        return jsonify({"msg": "Terceirizado criado"}), 201

# Veículos
@app.route('/veiculos', methods=['GET', 'POST'])
def veiculos():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        veiculos = cursor.execute('SELECT * FROM Veiculo').fetchall()
        result = [dict(row) for row in veiculos]
        conn.close()
        return jsonify(result)

    if request.method == 'POST':
        data = request.json
        cursor.execute('INSERT INTO Veiculo (tipo, placa, disponivel) VALUES (?, ?, ?)',
                       (data['tipo'], data['placa'], 1))
        conn.commit()
        conn.close()
        return jsonify({"msg": "Veículo criado"}), 201

# Pratos
@app.route('/pratos', methods=['GET', 'POST'])
def pratos():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        pratos = cursor.execute('SELECT * FROM Prato').fetchall()
        result = [dict(row) for row in pratos]
        conn.close()
        return jsonify(result)

    if request.method == 'POST':
        data = request.json
        cursor.execute('INSERT INTO Prato (nome, preco) VALUES (?, ?)', (data['nome'], data['preco']))
        conn.commit()
        conn.close()
        return jsonify({"msg": "Prato criado"}), 201

# Pedidos
@app.route('/pedidos', methods=['GET', 'POST', 'PUT'])
def pedidos():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        # Buscar pedidos com detalhes
        pedidos = cursor.execute('SELECT * FROM Pedido').fetchall()
        result = []
        for pedido in pedidos:
            p = dict(pedido)
            # Cliente nome
            cliente = cursor.execute('SELECT nome FROM Cliente WHERE id = ?', (pedido['cliente_id'],)).fetchone()
            p['cliente_nome'] = cliente['nome'] if cliente else None

            # Entregador nome
            if pedido['entregador_id']:
                entregador = cursor.execute('SELECT nome FROM Funcionario WHERE id = ?', (pedido['entregador_id'],)).fetchone()
                p['entregador_nome'] = entregador['nome'] if entregador else None
            else:
                p['entregador_nome'] = None

            # Pratos do pedido
            pratos_pedido = cursor.execute('''
                SELECT Prato.nome, Pedido_Prato.quantidade, Pedido_Prato.observacoes
                FROM Pedido_Prato
                JOIN Prato ON Pedido_Prato.prato_id = Prato.id
                WHERE Pedido_Prato.pedido_id = ?''', (pedido['id'],)).fetchall()
            p['pratos'] = [dict(pr) for pr in pratos_pedido]

            result.append(p)
        conn.close()
        return jsonify(result)

    if request.method == 'POST':
        data = request.json
        cursor.execute('''
            INSERT INTO Pedido (cliente_id, data, hora, endereco_entrega, forma_pagamento, taxa_servico, taxa_entrega,
            taxa_couvert, tipo_pedido, entregador_id, forma_entrega, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (
                        data['cliente_id'],
                        data['data'],
                        data['hora'],
                        data.get('endereco_entrega'),
                        data['forma_pagamento'],
                        data.get('taxa_servico', 0),
                        data.get('taxa_entrega', 0),
                        data.get('taxa_couvert', 0),
                        data['tipo_pedido'],
                        data.get('entregador_id'),
                        data.get('forma_entrega'),
                        "aguardando"  # status inicial
                       ))
        pedido_id = cursor.lastrowid

        for prato in data['pratos']:
            cursor.execute('''
                INSERT INTO Pedido_Prato (pedido_id, prato_id, quantidade, observacoes)
                VALUES (?, ?, ?, ?)''',
                           (pedido_id, prato['prato_id'], prato['quantidade'], prato.get('observacoes')))
        conn.commit()
        conn.close()
        return jsonify({"msg": "Pedido criado", "pedido_id": pedido_id}), 201

    if request.method == 'PUT':
        data = request.json
        cursor.execute('UPDATE Pedido SET status = ? WHERE id = ?', (data['status'], data['id']))
        conn.commit()
        conn.close()
        return jsonify({"msg": "Status atualizado"}), 200

if __name__ == '__main__':
    app.run(debug=True)

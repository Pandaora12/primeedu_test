from flask import request, jsonify, Blueprint
from src.models import db, Pagamento, Aluno
from routes.auth import token_required
from flasgger import swag_from
from datetime import datetime

pagamentos_bp = Blueprint('pagamentos', __name__)

# Adicionar pagamento
@pagamentos_bp.route('/pagamentos', methods=['POST'])
@token_required
def adicionar_pagamento(usuario_atual):
    """
    Adicionar um novo pagamento
    
    **URL Completa:** `POST http://localhost:5000/pagamentos`
    **Para Insomnia/Postman:** Copie a URL acima + Header: `Authorization: Bearer {token}`
    ---
    tags:
      - Pagamentos
    security:
      - Bearer: []
    parameters:
      - in: body
        name: pagamento
        description: Dados do pagamento
        required: true
        schema:
          type: object
          required:
            - id_aluno
            - data_pagamento
            - valor_pago
            - forma_pagamento
            - referencia
            - status
          properties:
            id_aluno:
              type: integer
              example: 1
            data_pagamento:
              type: string
              format: date
              example: "2024-01-15"
            valor_pago:
              type: number
              example: 150.50
            forma_pagamento:
              type: string
              example: "PIX"
            referencia:
              type: string
              example: "Janeiro/2024"
            status:
              type: string
              enum: ["pago", "pendente"]
              example: "pago"
    responses:
      201:
        description: Pagamento registrado com sucesso
      404:
        description: Aluno não encontrado
      401:
        description: Token não fornecido ou inválido
    """
    data = request.get_json()
    aluno = Aluno.query.get(data['id_aluno'])
    if not aluno:
        return jsonify({"message": "Aluno não encontrado!"}), 404
    pagamento = Pagamento(
        id_aluno=data['id_aluno'],
        data_pagamento=data['data_pagamento'],
        valor_pago=data['valor_pago'],
        forma_pagamento=data['forma_pagamento'],
        referencia=data['referencia'],
        status=data['status']
    )
    db.session.add(pagamento)
    db.session.commit()
    return jsonify({"message": "Pagamento registrado com sucesso!"}), 201

# Listar pagamentos
@pagamentos_bp.route('/pagamentos', methods=['GET'])
@token_required
def listar_pagamentos(usuario_atual):
    """
    Listar todos os pagamentos
    ---
    tags:
      - Pagamentos
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de pagamentos
        schema:
          type: array
          items:
            type: object
            properties:
              id_pagamento:
                type: integer
              id_aluno:
                type: integer
              data_pagamento:
                type: string
              valor_pago:
                type: number
              forma_pagamento:
                type: string
              referencia:
                type: string
              status:
                type: string
      401:
        description: Token não fornecido ou inválido
    """
    pagamentos = Pagamento.query.all()
    return jsonify([pagamento.as_dict() for pagamento in pagamentos])

# Consultar pagamento por ID
@pagamentos_bp.route('/pagamentos/<int:id>', methods=['GET'])
@token_required
def consultar_pagamento(usuario_atual, id):
    """
    Consultar pagamento por ID
    ---
    tags:
      - Pagamentos
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do pagamento
    responses:
      200:
        description: Dados do pagamento
      404:
        description: Pagamento não encontrado
      401:
        description: Token não fornecido ou inválido
    """
    pagamento = Pagamento.query.get(id)
    if pagamento:
        return jsonify(pagamento.as_dict())
    return jsonify({"message": "Pagamento não encontrado!"}), 404

# Atualizar pagamento
@pagamentos_bp.route('/pagamentos/<int:id>', methods=['PUT'])
@token_required
def atualizar_pagamento(usuario_atual, id):
    """
    Atualizar dados de um pagamento
    ---
    tags:
      - Pagamentos
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do pagamento
      - in: body
        name: pagamento
        description: Dados atualizados do pagamento
        required: true
        schema:
          type: object
          properties:
            id_aluno:
              type: integer
            data_pagamento:
              type: string
              format: date
            valor_pago:
              type: number
            forma_pagamento:
              type: string
            referencia:
              type: string
            status:
              type: string
    responses:
      200:
        description: Pagamento atualizado com sucesso
      404:
        description: Pagamento não encontrado
      401:
        description: Token não fornecido ou inválido
    """
    pagamento = Pagamento.query.get(id)
    if not pagamento:
        return jsonify({"message": "Pagamento não encontrado!"}), 404
    data = request.get_json()
    pagamento.id_aluno = data['id_aluno']
    pagamento.data_pagamento = data['data_pagamento']
    pagamento.valor_pago = data['valor_pago']
    pagamento.forma_pagamento = data['forma_pagamento']
    pagamento.referencia = data['referencia']
    pagamento.status = data['status']
    db.session.commit()
    return jsonify({"message": "Pagamento atualizado com sucesso!"})

# Deletar pagamento
@pagamentos_bp.route('/pagamentos/<int:id>', methods=['DELETE'])
@token_required
def deletar_pagamento(usuario_atual, id):
    """
    Deletar um pagamento
    ---
    tags:
      - Pagamentos
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do pagamento
    responses:
      200:
        description: Pagamento deletado com sucesso
      404:
        description: Pagamento não encontrado
      401:
        description: Token não fornecido ou inválido
    """
    pagamento = Pagamento.query.get(id)
    if not pagamento:
        return jsonify({"message": "Pagamento não encontrado!"}), 404
    db.session.delete(pagamento)
    db.session.commit()
    return jsonify({"message": "Pagamento deletado com sucesso!"})

# Consultar pagamentos por aluno
@pagamentos_bp.route('/alunos/<int:id_aluno>/pagamentos', methods=['GET'])
@token_required
def consultar_pagamentos_aluno(usuario_atual, id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        return jsonify({"message": "Aluno não encontrado!"}), 404
    pagamentos = Pagamento.query.filter_by(id_aluno=id_aluno).all()
    return jsonify([pagamento.as_dict() for pagamento in pagamentos])

# Gerar relatório de pagamentos por período
@pagamentos_bp.route('/relatorios/pagamentos', methods=['GET'])
@token_required
def relatorio_pagamentos(usuario_atual):
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    if not data_inicio or not data_fim:
        return jsonify({"message": "Data de início e fim são obrigatórias!"}), 400
    
    try:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Formato de data inválido! Use YYYY-MM-DD"}), 400
    
    pagamentos = Pagamento.query.filter(
        Pagamento.data_pagamento >= data_inicio,
        Pagamento.data_pagamento <= data_fim
    ).all()
    
    total = sum(float(pagamento.valor_pago) for pagamento in pagamentos)
    
    return jsonify({
        "pagamentos": [pagamento.as_dict() for pagamento in pagamentos],
        "total": total,
        "periodo": {
            "inicio": data_inicio.strftime('%Y-%m-%d'),
            "fim": data_fim.strftime('%Y-%m-%d')
        }
    })
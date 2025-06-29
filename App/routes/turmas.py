from flask import request, jsonify, Blueprint
from src.models import db, Turma
from flasgger import swag_from

turmas_bp = Blueprint('turmas', __name__)

# Adicionar uma nova turma
@turmas_bp.route('/turmas', methods=['POST'])
def adicionar_turma():
    """
    Adicionar uma nova turma
    ---
    tags:
      - Turmas
    parameters:
      - in: body
        name: turma
        description: Dados da turma
        required: true
        schema:
          type: object
          required:
            - nome_turma
          properties:
            nome_turma:
              type: string
              example: "Turma A - 1º Ano"
            id_professor:
              type: integer
              example: 1
            horario:
              type: string
              example: "08:00 - 12:00"
    responses:
      201:
        description: Turma adicionada com sucesso
      400:
        description: Dados inválidos
    """
    data = request.get_json()
    nova_turma = Turma(
        nome_turma=data['nome_turma'],
        id_professor=data.get('id_professor'),
        horario=data.get('horario')
    )
    db.session.add(nova_turma)
    db.session.commit()
    return jsonify({"message": "Turma adicionada com sucesso!"}), 201

# Listar todas as turmas
@turmas_bp.route('/turmas', methods=['GET'])
def listar_turmas():
    """
    Listar todas as turmas
    ---
    tags:
      - Turmas
    responses:
      200:
        description: Lista de turmas
        schema:
          type: array
          items:
            type: object
            properties:
              id_turma:
                type: integer
              nome_turma:
                type: string
              id_professor:
                type: integer
              horario:
                type: string
    """
    turmas = Turma.query.all()
    return jsonify([turma.as_dict() for turma in turmas])

# Consultar turma pelo ID
@turmas_bp.route('/turmas/<int:id>', methods=['GET'])
def consultar_turma(id):
    """
    Consultar turma por ID
    ---
    tags:
      - Turmas
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da turma
    responses:
      200:
        description: Dados da turma
      404:
        description: Turma não encontrada
    """
    turma = Turma.query.get(id)
    if turma:
        return jsonify(turma.as_dict())
    return jsonify({"message": "Turma não encontrada!"}), 404

# Atualizar dados de uma turma
@turmas_bp.route('/turmas/<int:id>', methods=['PUT'])
def atualizar_turma(id):
    """
    Atualizar dados de uma turma
    ---
    tags:
      - Turmas
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da turma
      - in: body
        name: turma
        description: Dados atualizados da turma
        required: true
        schema:
          type: object
          properties:
            nome_turma:
              type: string
            id_professor:
              type: integer
            horario:
              type: string
    responses:
      200:
        description: Turma atualizada com sucesso
      404:
        description: Turma não encontrada
    """
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({"message": "Turma não encontrada!"}), 404
    data = request.get_json()
    turma.nome_turma = data['nome_turma']
    turma.id_professor = data.get('id_professor')
    turma.horario = data.get('horario')
    db.session.commit()
    return jsonify({"message": "Turma atualizada com sucesso!"})

# Deletar turma
@turmas_bp.route('/turmas/<int:id>', methods=['DELETE'])
def deletar_turma(id):
    """
    Deletar uma turma
    ---
    tags:
      - Turmas
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da turma
    responses:
      200:
        description: Turma deletada com sucesso
      404:
        description: Turma não encontrada
    """
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({"message": "Turma não encontrada!"}), 404
    db.session.delete(turma)
    db.session.commit()
    return jsonify({"message": "Turma deletada com sucesso!"})
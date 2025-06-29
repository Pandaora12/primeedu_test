from flask import request, jsonify, Blueprint
from src.models import db, Aluno
from flasgger import swag_from

alunos_bp = Blueprint('alunos', __name__)

# Adicionar um novo aluno
@alunos_bp.route('/alunos', methods=['POST'])
def adicionar_aluno():
    """
    Adicionar um novo aluno
    
    **URL Completa:** `POST http://localhost:5000/alunos`
    **Para Insomnia/Postman:** Copie a URL acima
    ---
    tags:
      - Alunos
    parameters:
      - in: body
        name: aluno
        description: Dados do aluno
        required: true
        schema:
          type: object
          required:
            - nome_completo
            - data_nascimento
            - id_turma
            - nome_responsavel
            - telefone_responsavel
            - email_responsavel
          properties:
            nome_completo:
              type: string
              example: "João Silva Santos"
            data_nascimento:
              type: string
              format: date
              example: "2010-05-15"
            id_turma:
              type: integer
              example: 1
            nome_responsavel:
              type: string
              example: "Maria Silva"
            telefone_responsavel:
              type: string
              example: "(11) 99999-9999"
            email_responsavel:
              type: string
              example: "maria.silva@email.com"
    responses:
      201:
        description: Aluno adicionado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Aluno adicionado com sucesso!"
      400:
        description: Dados inválidos
    """
    data = request.get_json()
    novo_aluno = Aluno(
        nome_completo=data['nome_completo'],
        data_nascimento=data['data_nascimento'],
        id_turma=data['id_turma'],
        nome_responsavel=data['nome_responsavel'],
        telefone_responsavel=data['telefone_responsavel'],
        email_responsavel=data['email_responsavel']
    )
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify({"message": "Aluno adicionado com sucesso!"}), 201

# Listar todos os alunos
@alunos_bp.route('/alunos', methods=['GET'])
def listar_alunos():
    """
    Listar todos os alunos
    
    **URL Completa:** `GET http://localhost:5000/alunos`
    **Para Insomnia/Postman:** Copie a URL acima
    ---
    tags:
      - Alunos
    responses:
      200:
        description: Lista de alunos
        schema:
          type: array
          items:
            type: object
            properties:
              id_aluno:
                type: integer
              nome_completo:
                type: string
              data_nascimento:
                type: string
                format: date
              id_turma:
                type: integer
              nome_responsavel:
                type: string
              telefone_responsavel:
                type: string
              email_responsavel:
                type: string
    """
    alunos = Aluno.query.all()
    return jsonify([aluno.as_dict() for aluno in alunos])

# Consultar aluno pelo ID
@alunos_bp.route('/alunos/<int:id>', methods=['GET'])
def consultar_aluno(id):
    """
    Consultar aluno por ID
    ---
    tags:
      - Alunos
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do aluno
    responses:
      200:
        description: Dados do aluno
        schema:
          type: object
          properties:
            id_aluno:
              type: integer
            nome_completo:
              type: string
            data_nascimento:
              type: string
            id_turma:
              type: integer
            nome_responsavel:
              type: string
            telefone_responsavel:
              type: string
            email_responsavel:
              type: string
      404:
        description: Aluno não encontrado
    """
    aluno = Aluno.query.get(id)
    if aluno:
        return jsonify(aluno.as_dict())
    return jsonify({"message": "Aluno não encontrado!"}), 404

# Atualizar dados de um aluno
@alunos_bp.route('/alunos/<int:id>', methods=['PUT'])
def atualizar_aluno(id):
    """
    Atualizar dados de um aluno
    ---
    tags:
      - Alunos
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do aluno
      - in: body
        name: aluno
        description: Dados atualizados do aluno
        required: true
        schema:
          type: object
          properties:
            nome_completo:
              type: string
            data_nascimento:
              type: string
              format: date
            id_turma:
              type: integer
            nome_responsavel:
              type: string
            telefone_responsavel:
              type: string
            email_responsavel:
              type: string
    responses:
      200:
        description: Aluno atualizado com sucesso
      404:
        description: Aluno não encontrado
    """
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"message": "Aluno não encontrado!"}), 404
    data = request.get_json()
    aluno.nome_completo = data['nome_completo']
    aluno.data_nascimento = data['data_nascimento']
    aluno.id_turma = data['id_turma']
    aluno.nome_responsavel = data['nome_responsavel']
    aluno.telefone_responsavel = data['telefone_responsavel']
    aluno.email_responsavel = data['email_responsavel']
    db.session.commit()
    return jsonify({"message": "Aluno atualizado com sucesso!"})

# Deletar aluno
@alunos_bp.route('/alunos/<int:id>', methods=['DELETE'])
def deletar_aluno(id):
    """
    Deletar um aluno
    ---
    tags:
      - Alunos
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do aluno
    responses:
      200:
        description: Aluno deletado com sucesso
      404:
        description: Aluno não encontrado
    """
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"message": "Aluno não encontrado!"}), 404
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"message": "Aluno deletado com sucesso!"})
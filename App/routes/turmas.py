from flask import request, jsonify, Blueprint
from src.models import db, Turma

turmas_bp = Blueprint('turmas', __name__)

# Adicionar uma nova turma
@turmas_bp.route('/turmas', methods=['POST'])
def adicionar_turma():
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
    turmas = Turma.query.all()
    return jsonify([turma.as_dict() for turma in turmas])

# Consultar turma pelo ID
@turmas_bp.route('/turmas/<int:id>', methods=['GET'])
def consultar_turma(id):
    turma = Turma.query.get(id)
    if turma:
        return jsonify(turma.as_dict())
    return jsonify({"message": "Turma não encontrada!"}), 404

# Atualizar dados de uma turma
@turmas_bp.route('/turmas/<int:id>', methods=['PUT'])
def atualizar_turma(id):
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
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({"message": "Turma não encontrada!"}), 404
    db.session.delete(turma)
    db.session.commit()
    return jsonify({"message": "Turma deletada com sucesso!"})
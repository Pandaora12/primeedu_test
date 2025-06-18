from flask import request, jsonify, Blueprint
from src.models import db, Aluno

alunos_bp = Blueprint('alunos', __name__)

# Adicionar um novo aluno
@alunos_bp.route('/alunos', methods=['POST'])
def adicionar_aluno():
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
    alunos = Aluno.query.all()
    return jsonify([aluno.as_dict() for aluno in alunos])

# Consultar aluno pelo ID
@alunos_bp.route('/alunos/<int:id>', methods=['GET'])
def consultar_aluno(id):
    aluno = Aluno.query.get(id)
    if aluno:
        return jsonify(aluno.as_dict())
    return jsonify({"message": "Aluno não encontrado!"}), 404

# Atualizar dados de um aluno
@alunos_bp.route('/alunos/<int:id>', methods=['PUT'])
def atualizar_aluno(id):
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
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"message": "Aluno não encontrado!"}), 404
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"message": "Aluno deletado com sucesso!"})
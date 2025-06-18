from flask import request, jsonify, Blueprint
from src.models import db, Atividade, Aluno, Atividade_Aluno, Atividade_Turma, Turma
from routes.auth import token_required
from datetime import datetime

atividades_bp = Blueprint('atividades', __name__)

# Adicionar atividade
@atividades_bp.route('/atividades', methods=['POST'])
@token_required
def adicionar_atividade(usuario_atual):
    data = request.get_json()
    nova_atividade = Atividade(
        descricao=data['descricao'],
        data_realizacao=data['data_realizacao']
    )
    db.session.add(nova_atividade)
    db.session.commit()

    # Associar alunos à atividade
    for aluno_id in data['id_alunos']:
        atividade_aluno = Atividade_Aluno(id_atividade=nova_atividade.id_atividade, id_aluno=aluno_id)
        db.session.add(atividade_aluno)

    db.session.commit()
    return jsonify({"message": "Atividade registrada com sucesso!"}), 201

# Listar atividades
@atividades_bp.route('/atividades', methods=['GET'])
@token_required
def listar_atividades(usuario_atual):
    atividades = Atividade.query.all()
    return jsonify([atividade.as_dict() for atividade in atividades])

# Consultar atividade por ID
@atividades_bp.route('/atividades/<int:id>', methods=['GET'])
@token_required
def consultar_atividade(usuario_atual, id):
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({"message": "Atividade não encontrada!"}), 404
    
    # Buscar alunos associados a esta atividade
    atividade_alunos = Atividade_Aluno.query.filter_by(id_atividade=id).all()
    alunos_ids = [aa.id_aluno for aa in atividade_alunos]
    alunos = Aluno.query.filter(Aluno.id_aluno.in_(alunos_ids)).all()
    
    # Buscar turmas associadas a esta atividade
    atividade_turmas = Atividade_Turma.query.filter_by(id_atividade=id).all()
    turmas_ids = [at.id_turma for at in atividade_turmas]
    turmas = Turma.query.filter(Turma.id_turma.in_(turmas_ids)).all()
    
    resultado = atividade.as_dict()
    resultado['alunos'] = [aluno.as_dict() for aluno in alunos]
    resultado['turmas'] = [turma.as_dict() for turma in turmas]
    
    return jsonify(resultado)

# Atualizar atividade
@atividades_bp.route('/atividades/<int:id>', methods=['PUT'])
@token_required
def atualizar_atividade(usuario_atual, id):
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({"message": "Atividade não encontrada!"}), 404
    
    data = request.get_json()
    atividade.descricao = data['descricao']
    atividade.data_realizacao = data['data_realizacao']
    
    # Atualizar associações com alunos
    if 'id_alunos' in data:
        # Remover associações existentes
        Atividade_Aluno.query.filter_by(id_atividade=id).delete()
        
        # Adicionar novas associações
        for aluno_id in data['id_alunos']:
            atividade_aluno = Atividade_Aluno(id_atividade=id, id_aluno=aluno_id)
            db.session.add(atividade_aluno)
    
    # Atualizar associações com turmas
    if 'id_turmas' in data:
        # Remover associações existentes
        Atividade_Turma.query.filter_by(id_atividade=id).delete()
        
        # Adicionar novas associações
        for turma_id in data['id_turmas']:
            atividade_turma = Atividade_Turma(id_atividade=id, id_turma=turma_id)
            db.session.add(atividade_turma)
    
    db.session.commit()
    return jsonify({"message": "Atividade atualizada com sucesso!"})

# Deletar atividade
@atividades_bp.route('/atividades/<int:id>', methods=['DELETE'])
@token_required
def deletar_atividade(usuario_atual, id):
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({"message": "Atividade não encontrada!"}), 404
    
    # Remover associações com alunos
    Atividade_Aluno.query.filter_by(id_atividade=id).delete()
    
    # Remover associações com turmas
    Atividade_Turma.query.filter_by(id_atividade=id).delete()
    
    db.session.delete(atividade)
    db.session.commit()
    return jsonify({"message": "Atividade deletada com sucesso!"})

# Adicionar atividade para uma turma
@atividades_bp.route('/turmas/<int:id_turma>/atividades', methods=['POST'])
@token_required
def adicionar_atividade_turma(usuario_atual, id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        return jsonify({"message": "Turma não encontrada!"}), 404
    
    data = request.get_json()
    nova_atividade = Atividade(
        descricao=data['descricao'],
        data_realizacao=data['data_realizacao']
    )
    db.session.add(nova_atividade)
    db.session.commit()
    
    # Associar a atividade à turma
    atividade_turma = Atividade_Turma(
        id_atividade=nova_atividade.id_atividade,
        id_turma=id_turma
    )
    db.session.add(atividade_turma)
    
    # Associar a atividade a todos os alunos da turma
    alunos = Aluno.query.filter_by(id_turma=id_turma).all()
    for aluno in alunos:
        atividade_aluno = Atividade_Aluno(
            id_atividade=nova_atividade.id_atividade,
            id_aluno=aluno.id_aluno
        )
        db.session.add(atividade_aluno)
    
    db.session.commit()
    return jsonify({"message": "Atividade adicionada à turma com sucesso!"}), 201

# Listar atividades de uma turma
@atividades_bp.route('/turmas/<int:id_turma>/atividades', methods=['GET'])
@token_required
def listar_atividades_turma(usuario_atual, id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        return jsonify({"message": "Turma não encontrada!"}), 404
    
    atividade_turmas = Atividade_Turma.query.filter_by(id_turma=id_turma).all()
    atividades_ids = [at.id_atividade for at in atividade_turmas]
    atividades = Atividade.query.filter(Atividade.id_atividade.in_(atividades_ids)).all()
    
    return jsonify([atividade.as_dict() for atividade in atividades])

# Listar atividades de um aluno
@atividades_bp.route('/alunos/<int:id_aluno>/atividades', methods=['GET'])
@token_required
def listar_atividades_aluno(usuario_atual, id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        return jsonify({"message": "Aluno não encontrado!"}), 404
    
    atividade_alunos = Atividade_Aluno.query.filter_by(id_aluno=id_aluno).all()
    atividades_ids = [aa.id_atividade for aa in atividade_alunos]
    atividades = Atividade.query.filter(Atividade.id_atividade.in_(atividades_ids)).all()
    
    return jsonify([atividade.as_dict() for atividade in atividades])

# Gerar relatório de atividades por período
@atividades_bp.route('/relatorios/atividades', methods=['GET'])
@token_required
def relatorio_atividades(usuario_atual):
    id_turma = request.args.get('id_turma')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    if not data_inicio or not data_fim:
        return jsonify({"message": "Data de início e fim são obrigatórias!"}), 400
    
    try:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Formato de data inválido! Use YYYY-MM-DD"}), 400
    
    query = Atividade.query.filter(
        Atividade.data_realizacao >= data_inicio,
        Atividade.data_realizacao <= data_fim
    )
    
    if id_turma:
        # Filtrar atividades por turma
        atividade_turmas = Atividade_Turma.query.filter_by(id_turma=id_turma).all()
        atividades_ids = [at.id_atividade for at in atividade_turmas]
        query = query.filter(Atividade.id_atividade.in_(atividades_ids))
    
    atividades = query.all()
    
    resultado = {
        "atividades": [],
        "periodo": {
            "inicio": data_inicio.strftime('%Y-%m-%d'),
            "fim": data_fim.strftime('%Y-%m-%d')
        },
        "total_atividades": len(atividades)
    }
    
    for atividade in atividades:
        atividade_dict = atividade.as_dict()
        
        # Buscar turmas associadas a esta atividade
        atividade_turmas = Atividade_Turma.query.filter_by(id_atividade=atividade.id_atividade).all()
        turmas_ids = [at.id_turma for at in atividade_turmas]
        turmas = Turma.query.filter(Turma.id_turma.in_(turmas_ids)).all()
        
        atividade_dict['turmas'] = [turma.as_dict() for turma in turmas]
        resultado["atividades"].append(atividade_dict)
    
    return jsonify(resultado)
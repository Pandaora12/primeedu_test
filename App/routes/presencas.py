from flask import request, jsonify, Blueprint
from src.models import db, Presenca, Aluno
from routes.auth import token_required
from datetime import datetime, timedelta

presencas_bp = Blueprint('presencas', __name__)

# Registrar presença
@presencas_bp.route('/presencas', methods=['POST'])
@token_required
def registrar_presenca(usuario_atual):
    data = request.get_json()
    aluno = Aluno.query.get(data['id_aluno'])
    if not aluno:
        return jsonify({"message": "Aluno não encontrado!"}), 404
    presenca = Presenca(
        id_aluno=data['id_aluno'],
        data_presenca=data['data_presenca'],
        presente=data['presente']
    )
    db.session.add(presenca)
    db.session.commit()
    return jsonify({"message": "Presença registrada com sucesso!"}), 201

# Listar presenças
@presencas_bp.route('/presencas', methods=['GET'])
@token_required
def listar_presencas(usuario_atual):
    presencas = Presenca.query.all()
    return jsonify([presenca.as_dict() for presenca in presencas])

# Consultar presença de um aluno
@presencas_bp.route('/presencas/<int:id>', methods=['GET'])
@token_required
def consultar_presenca(usuario_atual, id):
    presencas = Presenca.query.filter_by(id_aluno=id).all()
    if presencas:
        return jsonify([presenca.as_dict() for presenca in presencas])
    return jsonify({"message": "Nenhuma presença encontrada!"}), 404

# Atualizar presença
@presencas_bp.route('/presencas/<int:id>', methods=['PUT'])
@token_required
def atualizar_presenca(usuario_atual, id):
    presenca = Presenca.query.get(id)
    if not presenca:
        return jsonify({"message": "Presença não encontrada!"}), 404
    data = request.get_json()
    presenca.id_aluno = data['id_aluno']
    presenca.data_presenca = data['data_presenca']
    presenca.presente = data['presente']
    db.session.commit()
    return jsonify({"message": "Presença atualizada com sucesso!"})

# Deletar presença
@presencas_bp.route('/presencas/<int:id>', methods=['DELETE'])
@token_required
def deletar_presenca(usuario_atual, id):
    presenca = Presenca.query.get(id)
    if not presenca:
        return jsonify({"message": "Presença não encontrada!"}), 404
    db.session.delete(presenca)
    db.session.commit()
    return jsonify({"message": "Presença deletada com sucesso!"})

# Registrar presença para uma turma inteira
@presencas_bp.route('/turmas/<int:id_turma>/presencas', methods=['POST'])
@token_required
def registrar_presenca_turma(usuario_atual, id_turma):
    data = request.get_json()
    data_presenca = data['data_presenca']
    
    # Buscar todos os alunos da turma
    alunos = Aluno.query.filter_by(id_turma=id_turma).all()
    if not alunos:
        return jsonify({"message": "Nenhum aluno encontrado nesta turma!"}), 404
    
    # Registrar presença para cada aluno
    for aluno in alunos:
        # Verificar se já existe registro para este aluno nesta data
        presenca_existente = Presenca.query.filter_by(
            id_aluno=aluno.id_aluno,
            data_presenca=data_presenca
        ).first()
        
        if presenca_existente:
            presenca_existente.presente = data.get('presente', True)
        else:
            presenca = Presenca(
                id_aluno=aluno.id_aluno,
                data_presenca=data_presenca,
                presente=data.get('presente', True)
            )
            db.session.add(presenca)
    
    db.session.commit()
    return jsonify({"message": "Presenças registradas com sucesso!"}), 201

# Gerar relatório de frequência por período
@presencas_bp.route('/relatorios/frequencia', methods=['GET'])
@token_required
def relatorio_frequencia(usuario_atual):
    id_aluno = request.args.get('id_aluno')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    if not data_inicio or not data_fim:
        return jsonify({"message": "Data de início e fim são obrigatórias!"}), 400
    
    try:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Formato de data inválido! Use YYYY-MM-DD"}), 400
    
    query = Presenca.query.filter(
        Presenca.data_presenca >= data_inicio,
        Presenca.data_presenca <= data_fim
    )
    
    if id_aluno:
        query = query.filter_by(id_aluno=id_aluno)
    
    presencas = query.all()
    
    # Calcular estatísticas
    total_dias = (data_fim - data_inicio).days + 1
    dias_uteis = sum(1 for i in range(total_dias) if (data_inicio + timedelta(days=i)).weekday() < 5)
    
    if id_aluno:
        # Relatório para um aluno específico
        aluno = Aluno.query.get(id_aluno)
        if not aluno:
            return jsonify({"message": "Aluno não encontrado!"}), 404
        
        presencas_aluno = [p for p in presencas if p.id_aluno == int(id_aluno)]
        dias_presentes = sum(1 for p in presencas_aluno if p.presente)
        
        return jsonify({
            "aluno": aluno.as_dict(),
            "presencas": [p.as_dict() for p in presencas_aluno],
            "estatisticas": {
                "dias_uteis": dias_uteis,
                "dias_presentes": dias_presentes,
                "percentual_presenca": round((dias_presentes / dias_uteis) * 100, 2) if dias_uteis > 0 else 0
            },
            "periodo": {
                "inicio": data_inicio.strftime('%Y-%m-%d'),
                "fim": data_fim.strftime('%Y-%m-%d')
            }
        })
    else:
        # Relatório geral
        alunos = {}
        for presenca in presencas:
            if presenca.id_aluno not in alunos:
                aluno = Aluno.query.get(presenca.id_aluno)
                alunos[presenca.id_aluno] = {
                    "aluno": aluno.as_dict(),
                    "dias_presentes": 0,
                    "presencas": []
                }
            
            alunos[presenca.id_aluno]["presencas"].append(presenca.as_dict())
            if presenca.presente:
                alunos[presenca.id_aluno]["dias_presentes"] += 1
        
        for aluno_id in alunos:
            alunos[aluno_id]["percentual_presenca"] = round(
                (alunos[aluno_id]["dias_presentes"] / dias_uteis) * 100, 2
            ) if dias_uteis > 0 else 0
        
        return jsonify({
            "alunos": list(alunos.values()),
            "estatisticas_gerais": {
                "dias_uteis": dias_uteis,
                "total_alunos": len(alunos)
            },
            "periodo": {
                "inicio": data_inicio.strftime('%Y-%m-%d'),
                "fim": data_fim.strftime('%Y-%m-%d')
            }
        })
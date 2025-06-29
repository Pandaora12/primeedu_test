from flask import request, jsonify, Blueprint
from src.models import db, Aluno, Pagamento, Presenca, Atividade, Turma
from routes.auth import token_required
from flasgger import swag_from
from datetime import datetime, timedelta
from sqlalchemy import func, and_

relatorios_bp = Blueprint('relatorios', __name__)

# RF006: Relatórios de Pagamentos
@relatorios_bp.route('/relatorios/pagamentos', methods=['GET'])
@token_required
def relatorio_pagamentos(usuario_atual):
    """
    Gerar relatório de pagamentos por período
    ---
    tags:
      - Relatórios
    security:
      - Bearer: []
    parameters:
      - in: query
        name: data_inicio
        type: string
        format: date
        required: true
        description: Data de início (YYYY-MM-DD)
        example: "2024-01-01"
      - in: query
        name: data_fim
        type: string
        format: date
        required: true
        description: Data de fim (YYYY-MM-DD)
        example: "2024-01-31"
      - in: query
        name: status
        type: string
        enum: ["pago", "pendente"]
        description: Filtrar por status
    responses:
      200:
        description: Relatório de pagamentos
        schema:
          type: object
          properties:
            periodo:
              type: object
            resumo:
              type: object
            pagamentos:
              type: array
      400:
        description: Parâmetros inválidos
      401:
        description: Token não fornecido ou inválido
    """
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    status = request.args.get('status')  # 'pago', 'pendente'
    
    if not data_inicio or not data_fim:
        return jsonify({"message": "Data de início e fim são obrigatórias!"}), 400
    
    try:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"message": "Formato de data inválido! Use YYYY-MM-DD"}), 400
    
    query = Pagamento.query.filter(
        Pagamento.data_pagamento >= data_inicio,
        Pagamento.data_pagamento <= data_fim
    )
    
    if status:
        query = query.filter(Pagamento.status == status)
    
    pagamentos = query.all()
    
    # Calcular totais
    total_recebido = sum(float(p.valor_pago) for p in pagamentos if p.status == 'pago')
    total_pendente = sum(float(p.valor_pago) for p in pagamentos if p.status == 'pendente')
    
    resultado = {
        "periodo": {
            "inicio": data_inicio.isoformat(),
            "fim": data_fim.isoformat()
        },
        "resumo": {
            "total_recebido": total_recebido,
            "total_pendente": total_pendente,
            "total_pagamentos": len(pagamentos)
        },
        "pagamentos": [p.as_dict() for p in pagamentos]
    }
    
    return jsonify(resultado)

# RF006: Relatório de Inadimplência
@relatorios_bp.route('/relatorios/inadimplencia', methods=['GET'])
@token_required
def relatorio_inadimplencia(usuario_atual):
    """
    Gerar relatório de inadimplência
    ---
    tags:
      - Relatórios
    security:
      - Bearer: []
    responses:
      200:
        description: Relatório de inadimplência
        schema:
          type: object
          properties:
            data_consulta:
              type: string
            total_inadimplentes:
              type: integer
            valor_total_devido:
              type: number
            inadimplentes:
              type: array
      401:
        description: Token não fornecido ou inválido
    """
    hoje = datetime.now().date()
    
    # Pagamentos vencidos (pendentes e com data anterior a hoje)
    pagamentos_vencidos = Pagamento.query.filter(
        Pagamento.status == 'pendente',
        Pagamento.data_pagamento < hoje
    ).all()
    
    # Agrupar por aluno
    inadimplentes = {}
    for pagamento in pagamentos_vencidos:
        aluno = Aluno.query.get(pagamento.id_aluno)
        if aluno:
            if aluno.id_aluno not in inadimplentes:
                inadimplentes[aluno.id_aluno] = {
                    "aluno": aluno.as_dict(),
                    "pagamentos_vencidos": [],
                    "total_devido": 0
                }
            inadimplentes[aluno.id_aluno]["pagamentos_vencidos"].append(pagamento.as_dict())
            inadimplentes[aluno.id_aluno]["total_devido"] += float(pagamento.valor_pago)
    
    resultado = {
        "data_consulta": hoje.isoformat(),
        "total_inadimplentes": len(inadimplentes),
        "valor_total_devido": sum(i["total_devido"] for i in inadimplentes.values()),
        "inadimplentes": list(inadimplentes.values())
    }
    
    return jsonify(resultado)

# RF009: Relatórios de Presenças
@relatorios_bp.route('/relatorios/presencas', methods=['GET'])
@token_required
def relatorio_presencas(usuario_atual):
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    id_aluno = request.args.get('id_aluno')
    id_turma = request.args.get('id_turma')
    
    if not data_inicio or not data_fim:
        return jsonify({"message": "Data de início e fim são obrigatórias!"}), 400
    
    try:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"message": "Formato de data inválido! Use YYYY-MM-DD"}), 400
    
    query = Presenca.query.filter(
        Presenca.data_presenca >= data_inicio,
        Presenca.data_presenca <= data_fim
    )
    
    if id_aluno:
        query = query.filter(Presenca.id_aluno == id_aluno)
    elif id_turma:
        alunos_turma = Aluno.query.filter_by(id_turma=id_turma).all()
        ids_alunos = [a.id_aluno for a in alunos_turma]
        query = query.filter(Presenca.id_aluno.in_(ids_alunos))
    
    presencas = query.all()
    
    # Calcular estatísticas por aluno
    stats_por_aluno = {}
    for presenca in presencas:
        aluno_id = presenca.id_aluno
        if aluno_id not in stats_por_aluno:
            aluno = Aluno.query.get(aluno_id)
            stats_por_aluno[aluno_id] = {
                "aluno": aluno.as_dict() if aluno else None,
                "total_dias": 0,
                "dias_presentes": 0,
                "dias_ausentes": 0,
                "percentual_frequencia": 0
            }
        
        stats_por_aluno[aluno_id]["total_dias"] += 1
        if presenca.presente:
            stats_por_aluno[aluno_id]["dias_presentes"] += 1
        else:
            stats_por_aluno[aluno_id]["dias_ausentes"] += 1
    
    # Calcular percentuais
    for stats in stats_por_aluno.values():
        if stats["total_dias"] > 0:
            stats["percentual_frequencia"] = round(
                (stats["dias_presentes"] / stats["total_dias"]) * 100, 2
            )
    
    resultado = {
        "periodo": {
            "inicio": data_inicio.isoformat(),
            "fim": data_fim.isoformat()
        },
        "resumo": {
            "total_alunos": len(stats_por_aluno),
            "total_registros": len(presencas)
        },
        "frequencia_por_aluno": list(stats_por_aluno.values())
    }
    
    return jsonify(resultado)

# RF013: Relatório de Atividades (complementar ao existente)
@relatorios_bp.route('/relatorios/atividades-turma', methods=['GET'])
@token_required
def relatorio_atividades_turma(usuario_atual):
    id_turma = request.args.get('id_turma')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    if not id_turma:
        return jsonify({"message": "ID da turma é obrigatório!"}), 400
    
    if not data_inicio or not data_fim:
        return jsonify({"message": "Data de início e fim são obrigatórias!"}), 400
    
    try:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"message": "Formato de data inválido! Use YYYY-MM-DD"}), 400
    
    turma = Turma.query.get(id_turma)
    if not turma:
        return jsonify({"message": "Turma não encontrada!"}), 404
    
    # Buscar atividades da turma no período
    from src.models import Atividade_Turma
    atividades_turma = db.session.query(Atividade_Turma.id_atividade).filter_by(id_turma=id_turma).all()
    atividades_ids = [a[0] for a in atividades_turma]
    
    atividades = Atividade.query.filter(
        Atividade.id_atividade.in_(atividades_ids),
        Atividade.data_realizacao >= data_inicio,
        Atividade.data_realizacao <= data_fim
    ).order_by(Atividade.data_realizacao).all()
    
    resultado = {
        "turma": turma.as_dict(),
        "periodo": {
            "inicio": data_inicio.isoformat(),
            "fim": data_fim.isoformat()
        },
        "total_atividades": len(atividades),
        "atividades": [atividade.as_dict() for atividade in atividades]
    }
    
    return jsonify(resultado)
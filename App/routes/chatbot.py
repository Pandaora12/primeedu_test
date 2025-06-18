from flask import request, jsonify, Blueprint
from src.models import db, Aluno, Pagamento, Presenca, Atividade
from routes.auth import token_required
from datetime import datetime, timedelta

chatbot_bp = Blueprint('chatbot', __name__)

# Endpoint para o chatbot
@chatbot_bp.route('/chatbot', methods=['POST'])
def chatbot_query():
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"message": "Consulta não fornecida"}), 400
    
    query = data['query'].lower()
    user_id = data.get('user_id')
    
    # Processar a consulta
    response = process_query(query, user_id)
    
    return jsonify({
        "response": response,
        "timestamp": datetime.now().isoformat()
    })

def process_query(query, user_id=None):
    # Perguntas sobre pagamentos
    if any(keyword in query for keyword in ['pagamento', 'mensalidade', 'valor', 'vencimento']):
        return handle_payment_query(query, user_id)
    
    # Perguntas sobre presenças
    elif any(keyword in query for keyword in ['presença', 'falta', 'frequência', 'compareceu']):
        return handle_attendance_query(query, user_id)
    
    # Perguntas sobre atividades
    elif any(keyword in query for keyword in ['atividade', 'tarefa', 'exercício', 'aula']):
        return handle_activity_query(query, user_id)
    
    # Perguntas sobre a escola
    elif any(keyword in query for keyword in ['escola', 'horário', 'contato', 'telefone', 'endereço']):
        return handle_school_info_query(query)
    
    # Resposta padrão
    else:
        return "Desculpe, não entendi sua pergunta. Posso ajudar com informações sobre pagamentos, presenças, atividades ou informações gerais da escola."

def handle_payment_query(query, user_id):
    # Se temos o ID do usuário, podemos fornecer informações personalizadas
    if user_id:
        try:
            # Buscar o aluno associado ao usuário
            aluno = Aluno.query.filter_by(id_responsavel=user_id).first()
            
            if not aluno:
                return "Não encontrei informações de alunos associados ao seu perfil."
            
            # Buscar pagamentos do aluno
            pagamentos = Pagamento.query.filter_by(id_aluno=aluno.id_aluno).order_by(Pagamento.data_pagamento.desc()).all()
            
            if not pagamentos:
                return f"Não encontrei registros de pagamentos para {aluno.nome_completo}."
            
            # Verificar pagamentos pendentes
            if 'pendente' in query or 'próximo' in query or 'vencimento' in query:
                pagamentos_pendentes = [p for p in pagamentos if p.status == 'pendente']
                if pagamentos_pendentes:
                    proximo = min(pagamentos_pendentes, key=lambda p: p.data_pagamento)
                    return f"O próximo pagamento de {aluno.nome_completo} vence em {proximo.data_pagamento.strftime('%d/%m/%Y')} no valor de R$ {proximo.valor_pago}."
                else:
                    return f"Não há pagamentos pendentes para {aluno.nome_completo}."
            
            # Verificar último pagamento
            elif 'último' in query or 'recente' in query:
                ultimo = pagamentos[0]
                return f"O último pagamento de {aluno.nome_completo} foi realizado em {ultimo.data_pagamento.strftime('%d/%m/%Y')} no valor de R$ {ultimo.valor_pago}."
            
            # Informações gerais de pagamento
            else:
                return f"O valor da mensalidade de {aluno.nome_completo} é de R$ {pagamentos[0].valor_pago}. O próximo vencimento é em {pagamentos[0].data_pagamento.strftime('%d/%m/%Y')}."
        
        except Exception as e:
            return "Desculpe, ocorreu um erro ao buscar informações de pagamento."
    
    # Respostas genéricas sobre pagamentos
    else:
        if 'como' in query and 'pagar' in query:
            return "Os pagamentos podem ser realizados via boleto bancário, cartão de crédito ou na secretaria da escola."
        elif 'vencimento' in query:
            return "As mensalidades vencem todo dia 10 de cada mês."
        elif 'valor' in query:
            return "O valor das mensalidades varia de acordo com o plano escolhido. Para informações específicas, por favor entre em contato com a secretaria."
        else:
            return "Para informações detalhadas sobre pagamentos, por favor entre em contato com a secretaria pelo telefone (11) 1234-5678."

def handle_attendance_query(query, user_id):
    # Implementação similar à função de pagamentos, mas para presenças
    if user_id:
        try:
            aluno = Aluno.query.filter_by(id_responsavel=user_id).first()
            
            if not aluno:
                return "Não encontrei informações de alunos associados ao seu perfil."
            
            # Buscar presenças recentes
            hoje = datetime.now().date()
            inicio_mes = hoje.replace(day=1)
            presencas = Presenca.query.filter_by(id_aluno=aluno.id_aluno).filter(
                Presenca.data_presenca >= inicio_mes
            ).order_by(Presenca.data_presenca.desc()).all()
            
            if not presencas:
                return f"Não encontrei registros de presença para {aluno.nome_completo} neste mês."
            
            # Verificar presença hoje
            if 'hoje' in query:
                presenca_hoje = next((p for p in presencas if p.data_presenca == hoje), None)
                if presenca_hoje:
                    return f"{aluno.nome_completo} {'compareceu' if presenca_hoje.presente else 'não compareceu'} à escola hoje."
                else:
                    return f"Não há registro de presença para {aluno.nome_completo} hoje."
            
            # Verificar faltas
            elif 'falta' in query:
                faltas = [p for p in presencas if not p.presente]
                if faltas:
                    return f"{aluno.nome_completo} tem {len(faltas)} faltas neste mês."
                else:
                    return f"{aluno.nome_completo} não tem faltas registradas neste mês."
            
            # Informações gerais de frequência
            else:
                total_dias = len(presencas)
                dias_presentes = sum(1 for p in presencas if p.presente)
                percentual = (dias_presentes / total_dias * 100) if total_dias > 0 else 0
                return f"{aluno.nome_completo} tem {percentual:.1f}% de frequência neste mês ({dias_presentes} presenças em {total_dias} dias)."
        
        except Exception as e:
            return "Desculpe, ocorreu um erro ao buscar informações de presença."
    
    # Respostas genéricas sobre presenças
    else:
        if 'justificar' in query:
            return "Para justificar faltas, envie um atestado médico ou uma declaração por escrito para a secretaria da escola."
        elif 'mínimo' in query:
            return "A frequência mínima exigida é de 75% das aulas."
        else:
            return "O controle de presença é realizado diariamente pelos professores. Para mais informações, entre em contato com a secretaria."

def handle_activity_query(query, user_id):
    # Implementação similar às funções anteriores, mas para atividades
    if user_id:
        try:
            aluno = Aluno.query.filter_by(id_responsavel=user_id).first()
            
            if not aluno:
                return "Não encontrei informações de alunos associados ao seu perfil."
            
            # Buscar atividades recentes e futuras
            hoje = datetime.now().date()
            proxima_semana = hoje + timedelta(days=7)
            
            # Buscar atividades associadas ao aluno
            from src.models import Atividade_Aluno
            atividades_ids = db.session.query(Atividade_Aluno.id_atividade).filter_by(id_aluno=aluno.id_aluno).all()
            atividades_ids = [a[0] for a in atividades_ids]
            
            atividades = Atividade.query.filter(
                Atividade.id_atividade.in_(atividades_ids),
                Atividade.data_realizacao >= hoje
            ).order_by(Atividade.data_realizacao).all()
            
            if not atividades:
                return f"Não encontrei atividades programadas para {aluno.nome_completo} nos próximos dias."
            
            # Verificar próximas atividades
            if 'próxima' in query or 'próximo' in query:
                proxima = atividades[0]
                return f"A próxima atividade de {aluno.nome_completo} será em {proxima.data_realizacao.strftime('%d/%m/%Y')}: {proxima.descricao}"
            
            # Listar todas as atividades da semana
            elif 'semana' in query:
                atividades_semana = [a for a in atividades if a.data_realizacao <= proxima_semana]
                if atividades_semana:
                    resposta = f"Atividades de {aluno.nome_completo} para esta semana:\\n"
                    for a in atividades_semana:
                        resposta += f"- {a.data_realizacao.strftime('%d/%m')}: {a.descricao}\\n"
                    return resposta
                else:
                    return f"Não há atividades programadas para {aluno.nome_completo} nesta semana."
            
            # Informações gerais sobre atividades
            else:
                return f"{aluno.nome_completo} tem {len(atividades)} atividades programadas para os próximos dias."
        
        except Exception as e:
            return "Desculpe, ocorreu um erro ao buscar informações de atividades."
    
    # Respostas genéricas sobre atividades
    else:
        return "As atividades são planejadas semanalmente pelos professores. Para informações específicas sobre as atividades da turma do seu filho, por favor entre em contato com a secretaria."

def handle_school_info_query(query):
    # Informações gerais sobre a escola
    if 'horário' in query:
        return "A escola funciona de segunda a sexta-feira, das 7h às 18h."
    elif 'contato' in query or 'telefone' in query:
        return "Você pode entrar em contato com a secretaria pelo telefone (11) 1234-5678 ou pelo e-mail contato@escolainfantil.com.br."
    elif 'endereço' in query:
        return "A escola está localizada na Rua das Flores, 123 - Jardim Primavera."
    elif 'férias' in query:
        return "O período de férias escolares é de 15 de dezembro a 31 de janeiro e de 1 a 15 de julho."
    else:
        return "A Escola Infantil UniFAAT-ADS é uma instituição comprometida com o desenvolvimento integral das crianças. Para mais informações, visite nosso site ou entre em contato com a secretaria."
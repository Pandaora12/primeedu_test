from src.app import db

class Aluno(db.Model):
    id_aluno = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(255), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    id_turma = db.Column(db.Integer, db.ForeignKey('turma.id_turma'))
    nome_responsavel = db.Column(db.String(255), nullable=False)
    telefone_responsavel = db.Column(db.String(20), nullable=False)
    email_responsavel = db.Column(db.String(100), nullable=False)

    def as_dict(self):
        return {
            'id_aluno': self.id_aluno,
            'nome_completo': self.nome_completo,
            'data_nascimento': self.data_nascimento,
            'id_turma': self.id_turma,
            'nome_responsavel': self.nome_responsavel,
            'telefone_responsavel': self.telefone_responsavel,
            'email_responsavel': self.email_responsavel
        }

class Pagamento(db.Model):
    id_pagamento = db.Column(db.Integer, primary_key=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id_aluno'))
    data_pagamento = db.Column(db.Date, nullable=False)
    valor_pago = db.Column(db.Numeric, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    referencia = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def as_dict(self):
        return {
            'id_pagamento': self.id_pagamento,
            'id_aluno': self.id_aluno,
            'data_pagamento': self.data_pagamento,
            'valor_pago': self.valor_pago,
            'forma_pagamento': self.forma_pagamento,
            'referencia': self.referencia,
            'status': self.status
        }

class Presenca(db.Model):
    id_presenca = db.Column(db.Integer, primary_key=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id_aluno'))
    data_presenca = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, nullable=False)

    def as_dict(self):
        return {
            'id_presenca': self.id_presenca,
            'id_aluno': self.id_aluno,
            'data_presenca': self.data_presenca,
            'presente': self.presente
        }

class Atividade(db.Model):
    id_atividade = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    data_realizacao = db.Column(db.Date, nullable=False)

    def as_dict(self):
        return {
            'id_atividade': self.id_atividade,
            'descricao': self.descricao,
            'data_realizacao': self.data_realizacao
        }

class Atividade_Aluno(db.Model):
    id_atividade = db.Column(db.Integer, db.ForeignKey('atividade.id_atividade'), primary_key=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id_aluno'), primary_key=True)

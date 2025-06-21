from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    nivel_acesso = db.Column(db.String(20))
    id_professor = db.Column(db.Integer)
    
    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)
        
    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
    def as_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'login': self.login,
            'nivel_acesso': self.nivel_acesso,
            'id_professor': self.id_professor
        }

class Turma(db.Model):
    id_turma = db.Column(db.Integer, primary_key=True)
    nome_turma = db.Column(db.String(50), nullable=False)
    id_professor = db.Column(db.Integer)
    horario = db.Column(db.String(100))
    alunos = db.relationship('Aluno', backref='turma', lazy=True)
    
    def as_dict(self):
        return {
            'id_turma': self.id_turma,
            'nome_turma': self.nome_turma,
            'id_professor': self.id_professor,
            'horario': self.horario
        }

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
            'data_pagamento': self.data_pagamento.isoformat() if self.data_pagamento else None,
            'valor_pago': float(self.valor_pago) if self.valor_pago else None,
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
            'data_presenca': self.data_presenca.isoformat() if self.data_presenca else None,
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
            'data_realizacao': self.data_realizacao.isoformat() if self.data_realizacao else None
        }

class Atividade_Aluno(db.Model):
    id_atividade = db.Column(db.Integer, db.ForeignKey('atividade.id_atividade'), primary_key=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id_aluno'), primary_key=True)
    
    def as_dict(self):
        return {
            'id_atividade': self.id_atividade,
            'id_aluno': self.id_aluno
        }

class Atividade_Turma(db.Model):
    id_atividade = db.Column(db.Integer, db.ForeignKey('atividade.id_atividade'), primary_key=True)
    id_turma = db.Column(db.Integer, db.ForeignKey('turma.id_turma'), primary_key=True)
    
    def as_dict(self):
        return {
            'id_atividade': self.id_atividade,
            'id_turma': self.id_turma
        }
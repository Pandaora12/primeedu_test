CREATE DATABASE primeEdu;

-- Tabela de Alunos
CREATE TABLE Aluno (
    id_aluno SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    id_turma INT,
    nome_responsavel VARCHAR(255) NOT NULL,
    telefone_responsavel VARCHAR(20) NOT NULL,
    email_responsavel VARCHAR(100) NOT NULL,
    informacoes_adicionais TEXT
);

-- Tabela de Turmas
CREATE TABLE Turma (
    id_turma SERIAL PRIMARY KEY,
    nome_turma VARCHAR(50) NOT NULL,
    id_professor INT,
    horario VARCHAR(100)
);

-- Tabela de Professores
CREATE TABLE Professor (
    id_professor SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(20)
);

-- Tabela de Pagamentos
CREATE TABLE Pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    id_aluno INT REFERENCES Aluno(id_aluno),
    data_pagamento DATE NOT NULL,
    valor_pago DECIMAL(10, 2),
    forma_pagamento VARCHAR(50),
    referencia VARCHAR(100),
    status VARCHAR(20)
);

CREATE TABLE Presenca (
    id_presenca SERIAL PRIMARY KEY,
    id_aluno INT REFERENCES Aluno(id_aluno),
    data_presenca DATE NOT NULL,
    presente BOOLEAN
);

CREATE TABLE Atividade (
    id_atividade SERIAL PRIMARY KEY,
    descricao TEXT,
    data_realizacao DATE NOT NULL
);

-- Tabela de Atividade_Aluno (associação entre atividade e aluno)
CREATE TABLE Atividade_Aluno (
    id_atividade INT REFERENCES Atividade(id_atividade),
    id_aluno INT REFERENCES Aluno(id_aluno),
    PRIMARY KEY (id_atividade, id_aluno)
);

-- Tabela de Usuários
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    nivel_acesso VARCHAR(20),
    id_professor INT REFERENCES Professor(id_professor)
);
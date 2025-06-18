# Sistema de Gerenciamento Escolar Infantil

Este projeto implementa um sistema de gerenciamento escolar infantil para a Escola Infantil UniFAAT-ADS, com foco no controle de pagamentos, presenças e atividades dos alunos.

## Tecnologias Utilizadas

- **Backend**: Python com Flask
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT (JSON Web Tokens)
- **Observabilidade**: Prometheus e Grafana
- **ChatBot**: Implementação básica com Flask

## Estrutura do Projeto

```
App/
├── routes/              # Rotas da API
│   ├── alunos.py        # Rotas para gerenciamento de alunos
│   ├── atividades.py    # Rotas para gerenciamento de atividades
│   ├── auth.py          # Rotas para autenticação
│   ├── chatbot.py       # Rotas para o chatbot
│   ├── pagamentos.py    # Rotas para gerenciamento de pagamentos
│   ├── presencas.py     # Rotas para gerenciamento de presenças
│   ├── turmas.py        # Rotas para gerenciamento de turmas
│   └── __init__.py      # Registro de blueprints
├── src/
│   ├── app.py           # Configuração da aplicação Flask
│   ├── models.py        # Modelos do banco de dados
│   └── __init__.py
├── .env.example         # Exemplo de variáveis de ambiente
├── requirements.txt     # Dependências do projeto
└── run.py              # Ponto de entrada da aplicação
```

## Instalação e Configuração

1. Clone o repositório:
   ```
   git clone <url-do-repositorio>
   cd primeEdu/App
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   ```
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

5. Inicie o banco de dados PostgreSQL:
   ```
   cd ../BD
   docker-compose up -d
   ```

6. Execute a aplicação:
   ```
   cd ../App
   python run.py
   ```

## Módulos do Sistema

### Módulo de Alunos
- Cadastro e gerenciamento de alunos
- Associação de alunos a turmas

### Módulo de Turmas
- Cadastro e gerenciamento de turmas
- Associação de professores a turmas

### Módulo de Pagamentos
- Registro de pagamentos de mensalidades
- Consulta de status de pagamentos
- Geração de relatórios financeiros

### Módulo de Presenças
- Registro diário de presenças
- Consulta de frequência por aluno
- Geração de relatórios de frequência

### Módulo de Atividades
- Cadastro de atividades pedagógicas
- Associação de atividades a alunos ou turmas
- Consulta de atividades por aluno ou turma

### ChatBot
- Suporte básico para pais e responsáveis
- Consulta de informações sobre pagamentos, presenças e atividades

## Autenticação e Segurança

O sistema utiliza autenticação baseada em tokens JWT (JSON Web Tokens). Para acessar as rotas protegidas, é necessário incluir o token no cabeçalho da requisição:

```
Authorization: Bearer <token>
```

## Observabilidade

O sistema está integrado com Prometheus e Grafana para monitoramento e visualização de métricas.

## Documentação da API

### Autenticação
- `POST /login`: Autenticação de usuário
- `POST /registrar`: Registro de novo usuário

### Alunos
- `GET /alunos`: Lista todos os alunos
- `GET /alunos/<id>`: Consulta um aluno específico
- `POST /alunos`: Adiciona um novo aluno
- `PUT /alunos/<id>`: Atualiza dados de um aluno
- `DELETE /alunos/<id>`: Remove um aluno

### Turmas
- `GET /turmas`: Lista todas as turmas
- `GET /turmas/<id>`: Consulta uma turma específica
- `POST /turmas`: Adiciona uma nova turma
- `PUT /turmas/<id>`: Atualiza dados de uma turma
- `DELETE /turmas/<id>`: Remove uma turma

### Pagamentos
- `GET /pagamentos`: Lista todos os pagamentos
- `GET /pagamentos/<id>`: Consulta um pagamento específico
- `POST /pagamentos`: Registra um novo pagamento
- `PUT /pagamentos/<id>`: Atualiza dados de um pagamento
- `DELETE /pagamentos/<id>`: Remove um pagamento
- `GET /alunos/<id_aluno>/pagamentos`: Lista pagamentos de um aluno
- `GET /relatorios/pagamentos`: Gera relatório de pagamentos por período

### Presenças
- `GET /presencas`: Lista todas as presenças
- `GET /presencas/<id>`: Consulta presenças de um aluno
- `POST /presencas`: Registra uma nova presença
- `PUT /presencas/<id>`: Atualiza dados de uma presença
- `DELETE /presencas/<id>`: Remove uma presença
- `POST /turmas/<id_turma>/presencas`: Registra presença para uma turma
- `GET /relatorios/frequencia`: Gera relatório de frequência por período

### Atividades
- `GET /atividades`: Lista todas as atividades
- `GET /atividades/<id>`: Consulta uma atividade específica
- `POST /atividades`: Adiciona uma nova atividade
- `PUT /atividades/<id>`: Atualiza dados de uma atividade
- `DELETE /atividades/<id>`: Remove uma atividade
- `POST /turmas/<id_turma>/atividades`: Adiciona atividade para uma turma
- `GET /turmas/<id_turma>/atividades`: Lista atividades de uma turma
- `GET /alunos/<id_aluno>/atividades`: Lista atividades de um aluno
- `GET /relatorios/atividades`: Gera relatório de atividades por período

### ChatBot
- `POST /chatbot`: Envia uma consulta ao chatbot
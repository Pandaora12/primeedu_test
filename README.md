# 🏫 Sistema de Gerenciamento Escolar Infantil

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0.1-green.svg)](https://flask.palletsprojects.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docker.com)
[![Swagger](https://img.shields.io/badge/API-Swagger-orange.svg)](https://swagger.io)

Sistema completo para gerenciamento de escola infantil com controle de alunos, turmas, pagamentos, presenças e atividades pedagógicas.

## 📋 Funcionalidades

### 👨‍🎓 Gestão de Alunos
- Cadastro completo com dados do responsável
- Consulta e edição de informações
- Histórico acadêmico

### 🏫 Gestão de Turmas
- Organização por turmas e professores
- Controle de horários
- Associação de alunos

### 💰 Controle Financeiro
- Registro de pagamentos e mensalidades
- Relatórios de inadimplência
- Múltiplas formas de pagamento

### ✅ Controle de Presença
- Registro diário de frequência
- Relatórios de presença por período
- Controle de faltas

### 📝 Atividades Pedagógicas
- Cadastro de atividades por turma
- Associação com alunos específicos
- Relatórios de atividades realizadas

### 📊 Relatórios Gerenciais
- Relatórios financeiros detalhados
- Análise de frequência dos alunos
- Dashboards de monitoramento

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.9** - Linguagem principal
- **Flask 2.0.1** - Framework web minimalista
- **SQLAlchemy** - ORM para banco de dados
- **PostgreSQL 13** - Banco de dados relacional
- **JWT** - Autenticação segura
- **Flasgger** - Documentação Swagger automática

### Frontend
- **Streamlit** - Interface web interativa
- **Pandas** - Manipulação de dados
- **Requests** - Comunicação com API

### Infraestrutura
- **Docker & Docker Compose** - Containerização
- **Prometheus** - Coleta de métricas
- **Grafana** - Visualização de dados
- **PostgreSQL Exporter** - Métricas do banco

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   STREAMLIT     │    │   FLASK API     │    │   POSTGRESQL    │
│   Dashboard     │◄──►│   Backend       │◄──►│   Database      │
│   Port: 8501    │    │   Port: 5000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────┐    ┌┴─────────────────┐    ┌─────────────────┐
         │   PROMETHEUS    │    │   GRAFANA        │    │ POSTGRES-EXPORT │
         │   Metrics       │    │   Monitoring     │    │ DB Metrics      │
         │   Port: 9090    │    │   Port: 3000     │    │ Port: 9187      │
         └─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Instalação e Execução

### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/Pandaora12/primeedu_test.git
cd primeEdu
```

2. **Inicie todos os serviços**
```bash
docker-compose up --build -d
```

3. **Verifique se todos os containers estão rodando**
```bash
docker-compose ps
```

4. **Acesse as aplicações**
- **Dashboard Principal**: http://localhost:8501
- **API Documentation**: http://localhost:5000/swagger/
- **Grafana Monitoring**: http://localhost:3000 (admin/admin)
- **Prometheus Metrics**: http://localhost:9090

## 📱 Como Usar

### 1. Navegação
- Use o menu lateral para navegar entre módulos
- **Dashboard**: Visão geral do sistema
- **Alunos**: Gerenciar cadastro de alunos
- **Turmas**: Organizar turmas e professores
- **Pagamentos**: Controle financeiro
- **Presenças**: Registro de frequência
- **Atividades**: Atividades pedagógicas

### 2. API REST
- Documentação completa: http://localhost:5000/swagger/
- Todas as rotas documentadas com exemplos
- Suporte a Postman/Insomnia

## 📊 Monitoramento

### Grafana Dashboard
- **URL**: http://localhost:3000
- **Login**: admin / admin
- **Métricas**: Performance do banco, API, sistema

### Prometheus Metrics
- **URL**: http://localhost:9090
- **Métricas coletadas**:
  - Conexões ativas no PostgreSQL
  - Tempo de resposta da API
  - Uso de recursos do sistema

## 🗄️ Banco de Dados

![image](https://github.com/user-attachments/assets/1933c69c-f9ea-4e45-b6ce-64c00ff49cfb)


### Schema Principal
```sql
-- Principais tabelas
Aluno (id_aluno, nome_completo, data_nascimento, id_turma, ...)
Turma (id_turma, nome_turma, id_professor, horario)
Pagamento (id_pagamento, id_aluno, valor_pago, status, ...)
Presenca (id_presenca, id_aluno, data_presenca, presente)
Atividade (id_atividade, descricao, data_realizacao)
Usuario (id_usuario, login, senha, nivel_acesso)
```

### Backup e Restore
```bash
# Backup
docker-compose exec db pg_dump -U admin primeEdu > backup.sql

# Restore
docker-compose exec -T db psql -U admin primeEdu < backup.sql
```

## 🔧 Comandos Úteis

### Docker Compose
```bash
# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Ver logs
docker-compose logs -f api

# Rebuild containers
docker-compose up --build -d

# Status dos containers
docker-compose ps
```

### Desenvolvimento
```bash
# Acessar container da API
docker-compose exec api bash

# Executar migrations
docker-compose exec api python -c "from src.app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Ver logs em tempo real
docker-compose logs -f
```

## 📚 Documentação da API

### Endpoints Principais

#### Alunos
- `GET /alunos` - Listar alunos
- `POST /alunos` - Adicionar aluno
- `GET /alunos/{id}` - Consultar aluno
- `PUT /alunos/{id}` - Atualizar aluno
- `DELETE /alunos/{id}` - Remover aluno

#### Pagamentos
- `GET /pagamentos` - Listar pagamentos
- `POST /pagamentos` - Registrar pagamento
- `GET /relatorios/inadimplencia` - Relatório de inadimplência

### Exemplos de Uso

#### Adicionar Aluno
```bash
curl -X POST http://localhost:5000/alunos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "nome_completo": "João Silva Santos",
    "data_nascimento": "2010-05-15",
    "id_turma": 1,
    "nome_responsavel": "Maria Silva",
    "telefone_responsavel": "(11) 99999-9999",
    "email_responsavel": "maria.silva@email.com"
  }'
```

## 🛡️ Segurança

### Medidas Implementadas
- ✅ Autenticação JWT com expiração
- ✅ Validação de entrada em todas as rotas
- ✅ Prevenção de SQL Injection via ORM
- ✅ CORS configurado adequadamente
- ✅ Containers isolados via Docker
- ✅ Senhas hasheadas com Werkzeug

### Boas Práticas
- Tokens JWT expiram em 24 horas
- Validação rigorosa de dados de entrada
- Logs de segurança habilitados
- Comunicação interna via rede Docker privada

## 🔄 Backup e Manutenção

### Backup Automático
```bash
# Script de backup diário
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T db pg_dump -U admin primeEdu > "backup_${DATE}.sql"
```

### Limpeza de Logs
```bash
# Limpar logs antigos
docker system prune -f
docker-compose logs --tail=100 api > api_recent.log
```

## 🚨 Troubleshooting

### Problemas Comuns

#### Container não inicia
```bash
# Verificar logs
docker-compose logs container_name

# Rebuild forçado
docker-compose down
docker-compose up --build --force-recreate
```

#### Erro de conexão com banco
```bash
# Verificar se PostgreSQL está rodando
docker-compose ps db

# Testar conexão
docker-compose exec api python -c "from src.models import db; print(db.engine.execute('SELECT 1').scalar())"
```

#### API não responde
```bash
# Verificar status da API
curl http://localhost:5000/

# Verificar logs
docker-compose logs api
```

## 📈 Performance

### Otimizações Implementadas
- Conexões de banco pooled via SQLAlchemy
- Queries otimizadas com relacionamentos lazy
- Cache de sessão no Streamlit
- Containers com recursos limitados

### Monitoramento
- Métricas de performance via Prometheus
- Dashboards de monitoramento no Grafana
- Logs estruturados para análise

### Padrões de Código
- Seguir PEP 8 para Python
- Documentar todas as funções
- Adicionar testes para novas funcionalidades
- Manter cobertura de testes > 80%

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

### FAQ

**Q: Como resetar a senha de admin?**
A: Execute o script de reset no container da API.

**Q: Como adicionar novos usuários?**
A: Use a interface web ou endpoint `/register` da API.

**Q: Como fazer backup dos dados?**
A: Use os comandos de backup PostgreSQL documentados acima.

**Q: Como escalar o sistema?**
A: Adicione réplicas no docker-compose.yml e configure load balancer.

---

**🚀 Sistema pronto para produção com arquitetura escalável e monitoramento completo!**

from flask import Flask, jsonify
from flask_cors import CORS
from src.models import db
from flasgger import Swagger
import os

def create_app():
    app = Flask(__name__)
    
    # Habilitar CORS
    CORS(app)
    
    # Configuração do Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/",
        "swagger_ui_config": {
            "displayRequestDuration": True,
            "docExpansion": "none",
            "filter": True,
            "showExtensions": True,
            "showCommonExtensions": True,
            "tryItOutEnabled": True
        }
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Sistema de Gerenciamento Escolar Infantil - API",
            "description": """API para gerenciamento de alunos, turmas, pagamentos, presenças e atividades escolares.
            
**URLs para Insomnia/Postman:**
- Base URL: `http://localhost:5000`
- Base URL HTTPS: `https://localhost:5000`

**Exemplos de URLs completas:**
- Login: `POST http://localhost:5000/login`
- Listar Alunos: `GET http://localhost:5000/alunos`
- Adicionar Pagamento: `POST http://localhost:5000/pagamentos`

**Autenticação:**
Para rotas protegidas, adicione o header: `Authorization: Bearer {seu_token}`
            """,
            "version": "1.0.0",
            "contact": {
                "name": "Equipe de Desenvolvimento",
                "email": "dev@escolainfantil.com"
            }
        },
        "host": "localhost:5000",
        "basePath": "/",
        "schemes": ["http", "https"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header. Exemplo: 'Bearer {token}'"
            }
        }
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Configuração do Banco de Dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@db:5432/primeEdu'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'minha-chave-secreta-123'
    
    # Inicializa o banco de dados com o app
    db.init_app(app)
    
    @app.route('/')
    def home():
        """
        Endpoint principal da API
        ---
        tags:
          - Sistema
        responses:
          200:
            description: Status da API
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Sistema Escolar - API Funcionando!"
                version:
                  type: string
                  example: "1.0.0"
                status:
                  type: string
                  example: "online"
        """
        return jsonify({
            "message": "Sistema Escolar - API Funcionando!",
            "version": "1.0.0",
            "status": "online",
            "swagger": "/swagger/"
        })
    
    # Registra as rotas
    from routes import register_blueprints
    register_blueprints(app)
    
    # Tratamento de erros
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Recurso não encontrado"}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Erro interno do servidor"}), 500
    
    # Criar tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
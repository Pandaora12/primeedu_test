from flask import Flask, jsonify
from flask_cors import CORS
from src.models import db
import os

def create_app():
    app = Flask(__name__)
    
    # Habilitar CORS
    CORS(app)
    
    # Configuração do Banco de Dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@db:5432/primeEdu'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'minha-chave-secreta-123'
    
    # Inicializa o banco de dados com o app
    db.init_app(app)
    
    @app.route('/')
    def home():
        return jsonify({
            "message": "Sistema Escolar - API Funcionando!",
            "version": "1.0.0",
            "status": "online"
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
from routes.alunos import alunos_bp
from routes.pagamentos import pagamentos_bp
from routes.presencas import presencas_bp
from routes.atividades import atividades_bp
from routes.turmas import turmas_bp
from routes.auth import auth_bp
from routes.chatbot import chatbot_bp
from routes.relatorios import relatorios_bp

def register_blueprints(app):
    app.register_blueprint(alunos_bp)
    app.register_blueprint(pagamentos_bp)
    app.register_blueprint(presencas_bp)
    app.register_blueprint(atividades_bp)
    app.register_blueprint(turmas_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(relatorios_bp)
from flask import request, jsonify, Blueprint
from src.models import db, Usuario
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os

auth_bp = Blueprint('auth', __name__)

# Função para gerar token JWT
def gerar_token(usuario_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': usuario_id
    }
    return jwt.encode(
        payload,
        'minha-chave-secreta-123',
        algorithm='HS256'
    )

# Decorator para verificar token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token não fornecido!'}), 401
        
        try:
            data = jwt.decode(
                token, 
                'minha-chave-secreta-123',
                algorithms=['HS256']
            )
            usuario_atual = Usuario.query.get(data['sub'])
        except:
            return jsonify({'message': 'Token inválido!'}), 401
            
        return f(usuario_atual, *args, **kwargs)
    
    return decorated

# Registrar um novo usuário
@auth_bp.route('/register', methods=['POST'])
def registrar():
    data = request.get_json()
    
    # Verificar se o login já existe
    if Usuario.query.filter_by(login=data['login']).first():
        return jsonify({'message': 'Login já cadastrado!'}), 400
    
    novo_usuario = Usuario(
        login=data['login'],
        nivel_acesso=data.get('nivel_acesso', 'usuario'),
        id_professor=data.get('id_professor')
    )
    novo_usuario.set_senha(data['senha'])
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

# Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    usuario = Usuario.query.filter_by(login=data['login']).first()
    
    if not usuario or not usuario.verificar_senha(data['senha']):
        return jsonify({'message': 'Login ou senha incorretos!'}), 401
    
    token = gerar_token(usuario.id_usuario)
    
    return jsonify({
        'token': token,
        'usuario': usuario.as_dict()
    })

# Rota protegida de exemplo
@auth_bp.route('/perfil', methods=['GET'])
@token_required
def perfil(usuario_atual):
    return jsonify(usuario_atual.as_dict())
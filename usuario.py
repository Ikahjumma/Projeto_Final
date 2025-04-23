from flask import Blueprint #permite exchergar outras rotas
from flask import Flask,render_template, request, redirect
from models import Usuario #classe da estrutura do usuario
from database import db


bp_usuarios = Blueprint("usuarios", __name__, template_folder="templates") #busca os html

#criar usuario
@bp_usuarios.route('/usuarios', methods=['GET', 'POST'])
def usuario():
    if request.method == 'GET':
        return render_template('usuario.html')
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        u = Usuario(nome, email, senha) #objeto
        db.session.add(u) #inserir no banco
        db.session.commit() #aplicar mudança e resgistrar usuario no banco
        return "Cadastro efetuado com sucesso!"

#ver os usuario o read    
@bp_usuarios.route('recovery')
def recovery():
    usuarios = Usuario.query.all() #recuperar todos os objetos, registros que existem na tabela
    return render_template('usuarios_recovery.html', usuarios = usuarios)

#alteração de usuarios
@bp_usuarios.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    u = Usuario.query.get(id) #recuperar usuario

    if request.method == 'GET':
        return render_template ('usuarios_update.html', u = u)
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        u.nome = nome
        u.email = email
        #alterar os dados do usuario que tem o Id X
        db.session.add(u)
        db.session.commit()
        return redirect('/recovery')

#deletar usuarios
@bp_usuarios.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    u = Usuario.query.get(id) #recuperar usuario

    if request.method == 'GET':
        return render_template('usuarios_delete.html', u = u)
    
    if request.method == 'POST':
        db.session.delete(u)
        db.session.commit()
        return 'Usuário excluído com sucesso!'
    

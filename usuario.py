from flask import Blueprint #permite exchergar outras rotas
from flask import Flask, render_template, request, redirect
from models import Usuario #classe da estrutura do usuario
from database import db
from flask import session


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
        
        
        #Verificar se o e-mail já existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return render_template('usuario.html', mensagem='Este e-mail já está cadastrado. Tente outro.')
        
        #cria usuario e salva no banco
        u = Usuario(nome, email, senha) #objeto
        db.session.add(u) #inserir no banco
        db.session.commit() #aplicar mudança e resgistrar usuario no banco
        return render_template('usuario.html', mensagem='Cadastro feito! Agora faça login.')
        
        #apos o cadastro
    return redirect ('/usuarios/usuario')
    


#ROTA DO LOGIN, VERIFICAÇÃO
@bp_usuarios.route('/usuario', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email, senha=senha).first()

        if usuario:
            session['usuario_id'] = usuario.id
            return redirect('/previsao')
        else:
            # Voltar para a página de cadastro/login com erro
            return render_template('usuario.html', mensagem='Email ou senha inválidos.')  
    
    # Se for GET, mostra a tela de login normalmente
    return render_template('usuario.html')

#sair da conta 
@bp_usuarios.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect('/')
  
#ROTA REDEFINIR SENHA
@bp_usuarios.route('/redefinir_senha', methods=['GET', 'POST'])
def redefinir_senha():
    if request.method == 'POST':
        email = request.form.get('email')
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')

        if nova_senha != confirmar_senha:
            return render_template('redefinir_senha.html', mensagem='As senhas não coincidem.')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            usuario.senha = nova_senha
            db.session.commit()
            return render_template('redefinir_senha.html', mensagem='Senha atualizada com sucesso!')
        else:
            return render_template('redefinir_senha.html', mensagem='Email não encontrado.')

    return render_template('redefinir_senha.html')


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
    

#ROTA DELETA CONTA
@bp_usuarios.route('/deletar_meu_usuario', methods=['POST'])
def deletar_meu_usuario():
    usuario_id = session.get('usuario_id')

    if not usuario_id:
        return redirect('/usuarios/usuario')  # Redireciona pro login

    usuario = Usuario.query.get(usuario_id)

    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        session.pop('usuario_id', None)
        return redirect('/')  # Volta pra página inicial ou uma página de despedida

    return "Usuário não encontrado", 404

#ROTA PERFIL DO USUARIO PARA EXCLUSAÕ ALTERAÇÃO
@bp_usuarios.route('/perfil')
def perfil():
    usuario_id = session.get('usuario_id')
    
    if not usuario_id:
        return redirect('/usuarios/usuario')  # Se não estiver logado, redireciona

    usuario = Usuario.query.get(usuario_id)
    
    if usuario:
        return render_template('perfil.html', usuario=usuario)
    
    return "Usuário não encontrado", 404
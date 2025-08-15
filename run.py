from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta_aleatoria'

app.config['banco_de_dados'] = 'models/lojinha.db'

app.config['dados_login'] = []  # Variável global para armazenar os dados do login
UPLOAD_FOLDER = 'static/assets/avatar'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

# Verificar se o usuário já existe
def get_db():
    conexao = sqlite3.connect(app.config['banco_de_dados'])
    conexao.row_factory = sqlite3.Row
    return conexao

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        # Conectar ao banco de dados e verificar o login
        conexao = sqlite3.connect(app.config['banco_de_dados'])
        cursor = conexao.cursor()
        
        # Corrigindo a consulta SQL
        sql = "SELECT * FROM tb_usuarios WHERE usuario = ? AND senha = ?"
        cursor.execute(sql, (usuario, senha))
        
        login_usuario = cursor.fetchone()
        
        if login_usuario:
            app.config['dados_login'] = login_usuario
            return redirect('/cadclientes')
        else:
            return redirect('/')
    
    return render_template('index.html')  # Renderiza a página de login para o método GET


@app.route('/cadusu', methods=['GET', 'POST'])
def cadusu():
        usuario = None  # Define um valor padrão para a variável
        if request.method == 'POST':
            nome_usuario = request.form.get('nome_usuario')
            usuario = request.form.get('usuario')
            senha = request.form.get('senha')
            
            # Verificar se o usuário já existe
            # conn = get_db()
            # cursor = conn.cursor()

            conexao = sqlite3.connect('models/lojinha.db')
            cursor = conexao.cursor()



            cursor.execute("SELECT * FROM tb_usuarios WHERE usuario = ?", (usuario,))
            if cursor.fetchone():
                return "Usuário já existe. Tente outro."
            
                    # Verificar se o usuário já existe

            
            avatar = request.files.get('avatar')

            nome_avatar = None
            if avatar:
                extensao = avatar.filename.split('.')[-1]
                nome_avatar = f"{avatar.filename.strip().lower().replace(' ', '_')}"
                caminho_avatar = os.path.join(app.config['UPLOAD_FOLDER'], avatar.filename)
                avatar.save(caminho_avatar)

            # Inserir novo usuário
            # cursor.execute("INSERT INTO tb_usuarios (nome_usuario, usuario, senha) VALUES (?, ?, ?)", (nome_usuario, usuario, senha))

            cursor.execute("INSERT INTO tb_usuarios (nome_usuario, usuario, senha, avatar) VALUES (?, ?, ?, ?)", (nome_usuario, usuario, senha, nome_avatar))
            conexao.commit()
            conexao.close()

            return redirect('/login')  # Redireciona para a página de login
     
        return render_template('cadusu.html', usuario=usuario)  # Retorna o formulário de cadastro

     
@app.route('/cadclientes', methods=['GET', 'POST'])
def cadclientes():
    if request.method == 'POST':
        nome_completo = request.form.get('nome_completo')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        ende_rua = request.form.get('ende_rua')
        ende_num = request.form.get('ende_num')
        ende_cidade = request.form.get('ende_cidade')
        ende_estado = request.form.get('ende_estado')
        ende_cep = request.form.get('ende_cep')
        data_cadastro = request.form.get('data_cadastro')
        cpf = request.form.get('cpf')
        
        # Verificar se o cliente já existe
        conexao = get_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM tb_clientes WHERE cpf = ?", (cpf,))

        # Inserir novo cliente
        sql = "INSERT INTO tb_clientes (nome_completo, email, telefone, ende_rua, ende_num, ende_cidade, ende_estado, ende_cep, data_cadastro, cpf) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute (sql, (nome_completo, email, telefone, ende_rua, ende_num, ende_cidade, ende_estado, ende_cep, data_cadastro, cpf))
        conexao.commit()
        conexao.close()

        return redirect('/cadclientes')  # Redireciona após sucesso

    # Para o método GET, renderiza o formulário
    return render_template('cadclientes.html', l=app.config['dados_login'])  # Substitua por seu template # Redireciona para a página de cadastro
    

@app.route('/cadfornecedor', methods=['GET', 'POST'])
def cadfornecedor():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        site = request.form.get('site')
        ende_rua = request.form.get('ende_rua')
        ende_num = request.form.get('ende_num')
        ende_cidade = request.form.get('ende_cidade')
        ende_estado = request.form.get('ende_estado')
        ende_cep = request.form.get('ende_cep')
        data_cadastro = request.form.get('data_cadastro')
        cnpj = request.form.get('cnpj')
        
        # Verificar se o cliente já existe
        conexao = get_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM tb_fornecedores WHERE cnpj = ?", (cnpj,))

        # Inserir novo cliente
        sql = "INSERT INTO tb_fornecedores (nome, email, telefone, site, ende_rua, ende_num, ende_cidade, ende_estado, ende_cep, data_cadastro, cnpj) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute (sql, (nome, email, telefone, site, ende_rua, ende_num, ende_cidade, ende_estado, ende_cep, data_cadastro, cnpj))
        conexao.commit()
        conexao.close()

        return redirect('/cadfornecedor')  # Redireciona após sucesso

    # Para o método GET, renderiza o formulário
    return render_template('cadfornecedor.html', l=app.config['dados_login'])  # Substitua por seu template # Redireciona para a página de cadastro
    



@app.route('/consuclientes')
def consuclientes():
        if not app.config['dados_login']:
            return redirect('/')
        
        usuario_logado = app.config['dados_login'] 
        nome_usuario = usuario_logado[3] 

        conexao = sqlite3.connect('models/lojinha.db')
        cursor = conexao.cursor()
          
        cursor.execute("SELECT * FROM tb_clientes")
        clientes = cursor.fetchall()
        conexao.close()

    
        return render_template ("consuclientes.html", clientes=clientes, nome_usuario=nome_usuario, l=app.config['dados_login'])


@app.route('/consufornece')
def consufornece():
        if not app.config['dados_login']:
            return redirect('/')
        
        usuario_logado = app.config['dados_login'] 
        nome_usuario = usuario_logado[3] 

        conexao = sqlite3.connect('models/lojinha.db')
        cursor = conexao.cursor()
          
        cursor.execute("SELECT * FROM tb_fornecedores")
        fornecedores = cursor.fetchall()
        conexao.close()

    
        return render_template ("consufornece.html", fornecedores=fornecedores, nome_usuario=nome_usuario, l=app.config['dados_login'])


@app.route('/consusuarios')
def consusuarios():
        if not app.config['dados_login']:
            return redirect('/')
        
        usuario_logado = app.config['dados_login'] 
        nome_usuario = usuario_logado[3] 

        conexao = sqlite3.connect('models/lojinha.db')
        cursor = conexao.cursor()
          
        cursor.execute("SELECT * FROM tb_usuarios")
        usuarios = cursor.fetchall()
        conexao.close()

    
        return render_template ("consusuarios.html", usuarios=usuarios, nome_usuario=nome_usuario, l=app.config['dados_login'])

@app.route('/editusuario/<int:id>', methods=['GET', 'POST'])
def editusuario(id):
    conexao = sqlite3.connect('models/lojinha.db')
    cursor = conexao.cursor()

    if request.method == 'POST':
        usuario = request.form.get('usuario')  # Corrigido para corresponder ao HTML
        senha = request.form.get('senha')
        nome_usuario = request.form.get('nome_usuario')

        # Atualização no banco de dados
        sql = "UPDATE tb_usuarios SET usuario = ?, senha = ?, nome_usuario = ? WHERE usuario_id = ?"
        cursor.execute(sql, (usuario, senha, nome_usuario, id))

        conexao.commit()
        conexao.close()

        return redirect('/consusuarios')

    else:
        cursor.execute("SELECT * FROM tb_usuarios WHERE usuario_id = ?", (id,))
        usuario = cursor.fetchone()
        conexao.close()


        return render_template('editusuario.html', usuario=usuario, l=app.config['dados_login'])

@app.route('/excluirusuario/<int:id>', methods=['GET'])
def excluirusuario(id):
    conexao = sqlite3.connect('models/lojinha.db')
    cursor = conexao.cursor()
 
    sql = 'DELETE FROM tb_usuarios WHERE usuario_id = ?'
    cursor.execute(sql, (id,))
 
    conexao.commit()
    conexao.close()
 
    return redirect('/consusuarios')


@app.route('/editcliente/<int:id>', methods=['GET', 'POST'])
def editcliente(id):
    conexao = sqlite3.connect('models/lojinha.db')
    cursor = conexao.cursor()
 
    if request.method == 'POST':
        nome_completo = request.form.get('nome_completo')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        ende_rua = request.form.get ('ende_rua')
        ende_num = request.form.get ('ende_num')
        ende_cidade = request.form.get('ende_cidade')
        ende_estado = request.form.get ('ende_estado')
        ende_cep = request.form.get ('ende_cep')
        data_cadastro = request.form.get('data_cadastro')
        cpf = request.form.get ('cpf')

        sql = "UPDATE tb_clientes SET nome_completo = ?, email = ?, telefone = ?, ende_rua = ?, ende_num = ?, ende_cidade = ?, ende_estado = ?, ende_cep = ?, data_cadastro = ?, cpf = ? WHERE cliente_id = ?"
        cursor.execute(sql, (nome_completo, email, telefone, ende_rua, ende_num, ende_cidade, ende_estado, ende_cep, data_cadastro, cpf, id))
 
        conexao.commit()
        conexao.close()
 
        return redirect('/consuclientes')
 
    else:
        cursor.execute("SELECT * FROM tb_clientes WHERE cliente_id = ?", (id,))
        cliente = cursor.fetchone()
        conexao.close()
 
        return render_template('editcliente.html', cliente=cliente, l=app.config['dados_login'])
    

@app.route('/excluircliente/<int:id>', methods=['GET'])
def excluircliente(id):
    conexao = sqlite3.connect('models/lojinha.db')
    cursor = conexao.cursor()
 
    sql = 'DELETE FROM tb_clientes WHERE cliente_id = ?'
    cursor.execute(sql, (id,))
 
    conexao.commit()
    conexao.close()
 
    return redirect('/consuclientes')

@app.route('/vermaiscliente/<int:id>', methods=['GET', 'POST'])
def vermaiscliente(id):
        conexao = sqlite3.connect('models/lojinha.db')
        cursor = conexao.cursor()
          
        cursor.execute("SELECT * FROM tb_clientes WHERE cliente_id = ?", (id,))
        cliente = cursor.fetchone()
        conexao.close()

        return render_template ("vermaiscliente.html", cliente=cliente, l=app.config['dados_login'])

@app.route('/editfornece/<int:id>', methods=['GET', 'POST'])
def editcfornece(id):
    conexao = sqlite3.connect('models/lojinha.db')
    cursor = conexao.cursor()
 
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        site = request.form.get('site')
        ende_rua = request.form.get ('ende_rua')
        ende_num = request.form.get ('ende_num')
        ende_cidade = request.form.get('ende_cidade')
        ende_estado = request.form.get ('ende_estado')
        ende_cep = request.form.get ('ende_cep')
        data_cadastro = request.form.get('data_cadastro')
        cnpj = request.form.get ('cnpj')

        sql = "UPDATE tb_fornecedores SET nome = ?, email = ?, telefone = ?, site = ?, ende_rua = ?, ende_num = ?, ende_cidade = ?, ende_estado = ?, ende_cep = ?, data_cadastro = ?, cnpj = ? WHERE fornecedor_id = ?"
        cursor.execute(sql, (nome, email, telefone, site, ende_rua, ende_num, ende_cidade, ende_estado, ende_cep, data_cadastro, cnpj, id))
 
        conexao.commit()
        conexao.close()
 
        return redirect('/consufornece')
 
    else:
        cursor.execute("SELECT * FROM tb_fornecedores WHERE fornecedor_id = ?", (id,))
        fornecedor = cursor.fetchone()
        conexao.close()
 
        return render_template('editfornece.html', fornecedor=fornecedor, l=app.config['dados_login'])
    

@app.route('/excluirfornece/<int:id>', methods=['GET'])
def excluirfornece (id):
    conexao = sqlite3.connect('models/lojinha.db')
    cursor = conexao.cursor()
 
    sql = 'DELETE FROM tb_fornecedores WHERE fornecedor_id = ?'
    cursor.execute(sql, (id,))
 
    conexao.commit()
    conexao.close()
 
    session['dados_login'] = app.config['dados_login']

    return redirect('/consufornece')

@app.route('/vermaisfornece/<int:id>', methods=['GET', 'POST'])
def vermaisfornece(id):
        conexao = sqlite3.connect('models/lojinha.db')
        cursor = conexao.cursor()
          
        cursor.execute("SELECT * FROM tb_fornecedores WHERE fornecedor_id = ?", (id,))
        fornecedor = cursor.fetchone()
        conexao.close()

        return render_template ("vermaisfornecedor.html", fornecedor=fornecedor, l=app.config['dados_login'])

@app.route('/logout')
def logout():
    app.config['dados_login'] = []
    return redirect('/')


app.run(host='10.144.227.191', port=80, debug=True)


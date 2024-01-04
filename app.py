from flask import Flask
from PIL import Image
from flask import render_template, redirect, session, jsonify
from flask import request, abort
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'loja AtemporalBrand'

imagens = [
    ('static/imagens/feminino1.jpg', 1),
    ('static/imagens/feminino2.jpg', 2),
    ('static/imagens/feminino3.jpg', 3),
    ('static/imagens/feminino4.jpg', 4),
    ('static/imagens/feminino5.jpg', 5),
    ('static/imagens/feminino6.jpg', 6),
    ('static/imagens/feminino7.jpg', 7),
    ('static/imagens/feminino8.jpg', 8),
    ('static/imagens/masculino1.jpg', 9),
    ('static/imagens/masculino2.jpg', 10),
    ('static/imagens/masculino3.jpg', 11),
    ('static/imagens/masculino4.jpg', 12),
    ('static/imagens/masculino5.jpg', 13),
    ('static/imagens/masculino6.jpg', 14),
    ('static/imagens/masculino7.jpg', 15),
    ('static/imagens/masculino8.jpg', 16),
]

# Tamanho desejado para as imagens (largura x altura)
novo_tamanho = (150, 150)  # Ajuste o tamanho conforme necessário

for imagem_path, produto_id in imagens:
    # Abre a imagem
    imagem = Image.open(imagem_path)

    # Redimensiona a imagem
    imagem_redimensionada = imagem.resize(novo_tamanho)

    # Sobrescreve a imagem original com a imagem redimensionada
    imagem_redimensionada.save(imagem_path)

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'AtemporalBrand'

# Inicialização do MySQL
mysql = MySQL()
mysql.init_app(app)


@app.route('/')
def inicial():
    return render_template('principal.html')

# ...

@app.route('/pesquisar', methods=['GET'])
def pesquisar():
    # Obtém o termo de pesquisa da consulta GET
    termo_pesquisa = request.args.get('q', '')

    # Conecta-se ao banco de dados
    cursor = mysql.connection.cursor()

    # Realiza a consulta no banco de dados para obter informações do produto e suas imagens
    cursor.execute("""
        SELECT Produto.produtoID, Produto.nome, Produto.descricao, Produto.quantProduto, Produto.valorProduto, Produto.tamanhoProduto, Imagem.url
        FROM Produto
        LEFT JOIN Imagem ON Produto.produtoID = Imagem.produtoID
        WHERE Produto.nome LIKE %s
    """, ('%' + termo_pesquisa + '%',))
    
    resultados = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    cursor.close()

    # Retorna os resultados para o template HTML
    return render_template('pesquisa.html', resultados=resultados)

@app.route('/Cliente/<nome>')
def cliente(nome):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM cliente WHERE nome = %s", (nome,))
    data = cursor.fetchall()
    cursor.close()
    return str(data)

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/cadastro.html')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        senha = request.form['senha']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO cliente (nome, email, cpf, senha) VALUES (%s, %s, %s, %s)", (nome, email, cpf, senha))
        user = cursor.fetchone()
        mysql.connection.commit()
        cursor.close()

        return redirect
    
@app.route('/enviar', methods=['GET', 'POST'])
def enviar():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM cliente WHERE email = %s AND senha = %s", (email, senha))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Armazena o ID do usuário na sessão
            session['clienteid'] = user[0]
            
            # Redireciona para a página de conta do usuário
            return redirect('/minha_conta')
        else:
            return redirect('/login.html') 

    return render_template('login.html') 

@app.route('/minha_conta')
def minha_conta():
    # Verifica se o usuário está autenticado
    if 'clienteid' in session:
        clienteid = session['clienteid']

        # Consulta o banco de dados para obter informações específicas do usuário
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM cliente WHERE clienteid = %s", (clienteid,))
        user_info = cursor.fetchone()
        cursor.close()

        # Renderiza a página de conta do usuário com as informações obtidas
        return render_template('principal.html', user_info=user_info)
    else:
        # Se o usuário não está autenticado, redireciona para a página de login
        return redirect('/login.html') 

@app.route('/carrinho.html')
def carrinho():
    return render_template('carrinho.html')

@app.route('/Produto')
def produtos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM produto")
    data = cursor.fetchall()
    cursor.close()
    return str(data)


if __name__ == '__main__':
    app.run(debug=True)

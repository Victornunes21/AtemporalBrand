from flask import Flask
from PIL import Image
from flask import render_template, redirect, session, jsonify
from flask import request, abort
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'loja AtemporalBrand'


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

@app.route('/novidades.html')
def novidades():
    return render_template('novidades.html')

@app.route('/cadastrar_prod.html')
def cadastrar_prod():
    return render_template('cadastrar_prod.html')

carrinho_itens = []  # Lista para armazenar os itens no carrinho

@app.route('/adicionar_ao_carrinho', methods=['POST'])
def adicionar_ao_carrinho():
    try:
        data = request.json
        produto_id = data.get('produto_id')
        quantidade = data.get('quantidade')

        # Lógica para adicionar o item ao carrinho
        carrinho_itens.append({'produto_id': produto_id, 'quantidade': quantidade})

        resposta = {'status': 'success', 'mensagem': f'Produto {produto_id} adicionado ao carrinho'}
        return jsonify(resposta)
    except Exception as e:
        return jsonify({'status': 'error', 'mensagem': str(e)})

@app.route('/carrinho')
def exibir_carrinho():
    # Lógica para exibir os itens no carrinho
    return render_template('carrinho.html', carrinho_itens=carrinho_itens)


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

@app.route('/fornecedor.html')
def fornecedor():
    return render_template('fornecedor.html')

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

        return redirect('/minha_conta')
    
@app.route('/cadastrarforn', methods =['POST'])
def cadastrarforn():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Fornecedor (nome, email,  senha) VALUES (%s, %s,  %s)", (nome, email, senha))
        user = cursor.fetchone()

        mysql.connection.commit()
        cursor.close()

        return redirect('/')
    
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

@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        quantidade = request.form['quantidade']
        valor = request.form['valor']

        # Adapte esta lógica para inserir os dados no seu banco de dados
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO Produto (nome, descricao, quantProduto, valorProduto)
            VALUES (%s, %s, %s, %s)
        """, (nome, descricao, quantidade, valor))

        mysql.connection.commit()
        cursor.close()

        # Redirecione para a página de sucesso ou qualquer outra página
        return redirect('/cadastrar_prod')

if __name__ == '__main__':
    app.run(debug=True)
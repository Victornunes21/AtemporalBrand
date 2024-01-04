from flask import Flask
from flask import render_template, redirect, session
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

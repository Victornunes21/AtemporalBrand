from flask import Flask
from flask import render_template
from flask import request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'AtemporalBrand'

# Inicialização do MySQL
mysql = MySQL()
mysql.init_app(app)

usuarios = {
    'cliente1': 'cliente@gmail.com1'
}

@app.route('/')
def inicial():
    return render_template('principal.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    return render_template('cadastro.html')
    c = request.form['usuario']
    m = request.form['mens']
    usuarios[c] = m
    return render_template('resposta.html', usuario=usuarios)

@app.route('/Produto')
def produtos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM produto")
    data = cursor.fetchall()
    cursor.close()
    return str(data)

@app.route('/Cliente/<nome>')
def cliente(nome):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM cliente WHERE nome = %s", (nome,))
    data = cursor.fetchall()
    cursor.close()
    return str(data)

if __name__ == '__main__':
    app.run(debug=True)

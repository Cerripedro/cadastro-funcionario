from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Defina uma chave secreta para o Flash

# Função para criar a tabela de funcionários no banco de dados
def criar_tabela():
    conn = sqlite3.connect('funcionarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER,
            endereco TEXT,
            cargo TEXT,
            salario REAL,
            telefone TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Página inicial com a lista de funcionários
@app.route('/')
def index():
    criar_tabela()
    conn = sqlite3.connect('funcionarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM funcionarios')
    funcionarios = cursor.fetchall()
    conn.close()
    return render_template('index.html', funcionarios=funcionarios)

# Página de cadastro de funcionário
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        endereco = request.form['endereco']
        cargo = request.form['cargo']
        salario = request.form['salario']
        telefone = request.form['telefone']
        email = request.form['email']

        conn = sqlite3.connect('funcionarios.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO funcionarios (nome, idade, endereco, cargo, salario, telefone, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, idade, endereco, cargo, salario, telefone, email))
        conn.commit()
        conn.close()

        flash('Funcionário cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))

    return render_template('cadastrar.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

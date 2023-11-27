import sqlite3

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect('seu_banco_de_dados.db')  # Nome do arquivo do banco de dados
    cursor = conn.cursor()

    # Criação da tabela 'textos'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS textos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT
        )
    ''')

    conn.commit()
    conn.close()


# Rota para criar o banco de dados e a tabela (chame esta rota apenas uma vez para criar o banco)
@app.route('/criar_banco_de_dados')
def criar_banco_de_dados():
    create_database()
    return 'Banco de dados criado com sucesso!'


@app.route('/inserir_texto', methods=['POST'])
def inserir_texto():
    texto = request.form['texto']

    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Inserindo o texto na tabela 'textos'
    cursor.execute('INSERT INTO textos (texto) VALUES (?)', (texto,))

    conn.commit()
    conn.close()

    # Redireciona de volta para a página de cadastro
    return redirect('/db')

@app.route('/db')
def selecionar_textos():
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Seleciona todos os textos da tabela 'textos'
    cursor.execute('SELECT * FROM textos')
    textos = cursor.fetchall()

    conn.close()

    # Renderiza a página com os textos recuperados
    return render_template('Cadastro2.html', textos=textos)


@app.route('/editar_texto/<int:texto_id>')
def editar_texto(texto_id):
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Seleciona o texto específico da tabela 'textos' pelo ID
    cursor.execute('SELECT * FROM textos WHERE id = ?', (texto_id,))
    texto = cursor.fetchone()

    conn.close()

    # Renderiza a página de edição com o texto específico
    return render_template('editar_texto.html', texto=texto)


# Rota para processar a solicitação de edição
@app.route('/atualizar_texto/<int:texto_id>', methods=['POST'])
def atualizar_texto(texto_id):
    novo_texto = request.form['novo_texto']

    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Atualiza o texto na tabela 'textos'
    cursor.execute('UPDATE textos SET texto = ? WHERE id = ?', (novo_texto, texto_id))

    conn.commit()
    conn.close()

    # Redireciona de volta para a página de cadastro ou para onde você preferir
    return redirect('/db')

# Rota para excluir texto
@app.route('/excluir_texto/<int:texto_id>', methods=['POST'])
def excluir_texto(texto_id):
    conn = sqlite3.connect('seu_banco_de_dados.db')
    cursor = conn.cursor()

    # Exclui o texto da tabela 'textos'
    cursor.execute('DELETE FROM textos WHERE id = ?', (texto_id,))

    conn.commit()
    conn.close()

    # Redireciona de volta para a página de cadastro
    return redirect('/db')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/Cadastro')
def Cadastro():
    return render_template("Cadastro.html")

@app.route('/Contatos')
def Contatos():
    return render_template("Contatos.html")

@app.route('/Eventos')
def Eventos():
    return render_template("Eventos.html")

@app.route("/Informativos")
def Informativos():
    return render_template("Informativos.html")

@app.route("/Loja")
def Loja():
    return render_template("loja.html")

@app.route("/Home")
def PagHome():
    return render_template("PagHome.html")



app.run()
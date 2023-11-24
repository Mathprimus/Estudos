from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_table():
    # Conectar ao banco de dados
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Criar a tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY,
            text TEXT
        )
    ''')

    # Commit e fechar a conexão
    connection.commit()
    connection.close()

def insert_text(new_text):
    # Conectar ao banco de dados
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Inserir novo texto na tabela
    cursor.execute('INSERT INTO texts (text) VALUES (?)', (new_text,))

    # Commit e fechar a conexão
    connection.commit()
    connection.close()

def update_text(text_id, updated_text):
    # Conectar ao banco de dados
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Atualizar o texto na tabela
    cursor.execute('UPDATE texts SET text=? WHERE id=?', (updated_text, text_id))

    # Commit e fechar a conexão
    connection.commit()
    connection.close()

def select_text(text_id):
    # Conectar ao banco de dados
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Obter o texto pelo ID
    cursor.execute('SELECT * FROM texts WHERE id=?', (text_id,))
    data = cursor.fetchone()

    # Fechar a conexão
    connection.close()

    return data[1] if data else None

def get_all_texts():
    # Conectar ao banco de dados
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Obter todos os dados da tabela
    cursor.execute('SELECT * FROM texts')
    all_texts = cursor.fetchall()

    # Fechar a conexão
    connection.close()

    return all_texts

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        action = request.form['action']
        text_id = request.form.get('text_id', None)

        if action == 'insert':
            # Inserir novo texto
            new_text = request.form['text']
            insert_text(new_text)
        elif action == 'edit' and text_id is not None and text_id.isdigit():
            # Redirecionar para a página de edição se text_id for um número válido
            return redirect(url_for('edit_data', text_id=text_id))
        elif action == 'select':
            # Obter o texto selecionado e exibi-lo
            selected_text = select_text(text_id)
            return render_template('index.html', selected_text=selected_text)

    # Obter todos os dados para a seleção
    all_texts = get_all_texts()

    return render_template('index.html', all_texts=all_texts)

# Rota para editar o texto na tabela
@app.route('/edit_data/<text_id>', methods=['GET', 'POST'])
def edit_data(text_id):
    if request.method == 'POST':
        # Se o formulário foi submetido, atualizar o texto no banco de dados
        updated_text = request.form['text']
        update_text(text_id, updated_text)
        return redirect(url_for('main'))

    # Se for uma solicitação GET, obter o texto atual da tabela
    current_text = select_text(text_id)

    return render_template('edit.html', text_id=text_id, current_text=current_text)


if __name__ == '__main__':
    create_table()
    app.run(debug=True)

# Importa as bibliotecas
import os
import csv
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Definindo a variável de ambiente
os.environ['FLASK_DEBUG'] = 'True'

# Configurando o modo de depuração com base na variável de ambiente
app.debug = os.environ.get('FLASK_DEBUG') == 'True'


#######################################  Rotas  ###############################################

# Definindo as rotas das paginas
@app.route('/')
def ola():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/index_sobre.html')
def sobre():
    return render_template('index_sobre.html')

@app.route('/index_produtos.html')
def produtos():
    return render_template('index_produtos.html')

@app.route('/index_portifolios.html')
def portifolios():
    return render_template('index_portifolios.html')

@app.route('/index_avaliacoes.html')
def avaliacoes_geral():
    return render_template('index_avaliacoes.html')


############################   Avaliações(Glosario)    ########################################

# Rota das Avaliaçoes e manipulação do arquivo csv
@app.route('/avaliacoes')
def avaliacoes():

    # Cria a lista
    avaliacoes_e_notas = []

    # Ler o arquivo, lista e vai redericionar para a pagina de avaliações
    with open(
            'avaliacoes.csv',
            newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            avaliacoes_e_notas.append(l)

    return render_template('index_avaliacoes.html',
                           avaliacoes=avaliacoes_e_notas)


# Rota para a pagina de nova avaliação
@app.route('/nova_avaliacoes')
def nova_avaliacao():
    return render_template('index_add_avaliacoes.html')


# Rota de Criação de novas avaliações para o arquivo csv
@app.route('/criar_nota', methods=['POST'])
def criar_nota():
    # Cria 2 variaveis e armazena as informações do formulario neles
    nota = request.form['nota']
    descricao = request.form['descricao']

    # Ler o arquivo, escreve o valor das variaveis, salva e 
    # vai redericionar para a pagina de avaliações
    with open(
            'avaliacoes.csv', 'a',
            newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([nota, descricao])

    return redirect(url_for('avaliacoes'))


# Rota de Remover avaliações para o arquivo csv
@app.route('/excluir_nota/<int:nota_id>', methods=['POST'])
def excluir_nota(nota_id):

    # Vai ler o arquivo
    with open('avaliacoes.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    # Remove a linha com base no ID do formulario
    if 0 <= nota_id < len(linhas):
        del linhas[nota_id]

        # Salvar as alterações de volta no arquivo
        with open('avaliacoes.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(linhas)
        # Limpa a proxima linha devido ao bug da biblioteca do csv
        if 0 <= nota_id < len(linhas):
            del linhas[nota_id]

    # Redericiona para a pagina de avaliações
    return redirect(url_for('avaliacoes'))

    if 0 <= nota_id < len(linhas):
        del linhas[nota_id]

#############################   Carrinho(Tarefas)   ###########################################

# Rota para a pagina do contato
@app.route('/index_contato.html')
def contato():
    return render_template('index_contato.html', carrinho=carrinho)

# Cria a lista
carrinho = []

# Rota de criação de um item no carrinho
@app.route('/add', methods=['POST'])
def add():
    # Cria a variavel de itens
    item = request.form['item']
    # Armazena as informações do formulario
    carrinho.append({'task': item, 'done': False})
    #Salva no csv
    save_cart_to_csv()
    # Atualiza a pagina
    return redirect(url_for('contato'))

# Rota para editar os itens do carrinho
@app.route('/edit/<int:index_contato>', methods=['GET', 'POST'])
def editar_index_contato(index_contato):
    item = carrinho[index_contato]
    if request.method == 'POST':
        item['task'] = request.form['item']
        save_cart_to_csv()
        return redirect(url_for('contato'))
    else:
        return render_template('edit_index_contato.html', item=item, index_contato=index_contato)

@app.route('/check/<int:index_contato>')
def check(index_contato):
    carrinho[index_contato]['done'] = not carrinho[index_contato]['done']
    save_cart_to_csv()
    return redirect(url_for('contato'))

@app.route('/delete/<int:index_contato>')
def delete(index_contato):
    del carrinho[index_contato]
    save_cart_to_csv()
    return redirect(url_for('contato'))

def save_cart_to_csv():
    with open('carrinho.csv', 'w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        for item in carrinho:
            writer.writerow([item['task'], item['done']])

def load_cart_from_csv():
    try:
        with open('carrinho.csv', newline='', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo, delimiter=';')
            carrinho.clear()
            for linha in reader:
                task, done = linha
                carrinho.append({'task': task, 'done': done.lower() == 'true'})
    except FileNotFoundError:
        pass


# Antes de rodar o aplicativo, abre a função de carreguar o carrinho a partir do CSV
load_cart_from_csv()

###############################################################################################
# Roda o aplicativo Flask
if __name__ == "__main__":
    app.run()

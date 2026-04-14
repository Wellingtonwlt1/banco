import PySimpleGUI as sg
import psycopg2

# Configuração da conexão com PostgreSQL
db_config = {
    "host": "localhost",
    "port": "5432",
    "dbname": "mercado",   # nome do banco sem acento
    "user": "postgres",
    "password": "592765"   # senha sem acento
}

# Cria tabela se não existir
conexao = psycopg2.connect(**db_config)
cursor = conexao.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS suplemento (
    id SERIAL PRIMARY KEY,
    lote VARCHAR(50),
    produto VARCHAR(100),
    fornecedor VARCHAR(100)
)
""")
conexao.commit()
cursor.close()
conexao.close()

# Carregar dados existentes do banco
conexao = psycopg2.connect(**db_config)
cursor = conexao.cursor()
cursor.execute("SELECT id, lote, produto, fornecedor FROM suplemento ORDER BY id")
dados_db = cursor.fetchall()
cursor.close()
conexao.close()

# Dados para exibir na tabela (sem o id)
dados = [[row[1], row[2], row[3]] for row in dados_db]
ids = [row[0] for row in dados_db]  # lista de ids reais

Titulos = ['Lote', 'Produto', 'Fornecedor']

layout = [
    [sg.Text(Titulos[0]), sg.Input(size=5, key=Titulos[0])],
    [sg.Text(Titulos[1]), sg.Input(size=20, key=Titulos[1])],
    [sg.Text(Titulos[2]), sg.Combo(['Fornecedor 1', 'Fornecedor 2', 'Fornecedor 3'], key=Titulos[2])],
    [sg.Button('Adicionar'), sg.Button('Editar'), sg.Button('Salvar', disabled=True), sg.Button('Excluir'), sg.Exit('Sair')],
    [sg.Table(values=dados, headings=Titulos, key='tabela', enable_events=True, auto_size_columns=True)]
]

window = sg.Window('Sistema de gerência de suplementos', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Sair':
        break

    if event == 'Adicionar':
        lote, produto, fornecedor = values[Titulos[0]], values[Titulos[1]], values[Titulos[2]]
        if not lote or not produto or not fornecedor:
            sg.popup("Preencha todos os campos!")
            continue

        # Insere no PostgreSQL
        conexao = psycopg2.connect(**db_config)
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO suplemento (lote, produto, fornecedor) VALUES (%s, %s, %s) RETURNING id",
                       (lote, produto, fornecedor))
        novo_id = cursor.fetchone()[0]
        conexao.commit()
        cursor.close()
        conexao.close()

        # Atualiza listas e tabela
        ids.append(novo_id)
        dados.append([lote, produto, fornecedor])
        window['tabela'].update(values=dados)

        # Limpa os campos
        for i in range(3):
            window[Titulos[i]].update(value='')

    if event == 'Editar':
        if values['tabela'] == []:
            sg.popup('Nenhuma linha selecionada')
        else:
            editarLinha = values['tabela'][0]
            sg.popup('Editar linha selecionada')
            for i in range(3):
                window[Titulos[i]].update(value=dados[editarLinha][i])
            window['Salvar'].update(disabled=False)

    if event == 'Salvar':
        if values['tabela'] == []:
            sg.popup('Nenhuma linha selecionada para salvar')
        else:
            editarLinha = values['tabela'][0]
            lote, produto, fornecedor = values[Titulos[0]], values[Titulos[1]], values[Titulos[2]]
            dados[editarLinha] = [lote, produto, fornecedor]
            window['tabela'].update(values=dados)
            window['Salvar'].update(disabled=True)

            # Atualiza no PostgreSQL usando o id real
            conexao = psycopg2.connect(**db_config)
            cursor = conexao.cursor()
            cursor.execute("UPDATE suplemento SET lote=%s, produto=%s, fornecedor=%s WHERE id=%s",
                           (lote, produto, fornecedor, ids[editarLinha]))
            conexao.commit()
            cursor.close()
            conexao.close()

    if event == 'Excluir':
        if values['tabela'] == []:
            sg.popup('Nenhuma linha selecionada para excluir')
        else:
            excluirLinha = values['tabela'][0]
            id_excluir = ids[excluirLinha]

            # Remove do PostgreSQL
            conexao = psycopg2.connect(**db_config)
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM suplemento WHERE id=%s", (id_excluir,))
            conexao.commit()
            cursor.close()
            conexao.close()

            # Atualiza listas e tabela
            ids.pop(excluirLinha)
            dados.pop(excluirLinha)
            window['tabela'].update(values=dados)

window.close()
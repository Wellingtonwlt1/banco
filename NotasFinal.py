import tkinter as tk
from tkinter import ttk
import pandas as pd

# Janela principal
janela = tk.Tk()
janela.title("Sistema de cadastro de Alunos")
janela.geometry("820x600")

# Labels e Entradas
lblNome = tk.Label(janela, text="Nome do Aluno:")
lblNota1 = tk.Label(janela, text="Nota 1")
lblNota2 = tk.Label(janela, text="Nota 2")

txtNome = tk.Entry(janela, bd=3)
txtNota1 = tk.Entry(janela)
txtNota2 = tk.Entry(janela)

# Posicionamento com grid
lblNome.grid(row=0, column=0, padx=5, pady=5, sticky="w")
txtNome.grid(row=0, column=1, padx=5, pady=5)

lblNota1.grid(row=1, column=0, padx=5, pady=5, sticky="w")
txtNota1.grid(row=1, column=1, padx=5, pady=5)

lblNota2.grid(row=2, column=0, padx=5, pady=5, sticky="w")
txtNota2.grid(row=2, column=1, padx=5, pady=5)

# Tabela
colunas = ("Aluno", "Nota1", "Nota2", "Média", "Situação")
treeMedias = ttk.Treeview(janela, columns=colunas, show="headings")

for coluna in colunas:
    treeMedias.heading(coluna, text=coluna)
    treeMedias.column(coluna, width=100)

treeMedias.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Scrollbar
scrollbar = ttk.Scrollbar(janela, orient="vertical", command=treeMedias.yview)
treeMedias.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=4, column=3, sticky="ns")

# Funções
def verificar_situacao(nota1, nota2):
    media = (nota1 + nota2) / 2
    if media >= 7.0:
        situacao = "Aprovado"
    elif media >= 5.0:
        situacao = "Em Recuperação"
    else:
        situacao = "Reprovado"
    return media, situacao

def cadastrar_aluno():
    try:
        nome = txtNome.get()
        nota1 = float(txtNota1.get())
        nota2 = float(txtNota2.get())

        media, situacao = verificar_situacao(nota1, nota2)

        treeMedias.insert("", "end", values=(nome, nota1, nota2, f"{media:.2f}", situacao))
        salvar_dados()
    except ValueError:
        print("Erro: Digite valores numéricos válidos.")
    finally:
        txtNome.delete(0, "end")
        txtNota1.delete(0, "end")
        txtNota2.delete(0, "end")

def salvar_dados():
    dados = []
    for line in treeMedias.get_children():
        valores = treeMedias.item(line)["values"]
        dados.append(valores)

    df = pd.DataFrame(data=dados, columns=colunas)
    df.to_excel("planilhaAlunos.xlsx", index=False, engine="openpyxl")
    print("Dados salvos com sucesso.")

def carregar_dados_iniciais():
    try:
        df = pd.read_excel("planilhaAlunos.xlsx")
        for _, row in df.iterrows():
            treeMedias.insert("", "end", values=(row["Aluno"], row["Nota1"], row["Nota2"], row["Média"], row["Situação"]))
    except FileNotFoundError:
        print("Nenhum dado encontrado.")

# Botão
btnCadastrar = tk.Button(janela, text="Cadastrar", command=cadastrar_aluno)
btnCadastrar.grid(row=3, column=0, columnspan=2, pady=10)

# Carregar dados existentes
carregar_dados_iniciais()

# Loop principal
janela.mainloop()
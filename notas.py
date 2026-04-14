# Importa a biblioteca tkinter para criar interfaces gráficas
import tkinter as tk
# Importa ttk (Themed Tkinter Widgets), que fornece widgets mais modernos
from tkinter import ttk

# Criação da janela principal
janela = tk.Tk()
janela.title("Sistema de Gestão Escolar")   # Define o título da janela
janela.geometry("600x400")                  # Define o tamanho da janela

# Label para o campo de nome do aluno
tk.Label(janela, text="Nome do Aluno:").pack()

# Campos de entrada para nome e notas
entrada_nome = tk.Entry(janela)     # Campo para digitar o nome do aluno
entrada_nome.pack()
entrada_nota1 = tk.Entry(janela)    # Campo para digitar a primeira nota
entrada_nota1.pack()
entrada_nota2 = tk.Entry(janela)    # Campo para digitar a segunda nota
entrada_nota2.pack()

# Criação da tabela (Treeview) para exibir os dados dos alunos
tabela = ttk.Treeview(
    janela,
    columns=("Nome", "Nota1", "Nota2", "Média", "Situação"),
    show="headings"  # Mostra apenas os cabeçalhos das colunas
)

# Definição dos cabeçalhos da tabela
tabela.heading("Nome", text="Nome do Aluno")
tabela.heading("Nota1", text="Nota 1")
tabela.heading("Nota2", text="Nota 2")
tabela.heading("Média", text="Média")
tabela.heading("Situação", text="Situação")
tabela.pack()

# Adiciona uma barra de rolagem vertical à tabela
scrollbar = ttk.Scrollbar(janela, orient="vertical", command=tabela.yview)
tabela.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Lista inicial de alunos com suas notas
alunos_iniciais = [
    ("Alice", 8.5, 7.0),
    ("Bruno", 5.0, 6.0),
    ("Carlos", 3.5, 4.0),
    ("Daniela", 9.0, 9.5)
]

# Insere os alunos iniciais na tabela
for aluno in alunos_iniciais:
    nome, nota1, nota2 = aluno
    media = (nota1 + nota2) / 2
    # Define a situação do aluno com base na média
    situacao = "Aprovado" if media >= 7 else "Recuperação" if media >= 5 else "Reprovado"
    tabela.insert("", "end", values=(nome, nota1, nota2, f"{media:.2f}", situacao))

# Função para cadastrar um novo aluno
def cadastrar_aluno():
    nome = entrada_nome.get()              # Recupera o nome digitado
    nota1 = float(entrada_nota1.get())     # Recupera a primeira nota
    nota2 = float(entrada_nota2.get())     # Recupera a segunda nota
    media = (nota1 + nota2) / 2            # Calcula a média
    # Define a situação com base na média
    situacao = "Aprovado" if media >= 7 else "Recuperação" if media >= 5 else "Reprovado"

    # Insere os dados do novo aluno na tabela
    tabela.insert("", "end", values=(nome, nota1, nota2, f"{media:.2f}", situacao))

# Botão para cadastrar aluno
tk.Button(janela, text="Cadastrar", command=cadastrar_aluno).pack()

# Inicia o loop principal da interface gráfica
janela.mainloop()
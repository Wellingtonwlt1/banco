import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd

# Usuários e permissões
usuarios = {
    "wellington": {"senha": "5927", "tipo": "professor"},
    "aluno1": {"senha": "1234", "tipo": "aluno"},
    "aluno2": {"senha": "1234", "tipo": "aluno"},
}

# Janela principal (inicialmente oculta)
janela = tk.Tk()
janela.title("Sistema de cadastro de Alunos")
janela.geometry("820x600")
janela.withdraw()

colunas = ("Aluno", "Nota1", "Nota2", "Média", "Situação")
treeMedias = ttk.Treeview(janela, columns=colunas, show="headings")

for coluna in colunas:
    treeMedias.heading(coluna, text=coluna)
    treeMedias.column(coluna, width=100)

treeMedias.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

scrollbar = ttk.Scrollbar(janela, orient="vertical", command=treeMedias.yview)
treeMedias.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=4, column=3, sticky="ns")

# Labels e Entradas
lblNome = tk.Label(janela, text="Nome do Aluno:")
lblNota1 = tk.Label(janela, text="Nota 1")
lblNota2 = tk.Label(janela, text="Nota 2")

txtNome = tk.Entry(janela, bd=3)
txtNota1 = tk.Entry(janela)
txtNota2 = tk.Entry(janela)

lblNome.grid(row=0, column=0, padx=5, pady=5, sticky="w")
txtNome.grid(row=0, column=1, padx=5, pady=5)

lblNota1.grid(row=1, column=0, padx=5, pady=5, sticky="w")
txtNota1.grid(row=1, column=1, padx=5, pady=5)

lblNota2.grid(row=2, column=0, padx=5, pady=5, sticky="w")
txtNota2.grid(row=2, column=1, padx=5, pady=5)

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
    if tipo_usuario != "professor":
        messagebox.showwarning("Acesso Negado", "Somente professores podem adicionar alunos.")
        return
    
    try:
        nome = txtNome.get()
        nota1 = float(txtNota1.get())
        nota2 = float(txtNota2.get())

        media, situacao = verificar_situacao(nota1, nota2)

        treeMedias.insert("", "end", values=(nome, nota1, nota2, f"{media:.2f}", situacao))
        salvar_dados()
    except ValueError:
        messagebox.showerror("Erro", "Digite valores numéricos válidos.")
    finally:
        txtNome.delete(0, "end")
        txtNota1.delete(0, "end")
        txtNota2.delete(0, "end")

def excluir_aluno():
    if tipo_usuario != "professor":
        messagebox.showwarning("Acesso Negado", "Somente professores podem excluir registros.")
        return
    
    selected_item = treeMedias.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Nenhum aluno selecionado para exclusão.")
        return

    treeMedias.delete(selected_item)
    salvar_dados()

def editar_aluno():
    if tipo_usuario != "professor":
        messagebox.showwarning("Acesso Negado", "Somente professores podem editar registros.")
        return
    
    selected_item = treeMedias.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Nenhum aluno selecionado para edição.")
        return

    valores = treeMedias.item(selected_item)["values"]
    nome, nota1, nota2, media, situacao = valores

    # Solicita novas notas
    try:
        nova_nota1 = float(simpledialog.askstring("Editar Nota", f"Nova Nota 1 para {nome}:", initialvalue=nota1))
        nova_nota2 = float(simpledialog.askstring("Editar Nota", f"Nova Nota 2 para {nome}:", initialvalue=nota2))

        nova_media, nova_situacao = verificar_situacao(nova_nota1, nova_nota2)

        # Atualiza valores na tabela
        treeMedias.item(selected_item, values=(nome, nova_nota1, nova_nota2, f"{nova_media:.2f}", nova_situacao))
        salvar_dados()
    except (ValueError, TypeError):
        messagebox.showerror("Erro", "Digite valores numéricos válidos.")

def salvar_dados():
    dados = []
    for line in treeMedias.get_children():
        valores = treeMedias.item(line)["values"]
        dados.append(valores)

    df = pd.DataFrame(data=dados, columns=colunas)
    df.to_excel("planilhaAlunos.xlsx", index=False, engine="openpyxl")
    print("Dados salvos com sucesso.")

def carregar_dados(usuario, tipo_usuario_local):
    global tipo_usuario
    tipo_usuario = tipo_usuario_local
    try:
        df = pd.read_excel("planilhaAlunos.xlsx")
        for _, row in df.iterrows():
            treeMedias.insert("", "end", values=(row["Aluno"], row["Nota1"], row["Nota2"], row["Média"], row["Situação"]))
    except FileNotFoundError:
        print("Nenhum dado encontrado.")

    # Botões só aparecem para professor
    if tipo_usuario == "professor":
        btnCadastrar = tk.Button(janela, text="Cadastrar", command=cadastrar_aluno)
        btnCadastrar.grid(row=3, column=0, columnspan=2, pady=10)

        btnExcluir = tk.Button(janela, text="Excluir Aluno", command=excluir_aluno)
        btnExcluir.grid(row=5, column=0, columnspan=2, pady=10)

        btnEditar = tk.Button(janela, text="Editar Notas", command=editar_aluno)
        btnEditar.grid(row=6, column=0, columnspan=2, pady=10)

# Tela de login
def abrir_tela_login():
    login_win = tk.Toplevel()
    login_win.title("Login")
    login_win.geometry("300x200")

    tk.Label(login_win, text="Usuário:").pack()
    entry_usuario = tk.Entry(login_win)
    entry_usuario.pack()

    tk.Label(login_win, text="Senha:").pack()
    entry_senha = tk.Entry(login_win, show="*")
    entry_senha.pack()

    def validar_login():
        usuario = entry_usuario.get()
        senha = entry_senha.get()

        if usuario in usuarios and usuarios[usuario]["senha"] == senha:
            tipo_usuario_local = usuarios[usuario]["tipo"]
            login_win.destroy()
            iniciar_sistema(tipo_usuario_local, usuario)
        else:
            messagebox.showerror("Erro", "Credenciais inválidas!")

    tk.Button(login_win, text="Entrar", command=validar_login).pack()

def iniciar_sistema(tipo_usuario_local, usuario):
    janela.deiconify()
    carregar_dados(usuario, tipo_usuario_local)

# Inicia tela de login
abrir_tela_login()
janela.mainloop()
import tkinter as tk
from tkinter import ttk
from banco import BancoDados

class BibliotecaGUI:
    def __init__(self, root, bd):
        self.bd = bd
        self.root = root
        self.root.title("Gerenciador de Biblioteca")

        # Treeview
        self.tree = ttk.Treeview(root, columns=("ID", "Título", "Autor", "Ano", "Gênero"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Autor", text="Autor")
        self.tree.heading("Ano", text="Ano de Publicação")
        self.tree.heading("Gênero", text="Gênero")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Formulário de entrada
        form = tk.Frame(root)
        form.pack(pady=10)

        tk.Label(form, text="Título").grid(row=0, column=0)
        tk.Label(form, text="Autor").grid(row=1, column=0)
        tk.Label(form, text="Ano").grid(row=2, column=0)
        tk.Label(form, text="Gênero").grid(row=3, column=0)

        self.entry_titulo = tk.Entry(form)
        self.entry_autor = tk.Entry(form)
        self.entry_ano = tk.Entry(form)
        self.entry_genero = tk.Entry(form)

        self.entry_titulo.grid(row=0, column=1)
        self.entry_autor.grid(row=1, column=1)
        self.entry_ano.grid(row=2, column=1)
        self.entry_genero.grid(row=3, column=1)

        # Botões CRUD
        frame_botoes = tk.Frame(root)
        frame_botoes.pack(pady=10)

        btn_inserir = tk.Button(frame_botoes, text="Inserir Livro", command=self.inserir_livro)
        btn_inserir.pack(side=tk.LEFT, padx=5)

        btn_atualizar = tk.Button(frame_botoes, text="Atualizar Selecionado", command=self.atualizar_livro)
        btn_atualizar.pack(side=tk.LEFT, padx=5)

        btn_excluir = tk.Button(frame_botoes, text="Excluir Selecionado", command=self.excluir_livro)
        btn_excluir.pack(side=tk.LEFT, padx=5)

        self.carregar_dados()

    def carregar_dados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        registros = self.bd.selecionar_dados()
        for registro in registros:
            self.tree.insert("", "end", values=registro)

    def inserir_livro(self):
        titulo = self.entry_titulo.get()
        autor = self.entry_autor.get()
        ano = int(self.entry_ano.get())
        genero = self.entry_genero.get()
        self.bd.inserir_dados(titulo, autor, ano, genero)
        self.carregar_dados()

    def atualizar_livro(self):
        selecionado = self.tree.selection()
        if selecionado:
            item = self.tree.item(selecionado)
            id_livro = item["values"][0]
            titulo = self.entry_titulo.get()
            autor = self.entry_autor.get()
            ano = int(self.entry_ano.get())
            genero = self.entry_genero.get()
            self.bd.cursor.execute(
                "UPDATE livros SET titulo=%s, autor=%s, ano_publicacao=%s, genero=%s WHERE id=%s",
                (titulo, autor, ano, genero, id_livro)
            )
            self.bd.conexao.commit()
            self.carregar_dados()

    def excluir_livro(self):
        selecionado = self.tree.selection()
        if selecionado:
            item = self.tree.item(selecionado)
            id_livro = item["values"][0]
            self.bd.cursor.execute("DELETE FROM livros WHERE id=%s", (id_livro,))
            self.bd.conexao.commit()
            self.carregar_dados()


if __name__ == "__main__":
    root = tk.Tk()
    app_bd = BancoDados()
    app_gui = BibliotecaGUI(root, app_bd)
    root.mainloop()
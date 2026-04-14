# Importa a biblioteca tkinter para criar interfaces gráficas
import tkinter as tk
# Importa o módulo messagebox para exibir caixas de diálogo
from tkinter import messagebox

# Classe principal da aplicação
class SaborRapidoApp:
    def __init__(self, root):
        # Configurações da janela principal
        self.root = root
        self.root.title("Sabor Rápido - Protótipo")  # Título da janela
        self.root.geometry("400x500")                # Tamanho da janela

        # Dicionário com itens do menu e seus preços
        self.itens_menu = {"Hambúrguer": 10.00, "Batata Frita": 5.00, "Refrigerante": 3.00}
        # Lista que armazenará os itens escolhidos pelo cliente
        self.pedido = []

        # Label com instruções
        tk.Label(root, text="Selecione os itens do pedido:", font=("Arial", 12)).pack(pady=10)
        
        # Listbox para mostrar os itens do menu (permite múltiplas seleções)
        self.listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, font=("Arial", 10))
        self.atualizar_lista_menu()  # Preenche a listbox com os itens do menu
        self.listbox.pack()

    # Atualiza a listbox com os itens do menu
    def atualizar_lista_menu(self):
        self.listbox.delete(0, tk.END)  # Limpa a listbox
        for item in self.itens_menu.keys():
            self.listbox.insert(tk.END, item)  # Insere cada item do menu

        # Botões para adicionar ao pedido e visualizar pedido
        tk.Button(root, text="Adicionar ao Pedido", command=self.adicionar_pedido).pack(pady=5)
        tk.Button(root, text="Visualizar Pedido", command=self.visualizar_pedido).pack(pady=5)

    # Adiciona os itens selecionados ao pedido
    def adicionar_pedido(self):
        selecionados = self.listbox.curselection()  # Pega índices dos itens selecionados
        for index in selecionados:
            item = self.listbox.get(index)          # Recupera o nome do item
            self.pedido.append(item)                # Adiciona à lista de pedido
        messagebox.showinfo("Pedido", "Itens adicionados com sucesso!")  # Mensagem de confirmação

    # Exibe os itens do pedido atual
    def visualizar_pedido(self):
        if not self.pedido:  # Se não houver itens
            messagebox.showinfo("Pedido", "Nenhum item no pedido.")
            return
        pedido_texto = "\n".join(self.pedido)  # Junta os itens em texto
        messagebox.showinfo("Pedido Atual", f"Itens no pedido:\n{pedido_texto}")

        # Botão para finalizar pedido
        tk.Button(root, text="Finalizar Pedido", command=self.finalizar_pedido).pack(pady=10)

    # Finaliza o pedido e calcula o total
    def finalizar_pedido(self):
        if not self.pedido:  # Se não houver itens
            messagebox.showinfo("Pedido", "Adicione itens antes de finalizar o pedido.")
            return
        # Calcula o total somando os preços dos itens
        total = sum(self.itens_menu[item] for item in self.pedido)
        messagebox.showinfo("Total", f"Total do pedido: R$ {total:.2f}\nPedido finalizado!")
        self.pedido.clear()  # Limpa o pedido após finalizar

        # Campos para adicionar novos itens ao menu
        tk.Label(root, text="Adicionar Novo Item ao Menu:", font=("Arial", 12)).pack(pady=10)
        self.entry_item = tk.Entry(root, font=("Arial", 10))   # Campo para nome do item
        self.entry_item.pack()
        self.entry_preco = tk.Entry(root, font=("Arial", 10))  # Campo para preço do item
        self.entry_preco.pack()
        tk.Button(root, text="Adicionar Item", command=self.adicionar_item_menu).pack(pady=5)

    # Adiciona um novo item ao menu
    def adicionar_item_menu(self):
        item = self.entry_item.get().strip()   # Recupera nome do item
        preco = self.entry_preco.get().strip() # Recupera preço do item
        if item and preco:  # Verifica se os campos foram preenchidos
            try:
                self.itens_menu[item] = float(preco)  # Converte preço para número e adiciona ao menu
                self.atualizar_lista_menu()           # Atualiza a listbox
                self.entry_item.delete(0, tk.END)     # Limpa campo de nome
                self.entry_preco.delete(0, tk.END)    # Limpa campo de preço
                messagebox.showinfo("Sucesso", "Item adicionado ao menu com sucesso!")
            except ValueError:
                messagebox.showerror("Erro", "Preço inválido. Digite um valor numérico.")
        else:
            messagebox.showerror("Erro", "Preencha ambos os campos corretamente.")

# Ponto de entrada do programa
if __name__ == "__main__":
    root = tk.Tk()              # Cria a janela principal
    app = SaborRapidoApp(root)  # Instancia a aplicação
    root.mainloop()             # Inicia o loop da interface gráfica
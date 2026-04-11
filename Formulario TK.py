import tkinter as tk
from tkinter import messagebox

def submit():
    # Recupera os dados dos campos de entrada
    nome = nome_entry.get()
    email = email_entry.get()

    # Verifica qual radiobutton está selecionado
    linguagem_preferida = linguagem_var.get()

    # Imprime os dados no console
    print("Nome:", nome)
    print("Email:", email)
    print("Linguagem Preferida:", linguagem_preferida)

    # Exibe uma mensagem de confirmação
    messagebox.showinfo("Dados enviados", 
                        f"Nome: {nome}\nEmail: {email}\nLinguagem: {linguagem_preferida}")

# Cria a janela principal
root = tk.Tk()
root.title("Formulário de Inscrição")

# Cria um frame para conter os widgets
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Campo de entrada para "Nome"
tk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="e")
nome_entry = tk.Entry(frame)
nome_entry.grid(row=0, column=1)

# Campo de entrada para "Email"
tk.Label(frame, text="Email:").grid(row=1, column=0, sticky="e")
email_entry = tk.Entry(frame)
email_entry.grid(row=1, column=1)

# Radiobuttons para linguagem preferida
tk.Label(frame, text="Linguagem Preferida:").grid(row=2, column=0, sticky="e")
linguagem_var = tk.StringVar(value="Python")  # valor padrão

tk.Radiobutton(frame, text="Python", variable=linguagem_var, value="Python").grid(row=2, column=1, sticky="w")
tk.Radiobutton(frame, text="Java", variable=linguagem_var, value="Java").grid(row=3, column=1, sticky="w")
tk.Radiobutton(frame, text="C++", variable=linguagem_var, value="C++").grid(row=4, column=1, sticky="w")

# Botão de envio
submit_button = tk.Button(frame, text="Enviar", command=submit)
submit_button.grid(row=5, columnspan=2, pady=10)

# Inicia o loop principal da interface
root.mainloop()
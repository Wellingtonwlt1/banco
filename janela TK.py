import tkinter as tk

def submit():
    # Recupera os dados dos campos de entrada
    nome = nome_entry.get()
    email = email_entry.get()

    # Imprime os dados no console
    print("Nome:", nome)
    print("Email:", email)

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

# Botão de envio
submit_button = tk.Button(frame, text="Enviar", command=submit)
submit_button.grid(row=2, columnspan=2, pady=10)

# Inicia o loop principal da interface
root.mainloop()
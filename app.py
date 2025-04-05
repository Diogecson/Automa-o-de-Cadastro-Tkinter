import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import webbrowser
import os

# Função para cadastrar os dados
def cadastrar():
    nome = entry_nome.get()
    email = entry_email.get()
    senha = entry_senha.get()
    responsavel = "Soares"  # Nome do responsável pelo cadastro
    
    if nome and email and senha:
        # Salvar os dados no arquivo de cadastro
        with open("cadastros.txt", "a") as arquivo:
            arquivo.write(f"Responsável: {responsavel}, Nome: {nome}, E-mail: {email}, Senha: {senha}\n")
        
        # Limpar os campos de entrada
        entry_nome.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_senha.delete(0, tk.END)

        # Fechar a janela de visualização, se estiver aberta
        if janela_visualizar.winfo_exists():
            janela_visualizar.destroy()

        # Atualizar a página HTML com os dados mais recentes
        atualizar_dashboard()

        # Abrir a página HTML com os dados cadastrados
        abrir_dashboard()

        messagebox.showinfo("Cadastro", f"Cadastro realizado com sucesso!\nResponsável: {responsavel}\nNome: {nome}\nE-mail: {email}")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

# Função para atualizar a página HTML com os dados mais recentes
def atualizar_dashboard():
    # Lê os dados de cadastro
    try:
        with open("cadastros.txt", "r") as arquivo:
            dados = arquivo.readlines()
        
        # Contar o número de cadastros (nomes)
        numero_de_cadastros = len(dados)
        
        # Criar o conteúdo HTML
        html_conteudo = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Dashboard de Dados Cadastrados</title>
          <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 0; }}
            .container {{ width: 80%; margin: 0 auto; padding: 20px; }}
            h1 {{ text-align: center; color: #333; }}
            .card {{ background-color: white; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); padding: 15px; margin: 15px; border-radius: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f4f4f9; }}
            .table-container {{
              max-height: 400px;  /* Altura máxima do contêiner */
              overflow-y: auto;   /* Ativa a rolagem vertical */
            }}
          </style>
        </head>
        <body>
          <div class="container">
            <h1>Dashboard de Dados Cadastrados</h1>
            <div class="card">
              <h3>Lista de Cadastros</h3>
              <p>Total de cadastros: <strong>{numero_de_cadastros}</strong></p>  <!-- Exibe a quantidade de cadastros -->
              <div class="table-container">
                <table id="tabela-dados">
                  <thead>
                    <tr>
                      <th>Responsável</th>
                      <th>Nome</th>
                      <th>E-mail</th>
                      <th>Senha</th>
                    </tr>
                  </thead>
                  <tbody>
        """
        
        # Adiciona cada cadastro na tabela HTML
        for linha in dados:
            dados_cadastro = linha.strip().split(', ')
            responsavel = dados_cadastro[0].split(': ')[1]
            nome = dados_cadastro[1].split(': ')[1]
            email = dados_cadastro[2].split(': ')[1]
            senha = dados_cadastro[3].split(': ')[1]
            
            html_conteudo += f"""
            <tr>
                <td>{responsavel}</td>
                <td>{nome}</td>
                <td>{email}</td>
                <td>{senha}</td>
            </tr>
            """
        
        # Finaliza o conteúdo HTML
        html_conteudo += """
                </tbody>
              </table>
            </div>
          </div>
        </body>
        </html>
        """
        
        # Salva o conteúdo HTML em um arquivo
        with open("index.html", "w") as f:
            f.write(html_conteudo)
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar o dashboard: {e}")

# Função para abrir o dashboard HTML no navegador
def abrir_dashboard():
    # Caminho para o arquivo HTML (ajuste o caminho conforme necessário)
    caminho_html = "file://" + os.path.abspath("index.html")
    webbrowser.open(caminho_html)

# Função para visualizar os dados salvos
def visualizar_dados():
    global janela_visualizar
    # Criar nova janela
    janela_visualizar = tk.Toplevel()
    janela_visualizar.title("Dados Cadastrados")
    
    # Definir o tamanho da janela
    janela_visualizar.geometry("400x300")
    
    # Abrir o arquivo e ler os dados
    try:
        with open("cadastros.txt", "r") as arquivo:
            dados = arquivo.readlines()
        
        # Criar um widget Text para exibir os dados
        texto = tk.Text(janela_visualizar, width=50, height=15, wrap=tk.WORD, font=("Arial", 10))
        texto.pack(pady=10)
        
        # Inserir os dados lidos no widget Text
        if dados:
            texto.insert(tk.END, "".join(dados))
        else:
            texto.insert(tk.END, "Nenhum dado cadastrado ainda.")
        
        # Tornar o widget de texto somente leitura
        texto.config(state=tk.DISABLED)

    except FileNotFoundError:
        texto.insert(tk.END, "Nenhum dado cadastrado ainda.")
        texto.config(state=tk.DISABLED)

# Função para deletar os cadastros
def deletar_cadastros():
    try:
        # Abrir o arquivo e limpar seu conteúdo
        open("cadastros.txt", "w").close()
        messagebox.showinfo("Deletar", "Todos os cadastros foram deletados com sucesso.")
        
        # Fechar a janela de visualização, se estiver aberta
        if janela_visualizar.winfo_exists():
            janela_visualizar.destroy()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao deletar os cadastros: {e}")

# Função para limpar os campos de entrada
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_senha.delete(0, tk.END)

# Função para abrir uma janela de seleção de dados e apagar um cadastro específico
def limpar_individual():
    # Criar uma janela para visualizar os dados e selecionar um cadastro
    janela_limpar_individual = tk.Toplevel()
    janela_limpar_individual.title("Selecionar Cadastro para Remover")
    janela_limpar_individual.geometry("400x300")
    
    # Abrir o arquivo e ler os dados
    try:
        with open("cadastros.txt", "r") as arquivo:
            dados = arquivo.readlines()

        if not dados:
            messagebox.showinfo("Erro", "Nenhum dado cadastrado para remover.")
            return
        
        # Criar uma Listbox para exibir os dados
        listbox = tk.Listbox(janela_limpar_individual, width=50, height=15, font=("Arial", 10))
        listbox.pack(pady=10)

        # Adicionar os dados na Listbox
        for i, linha in enumerate(dados):
            listbox.insert(tk.END, linha.strip())
        
        # Função para remover o cadastro selecionado
        def remover_selecionado():
            selecionado = listbox.curselection()
            if selecionado:
                linha_selecionada = dados[selecionado[0]]
                
                # Remover o cadastro da lista
                dados.pop(selecionado[0])
                
                # Reescrever o arquivo sem o cadastro excluído
                with open("cadastros.txt", "w") as arquivo:
                    arquivo.writelines(dados)
                
                messagebox.showinfo("Sucesso", f"Cadastro removido: {linha_selecionada}")
                janela_limpar_individual.destroy()
                visualizar_dados()  # Reabrir a janela com os dados atualizados
            else:
                messagebox.showerror("Erro", "Selecione um cadastro para remover.")
        
        # Botão para remover o cadastro selecionado
        botao_remover = ttk.Button(janela_limpar_individual, text="Remover Selecionado", command=remover_selecionado)
        botao_remover.pack(pady=10)

    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo de cadastros não encontrado.")

# Criar a janela principal
janela = tk.Tk()
janela.title("Cadastro de Usuário")

# Definir o tamanho da janela
janela.geometry("350x400")
janela.config(bg="#f4f4f9")  # Cor de fundo mais suave

# Criar o frame para organizar os widgets
frame = tk.Frame(janela, bg="#f4f4f9")
frame.pack(pady=20)

# Títulos e campos de entrada
label_nome = tk.Label(frame, text="Nome:", font=("Arial", 12), bg="#f4f4f9")
label_nome.pack(pady=5)

entry_nome = ttk.Entry(frame, font=("Arial", 12))
entry_nome.pack(pady=5)

label_email = tk.Label(frame, text="E-mail:", font=("Arial", 12), bg="#f4f4f9")
label_email.pack(pady=5)

entry_email = ttk.Entry(frame, font=("Arial", 12))
entry_email.pack(pady=5)

label_senha = tk.Label(frame, text="Senha:", font=("Arial", 12), bg="#f4f4f9")
label_senha.pack(pady=5)

entry_senha = ttk.Entry(frame, font=("Arial", 12), show="*")  # A senha será exibida como asteriscos
entry_senha.pack(pady=5)

# Botões com estilo moderno
botao_cadastrar = ttk.Button(janela, text="Cadastrar", command=cadastrar)
botao_cadastrar.pack(pady=10)

botao_visualizar = ttk.Button(janela, text="Visualizar Dados", command=visualizar_dados)
botao_visualizar.pack(pady=10)

botao_deletar = ttk.Button(janela, text="Deletar Todos os Cadastros", command=deletar_cadastros)
botao_deletar.pack(pady=10)

botao_limpar = ttk.Button(janela, text="Limpar Campos", command=limpar_campos)
botao_limpar.pack(pady=10)

botao_limpar_individual = ttk.Button(janela, text="Limpar Cadastro Individual", command=limpar_individual)
botao_limpar_individual.pack(pady=10)

# Garantir que a janela fique sempre na frente
janela.attributes("-topmost", 1)

# Desabilitar a minimização da janela
janela.resizable(False, False)

# Função para garantir que a janela permaneça aberta mesmo clicando fora
def on_focus_out(event):
    janela.lift()

# Configurar evento para manter a janela no topo
janela.bind("<FocusOut>", on_focus_out)

# Iniciar a aplicação
janela.mainloop()

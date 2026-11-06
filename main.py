
from datetime import datetime
import os
from time import sleep


#---pedro|pedro@gmail.com|password|banco|observacao|11-07-2026:7:00pm REGRA DE NEGOCIO DE ORGANIZACAO--------


categoria = {
    "banco": 3,
    "trabalho": 2,
    "redes sociais": 2,
    "estudos": 3 ,
    "outros": 1
}

def limpar_terminal():
    # 'nt' significa Windows, caso contrário é Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')
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
        print("7 - Sair")
        print("-" * 30)
        opcao = input("Escolha uma opção: ")
        if opcao in ["1", "2", "3", "4", "5", "6", "7"]:
            return opcao
        else:
            print("Opção inválida. Tente novamente.")



#-------------CRUD---------#


# Adicionar
def adicionar_credencial():
    limpar_terminal()
    print("Adicionar credencial")
    nome_credencial = input("Digite o nome do serviço: ")
    usuario_email_credencial = input("Digite o usuário ou e-mail: ")
    # Mostra as categorias existentes e a força mínima de cada uma
    print("-" *15)
    consultar_categorias()
    print("-" *15)

    categoria_credencial = input("Digite a categoria: ").lower()
    if categoria_credencial not in categoria:
        print("Categoria não existe. Deseja cadastrar essa nova categoria? (s/n)")
        if input().lower() == "s":
            cadastrar_categoria(categoria_credencial)
        else:
            categoria_credencial = "outros"
            print("A credencial foi colocada em 'outros'.")

    minimo = categoria[categoria_credencial]
    senha_credencial = input("Digite a senha: ")


    while True:
        forca_senha = analise_forca_senha(senha_credencial)
       
        if forca_senha in [1,2,3]:
            
            if forca_senha >= categoria[categoria_credencial]:
                print(f"Senha aceita,nivel:{forca_senha}")
                break
            
            else:
                print(f"A senha não atende a força mínima exigida para a categoria '{categoria_credencial}'.")
                senha_credencial = input("Digite uma nova senha: ")


    observacoes_credencial = input("Digite observações (opcional): ")
    data_cadastro =datetime.now() # Data do cadastro no formato dd/mm/aaaa 
    lista = [nome_credencial, usuario_email_credencial, senha_credencial, categoria_credencial, observacoes_credencial, data_cadastro]
    
    #ADICIONARF AO TXT
    #---pedro|pedro@gmail.com|password|banco|observacao|11-07-2026:7:00pm REGRA DE NEGOCIO DE ORGANIZACAO--------
    # abrir e adicionar credenciais
    with open("credenciais.txt", "a", encoding="utf-8") as file:
        for i in lista:
            file.write(str(i))
            file.write("|")
            
        file.write("\n")



    
def ler_credenciais():
    limpar_terminal()
    with open("credenciais.txt", "r", encoding="utf-8") as file:
            for linha in file:
                linha = linha.strip().split("|")
                print("-" * 30)
                if len(linha) == 0:
                    print("Nenhuma credencial cadastrada.")
                    return
                print("Credenciais:")
                print("-" * 30)
                print(f"Nome do serviço: {linha[0]}")
                print(f"Usuário ou e-mail: {linha[1]}")
                print(f"Senha: {linha[2][:2]}{'*' * (len(linha[2]) - 2)}")  # Mostra apenas os dois primeiros caracteres da senha
                print(f"Categoria: {linha[3]}")
                print(f"Observações: {linha[4]}")
                print(f"Data do último cadastro ou alteração: {linha[5]}")
                print("-" * 30)
    input_saida = input("Pressione Enter para continuar...")  




                
def atualizar_credencial():
    limpar_terminal()
    print("Atualizar credencial")
    print("-" * 30)
    print("Serviços cadastrados:")
    with open("credenciais.txt", "r", encoding="utf-8") as file:
        for linha in file:
            linha = linha.split("|")
            print(f"- {linha[0]}")
    nome_credencial = input("Digite o nome do serviço que deseja atualizar: ")
    with open("credenciais.txt", "r", encoding="utf-8") as file:
            
            for linha in file:
                linha = linha.split("|")


                if nome_credencial == linha[0]:
                    linha_antiga = linha.copy()  # Copia a linha antiga para comparação posterior
                    print("[1] Nome")
                    print("[2] Usuário")
                    print("[3] Senha")
                    print("[4] Categoria")
                    print("[5] Observações")
                    credencial = input("Digite o campo que deseja atualizar: ").lower()

                    if credencial == "1":
                        nova_credencial = input("Digite o novo nome do serviço: ")
                        linha[0] = nova_credencial
                        

                    elif credencial == "2":
                        novo_usuario = input("Digite o novo usuário ou e-mail: ")
                        linha[1] = novo_usuario

                    elif credencial == "3":
                        nova_senha = input("Digite a nova senha: ")
                        while True:
                                forca_senha = analise_forca_senha(nova_senha)
                               
                                if forca_senha in [1,2,3]:
                                    
                                    if forca_senha >= categoria[linha[3]]:
                                        print(f"Senha aceita,nivel:{forca_senha}")
                                        break
                                    
                                    else:
                                        print(f"A senha não atende a força mínima exigida para a categoria '{linha[3]}'.")
                                        senha_credencial = input("Digite uma nova senha: ")
                        linha[2] = nova_senha

                    elif credencial == "4":
                        nova_categoria = input("Digite a nova categoria: ").lower()

                        if nova_categoria not in categoria:
                            print("Categoria não existe. Deseja cadastrar essa nova categoria? (s/n)")

                            if input().lower() == "s":
                                cadastrar_categoria(nova_categoria)

                            else:
                                nova_categoria = "outros"
                                print("A credencial foi colocada em 'outros'.")

                        linha[3] = nova_categoria
                    elif credencial == "5":
                        novas_observacoes = input("Digite as novas observações: ")
                        linha[4] = novas_observacoes

                    data_cadastro =datetime.now()
                    linha[5] = str(data_cadastro)
                
                    print("Credencial atualizada com sucesso!")
                  
                    with open("credenciais.txt", "r", encoding="utf-8") as file:#ler todas as linhas do arquivo e guarda numna lista
                        linhas = file.readlines()

                    with open("credenciais.txt", "w", encoding="utf-8") as file:
                        for l in linhas:# vai passar por todas as linhas do arquivo e vai escrever no arquivo novamente, mas se a linha for a que foi atualizada, ele escreve a nova linha
                            
                            if l.strip() != "|".join(linha_antiga).strip():#se NAO FOR A LINHA antiga,ele escreve a linha do arquivo
                                file.write(l)
                            else:#SE FOR A LINHA DO ARQUIVO, ELE ESCREVE A LINHA ATUALIZADA
                                file.write("|".join(linha) )
                            
                    


        




def consultar_categorias():
    limpar_terminal()
    for i in categoria:
        print(f"Categoria: {i}, Força mínima: {categoria[i]}")

    input_saida = input("Pressione Enter para continuar...")  



def cadastrar_categoria(categoria_nova):
    
    #perguntar_forca_minima
    forca_minima = input("Digite a força mínima para a nova categoria(senha Fraca, senha Média, senha Forte): ").lower()
    if forca_minima == "senha fraca":
        forca_minima = 1
    if forca_minima == "senha média":
        forca_minima = 2
    if forca_minima == "senha forte":
        forca_minima = 3
    categoria[categoria_nova] = forca_minima


#---------------------------#



def analise_forca_senha(senha):
    status_maisculo = False
    status_minus = False
    tamanho = False
    num = False
    caracter = False

    lista = ["!", '@', "#", '$', '%', "&", "*", "-", "_", "?", "/","+","="]

    if len(senha) >=6:
        tamanho = True

    for i in range(len(senha)):
        if senha[i].isdigit() == False:
            if senha[i]==senha[i].upper():
                status_maisculo = True

    for i in range(len(senha)):
        if senha[i].isdigit() == False:
            if senha[i]==senha[i].lower():
                status_minus = True


    for i in lista:
        if i in senha:
            caracter = True
        
    for i in senha:
         if i.isdigit() == True:
              num = True

    if status_maisculo != False and status_minus != False and tamanho != False and num != False and caracter != False:
            return 3
    
    if tamanho!= False and status_minus != False  and num != False and status_maisculo != False:
            return 2
    
    if tamanho!= False :
        if num != False or status_minus != False:
            return 1
        
    
    
    

    
#-----------------------------#


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Detecção de riscos

def risk_detection(senhas):
        lista_repetida = []
        lista = []
        for posicao, senha in enumerate(senhas):
                if senha in senhas:
                        if senha not in lista:
                               lista.append(posicao)
                               lista.append(senha)
                        else:
                               x = lista.index(senha)
                               lista_repetida.append(lista[x-1])
                               lista_repetida.append(lista[x])
                               lista_repetida.append(posicao)
                               lista_repetida.append(senha)
        return lista_repetida



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def excluir_credencial():
    print("-" * 30)
    print("Serviços cadastrados:")
    with open("credenciais.txt", "r", encoding="utf-8") as file:
        linhas = file.readlines()
        nome = []
        for linha in linhas:
            linha = linha.split("|")
            nome.append(linha[0].lower())
            print(f"- {linha[0]}")
    nome_credencial = input("Digite o nome do serviço que deseja excluir: ").lower()
    if nome_credencial not in nome:
         print("Serviço não encontrado!")
         sleep(2)

    else:
         confirmacao = input("Você tem certeza que deseja excluir ? [s/n]").lower()
         if confirmacao == "s":
            with open("credenciais.txt", "w", encoding="utf-8") as file:
                for linha in linhas:
                    if linha.strip().split("|")[0].lower() != nome_credencial:
                         file.write(linha)
                    else:
                        print(f"Credencial '{nome_credencial}' excluída com sucesso!")
                        sleep(2)
         else:
            print("Exclusão cancelada!")
            sleep(2)



while True:
    opcao = menu()
    if opcao == "7":
        break
    elif opcao == "1":
        adicionar_credencial()
    elif opcao == "2":
        ler_credenciais()
    elif opcao == "6":
        excluir_credencial()
    elif opcao == "3":
        atualizar_credencial()
    elif opcao == "4":  
        consultar_categorias()
    elif opcao == "5":
        limpar_terminal()
        cadastrar_categoria(input("Digite o nome da nova categoria: ").lower())
    limpar_terminal()
    print("-"*30)
    lista = []
    with open("credenciais.txt", "r", encoding="utf-8") as file:
                for linha in file:
                    linha = linha.strip().split("|")
                    lista.append(linha[2])
                    
    senha_repetida = risk_detection(lista)
    if senha_repetida == 0:
        print("Não há senha repetida.")
    else:
        print(f"Há {int(len(senha_repetida))//2} senhas repetidas.")
    print("-"*30)

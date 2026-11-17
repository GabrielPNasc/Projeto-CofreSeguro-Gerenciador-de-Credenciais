from datetime import datetime
import os
from time import sleep
from agente import falar_com_agente
from login import *
from seguranca import *

#-------------CRUD---------#


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


# Adicionar
def adicionar_credencial(usuario):
    limpar_terminal()
    print("Adicionar credencial")
    nome_credencial = input("Digite o nome do serviço: ")
    usuario_email_credencial = input("Digite o usuário ou e-mail: ")
    # Mostra as categorias existentes e a força mínima de cada uma
    print("-" *15)
    consultar_categorias()
    print("-" *15)

    while True:
        categoria_credencial = int(input("Digite a categoria: "))
        try:
            for i in range(len(categoria)):
                if categoria_credencial == i + 1:
                    categoria_credencial = list(categoria.keys())[i]
                    break
        except ValueError:
            print("Categoria inválida. Digite um número válido.")
        break

    minimo = categoria[categoria_credencial]
    answer = int(input("[1]-Gerar senha Forte Automaticamente\n[2]-Criar senha manualmente\nEscolha uma opção: "))
    if answer == 1:
        senha_credencial = create_password()
        print(f"Sua senha gerada é: {senha_credencial}")
        input("Pressione Enter para continuar...")
    else:
        senha_credencial = input("Digite a senha: ")
        ## Se a senha já estiver cadastrada no credenciais.txt do usuário que está usando, avisar.
        if os.path.exists(arquivo_user(usuario)):
            with open(arquivo_user(usuario), "r", encoding="utf-8") as file:
                for linha_existente in file:
                    if senha_credencial in descriptografar(linha_existente):
                        print("ATENÇÃO: Essa senha já está cadastrada.")


    while True:
        forca_senha = analise_forca_senha(senha_credencial)
       
        if forca_senha in [1,2,3]:
            
            if forca_senha >= categoria[categoria_credencial]:
                print(f"Senha aceita,nivel:{forca_senha}")
                explicar_forca_senha(senha_credencial)
                break
            
            else:
                print(f"A senha não atende a força mínima exigida para a categoria '{categoria_credencial}'.")
                senha_credencial = input("Digite uma nova senha: ")


    observacoes_credencial = input("Digite observações (opcional): ")
    data_cadastro =datetime.now() # Data do cadastro no formato dd/mm/aaaa 
    senha_credencial = criptografar(senha_credencial)  # Criptografa a senha antes de salvar
    lista = [nome_credencial, usuario_email_credencial, senha_credencial, categoria_credencial, observacoes_credencial, data_cadastro]
    
    #ADICIONARF AO TXT
    #---pedro|pedro@gmail.com|password|banco|observacao|11-07-2026:7:00pm REGRA DE NEGOCIO DE ORGANIZACAO--------
    # abrir e adicionar credenciais
    with open(arquivo_user(usuario), "a", encoding="utf-8") as file:
        for i in lista:
            file.write(str(i))
            file.write("|")
            
        file.write("\n")
    return True

# Opção de revelar senha para o usuário
def revelar_senha(usuario, senha):
    while True:
        resposta = input("Deseja revelar a senha completa? (s/n): ").lower()
        # Usuario deverá confirmar senha inicial (do cadastro) para revelar a senha completa
        senha_confirmacao = input("Digite a senha do seu cadastro inicial para confirmar: ")
        with open(ARQ_USUARIOS, "r", encoding="utf-8") as file:
            for linha in file:
                linha = linha.strip().split("|")
                if usuario == linha[0]:
                    if senha_confirmacao == descriptografar(linha[1]):
                        if resposta == "s":
                            print(f"A senha completa é: {descriptografar(senha)}")
                            return True
                        elif resposta == "n":
                            print("Senha não revelada.")
                            return False
                        else:
                            print("Opção inválida. Digite 's' para sim ou 'n' para não.")
                    else:
                        print("Senha de confirmação incorreta. Tente novamente.")
                        return False
                     

    
def ler_credenciais(usuario):
    limpar_terminal()
    try:
        with open(arquivo_user(usuario), "r", encoding="utf-8") as file:
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
                    print(f"Senha: {descriptografar(linha[2])[:2]}{'*' * (len(descriptografar(linha[2])) - 2)}")  # Mostra apenas os dois primeiros caracteres da senha
                    print(f"Categoria: {linha[3]}")
                    print(f"Observações: {linha[4]}")
                    print(f"Data do último cadastro ou alteração: {linha[5]}")
                    print("-" * 30)
                    revelar_senha(usuario, linha[2])  
        input_saida = input("Pressione Enter para continuar...")  
    except FileNotFoundError:
            print("Arquivo de credenciais não encontrado. Cadastre uma credencial primeiro.")
            input("Pressione Enter para continuar...")
            return False
    

def register_log(acao):
    with open("log.txt", "a", encoding="utf-8") as file:
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        file.write(f"{acao} - {data_hora}\n")

                
def atualizar_credencial(usuario):
    try:
        limpar_terminal()
        print("Atualizar credencial")
        print("-" * 30)
        print("Serviços cadastrados:")
        with open(arquivo_user(usuario), "r", encoding="utf-8") as file:
            for linha in file:
                linha = linha.split("|")
                print(f"- {linha[0]}")
        nome_credencial = input("Digite o nome do serviço que deseja atualizar: ")
        with open(arquivo_user(usuario), "r", encoding="utf-8") as file:
                
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
                            answer = int(input("[1]-Gerar senha Forte Automaticamente\n[2]-Criar senha manualmente\nEscolha uma opção: "))
                            if answer == 1:
                                nova_senha = create_password()
                                print(f"Sua senha gerada é: {nova_senha}")
                                input("Pressione Enter para continuar...")
                            else:
                                nova_senha = input("Digite a senha: ")
                                ## Se a senha já estiver cadastrada no credenciais.txt, avisar.
                                if os.path.exists(arquivo_user(usuario)):
                                    with open(arquivo_user(usuario), "r", encoding="utf-8") as file:
                                        for linha_existente in file:
                                            if nova_senha in linha_existente:
                                                print("ATENÇÃO: Essa senha já está cadastrada.")
                                explicar_forca_senha(nova_senha)
                            while True:
                                    forca_senha = analise_forca_senha(nova_senha)
                                
                                    if forca_senha in [1,2,3]:
                                        
                                        if forca_senha >= categoria[linha[3]]:
                                            print(f"Senha aceita,nivel:{forca_senha}")
                                            break
                                        
                                        else:
                                            print(f"A senha não atende a força mínima exigida para a categoria '{linha[3]}'.")
                                            nova_senha = input("Digite uma nova senha: ")
                                    else:
                                        print("Senha inválida. Tente novamente.")
                                        nova_senha = input("Digite a senha: ")
                            if input("Tem certeza do que Deseja? (s/n): ").lower() == "s":
                                linha[2] = criptografar(nova_senha)
                            else:
                                print("Atualização de senha cancelada.")
                                return  False
                        

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
                    
                        with open(arquivo_user(usuario), "r", encoding="utf-8") as file:#ler todas as linhas do arquivo e guarda numna lista
                            linhas = file.readlines()

                        with open(arquivo_user(usuario), "w", encoding="utf-8") as file:
                            for l in linhas:# vai passar por todas as linhas do arquivo e vai escrever no arquivo novamente, mas se a linha for a que foi atualizada, ele escreve a nova linha
                                
                                if l.strip() != "|".join(linha_antiga).strip():#se NAO FOR A LINHA antiga,ele escreve a linha do arquivo
                                    file.write(l)
                                else:#SE FOR A LINHA DO ARQUIVO, ELE ESCREVE A LINHA ATUALIZADA
                                    file.write("|".join(linha) )
        return True
    except FileNotFoundError:
        print("Arquivo de credenciais não encontrado. Cadastre uma credencial primeiro.")
        input("Pressione Enter para continuar...")
        return False
                    



def consultar_categorias():
    limpar_terminal()
    for i in range(len(categoria)):
        print(f"[{i + 1}]-Categoria: {list(categoria.keys())[i]}, Força mínima: {categoria[list(categoria.keys())[i]]}")
    input_saida = input("Após pressionar Enter, digite o número da categoria.")  



def cadastrar_categoria(categoria_nova):
    
    #perguntar_forca_minima
    forca_minima = int(input("Digite a força mínima para a nova categoria(senha Fraca[1], senha Média[2], senha Forte[3]): "))
    if forca_minima == 1:
        forca_minima = 1
    if forca_minima == 2:
        forca_minima = 2
    if forca_minima == 3:
        forca_minima = 3
    categoria[categoria_nova] = forca_minima

    return True


#---------------------------#




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
def excluir_credencial(usuario):
    try:
        print("-" * 30)
        print("Serviços cadastrados:")
        with open(arquivo_user(usuario), "r", encoding="utf-8") as file:
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
                with open(arquivo_user(usuario), "w", encoding="utf-8") as file:
                    for linha in linhas:
                        if linha.strip().split("|")[0].lower() != nome_credencial:
                            file.write(linha)
                        else:
                            print(f"Credencial '{nome_credencial}' excluída com sucesso!")
                            sleep(2)
                            return True
            else:
                print("Exclusão cancelada!")
                sleep(2)
                return False
    except FileNotFoundError:
                print("Arquivo de credenciais não encontrado. Cadastre uma credencial primeiro.")
                input("Pressione Enter para continuar...")
                return False




def agente(usuario):
    arquivo, sistema = arquivo_user(usuario), "Sistema de Gerenciamento de Credenciais"
    print(f"\nUsando {arquivo} no sistema {sistema}. Digite 'sair' para encerrar.")
     
    while True:
        pergunta = input("\nPergunta > ").strip()
        if pergunta.lower() == "sair":
            break
    falar_com_agente(arquivo, pergunta, sistema)
    return True





def senhas_repetidas(usuario):
    limpar_terminal()
    print("-"*30)
    lista = []
    with open(arquivo_user(usuario), "r", encoding="utf-8") as file:
                    for linha in file:
                        linha = linha.strip().split("|")
                        lista.append(descriptografar(linha[2]))
                        
    senha_repetida = risk_detection(lista)
    if senha_repetida == 0:
        print("Não há senha repetida.")
    else:
        print(f"Há {int(len(senha_repetida))//2} senhas repetidas.")
    print("-"*30)
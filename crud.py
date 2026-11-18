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

def servicos_com_senha(usuario, senha):
    servicos = []
    if not os.path.exists(arquivo_user(usuario)):
        return servicos
    with open(arquivo_user(usuario), "r", encoding="utf-8") as file:
        for linha in file:
            linha = linha.strip().split("|")
            if len(linha) < 3:
                continue
            if descriptografar(linha[2]) == senha:
                servicos.append(linha[0])
    return servicos

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
        repetidos = servicos_com_senha(usuario, senha_credencial)
        if len(repetidos) > 0:
            print(f"ATENÇÃO: Essa senha já é usada em: {', '.join(repetidos)}")


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
def revelar_senha(usuario, senha, servico):
    while True:
        resposta = input("Deseja revelar a senha completa? (s/n): ").lower()
        if resposta == "n":
            print("Senha não revelada.")
            return False
        if resposta == "s":
            break
        print("Opção inválida. Digite 's' para sim ou 'n' para não.")

    senha_confirmacao = input("Digite a senha do seu cadastro inicial para confirmar: ")
    with open(ARQ_USUARIOS, "r", encoding="utf-8") as file:
        for linha in file:
            linha = linha.strip().split("|")
            if usuario == linha[0]:
                if senha_confirmacao == descriptografar(linha[1]):
                    print(f"A senha completa é: {descriptografar(senha)}")
                    register_log(f"Senha revelada (serviço: {servico})", usuario)
                    return True
                else:
                    print("Senha de confirmação incorreta.")
                    register_log(f"Tentativa falha de revelar senha (serviço: {servico})", usuario)
                    return False
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
                    revelar_senha(usuario, linha[2], linha[0]) 
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
        nome_credencial = input("Digite o nome do serviço que deseja atualizar: ").lower()
        with open(arquivo_user(usuario), "r", encoding="utf-8") as file:
                
                for linha in file:
                    linha = linha.split("|")


                    if nome_credencial == linha[0].lower():
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
                                repetidos = servicos_com_senha(usuario, nova_senha)
                                if len(repetidos) > 0:
                                    print(f"ATENÇÃO: Essa senha já é usada em: {', '.join(repetidos)}")
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



# Além de detectar senhas repetidas, tem que avisar ao usuário quais os serviços têm senhas repetidas. Por exemplo, se o usuário cadastrou a mesma senha para o serviço "Facebook" e "Instagram", o sistema deve alertar que essas duas credenciais têm a mesma senha.

SENHAS_COMUNS = [
    "123456", "12345678", "123456789", "password", "senha", "senha123",
    "qwerty", "abc123", "111111", "123123", "admin", "iloveyou",
    "letmein", "welcome", "000000", "654321", "1234", "12345",
]

def senhas_repetidas(usuario):
    limpar_terminal()
    print("-"*30)

    servicos = []
    senhas = []
    try:
        with open(arquivo_user(usuario), "r", encoding="utf-8") as file:
            for linha in file:
                linha = linha.strip().split("|")
                if len(linha) < 3:
                    continue
                servicos.append(linha[0])
                senhas.append(descriptografar(linha[2]))
    except FileNotFoundError:
        print("Nenhuma credencial cadastrada.")
        input("Pressione Enter para continuar...")
        return

    ja_agrupados = []
    encontrou = False

    for i in range(len(senhas)):
        if i in ja_agrupados:
            continue
        grupo = [servicos[i]]
        for j in range(i + 1, len(senhas)):
            if senhas[j] == senhas[i]:
                grupo.append(servicos[j])
                ja_agrupados.append(j)
        if len(grupo) > 1:
            encontrou = True
            print(f"⚠ Mesma senha em: {', '.join(grupo)}")

    if not encontrou:
        print("Não há senha repetida.")

    print("-"*30)
    input("Pressione Enter para continuar...")

def register_log(acao, usuario):
    with open("log.txt", "a", encoding="utf-8") as file:
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        file.write(f"{data_hora}|{usuario}|{acao}\n")

def consultar_log(usuario):
    limpar_terminal()
    print("-" * 30)
    print("Histórico de ações")
    print("-" * 30)

    encontrou = False
    try:
        with open("log.txt", "r", encoding="utf-8") as file:
            for linha in file:
                partes = linha.strip().split("|")
                if len(partes) < 3:      # ignora linhas do formato antigo
                    continue
                if partes[1] == usuario:
                    print(f"{partes[0]} - {partes[2]}")
                    encontrou = True
    except FileNotFoundError:
        pass

    if not encontrou:
        print("Nenhum registro encontrado.")

    print("-" * 30)
    input("Pressione Enter para continuar...")

def resumo_seguranca(usuario):
    limpar_terminal()

    servicos = []
    senhas = []
    datas = []
    try:
        with open(arquivo_user(usuario), "r", encoding="utf-8") as file:
            for linha in file:
                linha = linha.strip().split("|")
                if len(linha) < 6:
                    continue
                servicos.append(linha[0])
                senhas.append(descriptografar(linha[2]))
                datas.append(linha[5])
    except FileNotFoundError:
        pass

    print("-" * 30)
    print("Resumo de segurança")
    print("-" * 30)

    if len(senhas) == 0:
        print("Nenhuma credencial cadastrada.")
        print("-" * 30)
        input("Pressione Enter para continuar...")
        return

    # fracas
    fracas = 0
    for senha in senhas:
        forca = analise_forca_senha(senha)
        if forca is None or forca <= 1:
            fracas += 1

    # repetidas (conta as credenciais cuja senha aparece em mais de uma)
    repetidas = 0
    for i in range(len(senhas)):
        for j in range(len(senhas)):
            if i != j and senhas[i] == senhas[j]:
                repetidas += 1
                break

    # comuns
    comuns = 0
    for senha in senhas:
        if senha.lower() in SENHAS_COMUNS:
            comuns += 1

    print(f"Credenciais cadastradas: {len(senhas)}")
    print(f"Senhas fracas: {fracas}")
    print(f"Senhas repetidas: {repetidas}")
    print(f"Senhas na lista de senhas comuns: {comuns}")
    print("-" * 30)
    print("Tempo sem alterar cada senha ou tempo feito há cada alteração:")

    agora = datetime.now()
    for i in range(len(servicos)):
        try:
            data = datetime.strptime(datas[i].split(".")[0], "%Y-%m-%d %H:%M:%S")
            dias = (agora - data).days
            if dias == 0:
                tempo = "hoje"
            elif dias == 1:
                tempo = "há 1 dia"
            else:
                tempo = f"há {dias} dias"
        except ValueError:
            tempo = "data inválida"
        print(f"- {servicos[i]}: {tempo}")

    print("-" * 30)
    input("Pressione Enter para continuar...")

from datetime import date

#---pedro|pedro@gmail.com|password|banco|observacao|11-07-2026:7:00pm REGRA DE NEGOCIO DE ORGANIZACAO--------
from datetime import date

categoria = {
    "banco": "senha Forte",
    "trabalho": "senha Média",
    "redes sociais": "senha Boa",
    "estudos": "senha Forte",
    "outros": "senha Fraca"
}

def menu():
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
    print("Adicionar credencial")
    nome_credencial = input("Digite o nome do serviço: ")
    usuario_email_credencial = input("Digite o usuário ou e-mail: ")
    # Mostra as categorias existentes e a força mínima de cada uma
    consultar_categorias()

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
        print(forca_senha)
        if forca_senha == "senha forte":
            break
        else:
            print(f"A senha não atende a força mínima exigida para a categoria '{categoria_credencial}'.")
            senha_credencial = input("Digite uma nova senha: ")


    observacoes_credencial = input("Digite observações (opcional): ")
    data_cadastro = date.today().strftime("%d/%m/%Y")  # Data do cadastro no formato dd/mm/aaaa 
    lista = [nome_credencial, usuario_email_credencial, senha_credencial, categoria_credencial, observacoes_credencial, data_cadastro]
    
    #ADICIONARF AO TXT
    #---pedro|pedro@gmail.com|password|banco|observacao|11-07-2026:7:00pm REGRA DE NEGOCIO DE ORGANIZACAO--------
    # abrir e adicionar credenciais
    with open("credenciais.txt", "a", encoding="utf-8") as file:
        for i in lista:
            file.write(i)
            file.write("|")
            
        file.write("\n")



    
def ler_credenciais():
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

                
def atualizar_credencial():
    print("Atualizar credencial")
    nome_credencial = input("Digite o nome do serviço que deseja atualizar: ")
    with open("credenciais.txt", "r", encoding="utf-8") as file:
            
            for linha in file:
                linha = linha.split("|")


                if nome_credencial == linha[0]:
                    linha_antiga = linha.copy()  # Copia a linha antiga para comparação posterior
                    credencial = input("Digite o campo que deseja atualizar (nome, usuário, senha, categoria, observações): ").lower()

                    if credencial == "nome":
                        nova_credencial = input("Digite o novo nome do serviço: ")
                        linha[0] = nova_credencial
                        

                    elif credencial == "usuário":
                        novo_usuario = input("Digite o novo usuário ou e-mail: ")
                        linha[1] = novo_usuario

                    elif credencial == "senha":
                        nova_senha = input("Digite a nova senha: ")
                        linha[2] = nova_senha

                    elif credencial == "categoria":
                        nova_categoria = input("Digite a nova categoria: ").lower()

                        if nova_categoria not in categoria:
                            print("Categoria não existe. Deseja cadastrar essa nova categoria? (s/n)")

                            if input().lower() == "s":
                                cadastrar_categoria(nova_categoria)

                            else:
                                nova_categoria = "outros"
                                print("A credencial foi colocada em 'outros'.")

                        linha[3] = nova_categoria
                    elif credencial == "observações":
                        novas_observacoes = input("Digite as novas observações: ")
                        linha[4] = novas_observacoes

                    data_cadastro = date.today().strftime("%d/%m/%Y") 
                    linha[5] = data_cadastro
                
                    print("Credencial atualizada com sucesso!")
                  
                    with open("credenciais.txt", "r", encoding="utf-8") as file:#ler todas as linhas do arquivo e guarda numna lista
                        linhas = file.readlines()

                    with open("credenciais.txt", "w", encoding="utf-8") as file:
                        for l in linhas:# vai passar por todas as linhas do arquivo e vai escrever no arquivo novamente, mas se a linha for a que foi atualizada, ele escreve a nova linha
                            
                            if l.strip() != "|".join(linha_antiga).strip():#se NAO FOR A LINHA antiga,ele escreve a linha do arquivo
                                file.write(l)
                            else:#SE FOR A LINHA DO ARQUIVO, ELE ESCREVE A LINHA ATUALIZADA
                                file.write("|".join(linha) + "\n")
                            
                    


        




def consultar_categorias():
    for i in categoria:
        print(f"Categoria: {i}, Força mínima: {categoria[i]}")



def cadastrar_categoria(categoria_nova):
    #perguntar_forca_minima
    forca_minima = input("Digite a força mínima para a nova categoria(senha Fraca, senha Média, senha Forte): ").lower()
    categoria[categoria_nova] = forca_minima


#---------------------------#



def analise_forca_senha(senha):
    status_maisculo = False
    status_minus = False
    tamanho = True
    num = False
    caracter = False

    lista = ["!", '@', "#", '$', '%', "&", "*", "-", "_", "?", "/","+","="]
    if len(senha) >=6:
        for i in range(len(senha)):
            if senha[i]!=senha[i].upper():
                for i in range(len(senha)):
                        if senha[i]!=senha[i].lower():
                            for i in senha:
                                if i.isdigit()== False:
                                    for i in lista:
                                        if i in senha:
                                            caracter = True
                                        else:
                                            pass
                                else:
                                    num = True
                        else:
                            status_minus = True
            else:
                status_maisculo = True
    else:
        tamanho = False

    if status_maisculo == False and status_minus == False and tamanho == False and num == False and caracter == False:
        return "senha fraca"
    if status_maisculo == False and status_minus == False and tamanho == False:
        return "senha media"
    if status_maisculo != False and status_minus != False and tamanho != False and num != False and caracter != False:
        return "senha forte"
    
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

lista = []
senha_repetida = risk_detection(lista)
if senha_repetida == 0:
        print("Não há senha repetida.")
else:
        print(f"Há {int(len(senha_repetida))//2} senhas repetidas.")
print(risk_detection(lista))

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# login e listas

nome = []
usuario_email = []
senha = []
categoria = ["banco", "rede social", "estudo", "trabalho", "outros"]
forca_minima = [0, 0, 0, 0, 0]  # Força mínima de senha para cada categoria
categoria_credenciais = []   
observacoes = []
data_ultimo_cadastro_ou_alteracao = []
usuario = []
senha_login = []
usuario_logado = ""  # guarda quem fez login

# Login antes de acessar o CRUD     

def login():
    global usuario_logado
    print("tatu: gerenciamento de credenciais.")
    print("Login ou criar conta? (l/c)")
    resposta = input().lower()
    if resposta == "c":
        print("Criar conta")
        usuario.append(input("Digite o nome de usuário: "))
        senha_login.append(input("Digite a senha: "))
        print("Conta criada com sucesso! Agora faça o login.")
        login()
    elif resposta == "l":
        print("Login")
        usuario_digitado = input("Digite o nome de usuário: ")
        senha_digitada = input("Digite a senha: ")
        if usuario_digitado in usuario and senha_login[usuario.index(usuario_digitado)] == senha_digitada:
            usuario_logado = usuario_digitado
            print("Login realizado com sucesso!")
            menu()
        else:
            print("Usuário ou senha incorretos. Tente novamente.")
            login()
    else:
        print("Opção inválida. Tente novamente.")
        login()

# Analisar força da senha

def forca_da_senha(senha_digitada):
    forca = 0
    if len(senha_digitada) >= 8:
        forca = forca + 1
    tem_maiuscula = False
    tem_numero = False
    tem_simbolo = False
    for letra in senha_digitada:
        if letra.isupper():
            tem_maiuscula = True
        elif letra.isdigit():
            tem_numero = True
        elif not letra.isalnum():
            tem_simbolo = True
    if tem_maiuscula:
        forca = forca + 1
    if tem_numero:
        forca = forca + 1
    if tem_simbolo:
        forca = forca + 1
    return forca


# Pedir força mínima (0 a 4)

def pedir_forca():
    print("0 - Fraca, 1 - Média, 2 - Boa, 3 - Forte, 4 - Muito Forte")
    forca = input("Força mínima da senha para essa categoria (0 a 4): ")
    while forca not in ["0", "1", "2", "3", "4"]:
        forca = input("Digite um número de 0 a 4: ")
    return int(forca)

# Categorias

def consultar_categorias():
    print("Categorias:")
    for i in range(len(categoria)):
        print(f"{categoria[i]} - força mínima: {forca_minima[i]}")

def cadastrar_categoria(nome_categoria):
    if nome_categoria in categoria:
        # se já existe, só muda a força mínima
        forca_minima[categoria.index(nome_categoria)] = pedir_forca()
        print(f"Força mínima de {nome_categoria} atualizada!")
    else:
        categoria.append(nome_categoria)
        forca_minima.append(pedir_forca())
        print(f"Categoria {nome_categoria} cadastrada com sucesso!")

# Adicionar

def adicionar_credencial():
    print("Adicionar credencial")
    nome_credencial = input("Digite o nome do serviço: ")
    usuario_email_credencial = input("Digite o usuário ou e-mail: ")

    # Mostra as categorias existentes e a força mínima de cada uma
    consultar_categorias()
    print("Deseja cadastrar uma nova categoria ou mudar a força mínima de uma existente? (s/n)")
    if input().lower() == "s":
        cadastrar_categoria(input("Nome da categoria: ").lower())
        consultar_categorias()

    categoria_credencial = input("Digite a categoria: ").lower()
    if categoria_credencial not in categoria:
        print("Categoria não existe. Deseja cadastrar essa nova categoria? (s/n)")
        if input().lower() == "s":
            cadastrar_categoria(categoria_credencial)
        else:
            categoria_credencial = "outros"
            print("A credencial foi colocada em 'outros'.")

    # Se o usuário escolher uma categoria já existente, o sistema deve verificar se a senha atende à força mínima exigida para aquela categoria. Se não atender, o sistema deve solicitar que o usuário digite uma nova senha até que ela atenda à força mínima exigida.
    minimo = forca_minima[categoria.index(categoria_credencial)]
    while True:
        senha_credencial = input("Digite a senha: ")
        if forca_da_senha(senha_credencial) >= minimo:
            break
        print(f"Senha fraca! Força {forca_da_senha(senha_credencial)}, mas a categoria {categoria_credencial} exige {minimo}.")
        print("Dica: use 8+ caracteres, letra maiúscula, número e símbolo.")

    observacoes_credencial = input("Digite observações (opcional): ")
    data_cadastro = date.today().strftime("%d/%m/%Y")  # Data do cadastro no formato dd/mm/aaaa 

    nome.append(nome_credencial)
    usuario_email.append(usuario_email_credencial)
    senha.append(senha_credencial)
    categoria_credenciais.append(categoria_credencial)
    observacoes.append(observacoes_credencial)
    data_ultimo_cadastro_ou_alteracao.append(data_cadastro)

    print("Credencial adicionada com sucesso!")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Ler

def ler_credenciais():
    if len(nome) == 0:
        print("Nenhuma credencial cadastrada.")
        return
    print("Credenciais:")
    print("-" * 30)
    for i in range(len(nome)):
        print(f"Nome do serviço: {nome[i]}")
        print(f"Usuário ou e-mail: {usuario_email[i]}")
        print(f"Senha: {senha[i][:2]}{'*' * (len(senha[i]) - 2)}")  # Mostra apenas os dois primeiros caracteres da senha
        print(f"Categoria: {categoria_credenciais[i]}")
        print(f"Observações: {observacoes[i]}")
        print(f"Data do último cadastro ou alteração: {data_ultimo_cadastro_ou_alteracao[i]}")
        print("-" * 30)
        print("Deseja revelar a senha completa? (s/n)")
        if input().lower() == "s":
        # Terá que usar a senha do login para revelar a senha
            print("Digite a senha do login para revelar a senha completa: ")
            senha_revelada = input()
            if senha_revelada == senha_login[usuario.index(usuario_logado)]:
                print(f"Login: {usuario_email[i]} - Senha: {senha[i]}")
            else:
                print("Senha incorreta. Não é possível revelar a senha.")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Atualizar

def atualizar_credencial():
    print("Atualizar credencial")
    nome_credencial = input("Digite o nome do serviço que deseja atualizar: ")
    if nome_credencial in nome:
        index = nome.index(nome_credencial)
        usuario_email[index] = input("Digite o novo usuário ou e-mail: ")


        consultar_categorias()
        nova_categoria = input("Digite a nova categoria: ").lower()
        if nova_categoria not in categoria:
            print("Categoria não existe. Deseja cadastrar essa nova categoria? (s/n)")
            if input().lower() == "s":
                cadastrar_categoria(nova_categoria)
            else:
                nova_categoria = "outros"
                print("A credencial foi colocada em 'outros'.")
        categoria_credenciais[index] = nova_categoria

        minimo = forca_minima[categoria.index(nova_categoria)]
        nova_senha = input("Digite a nova senha: ")
        while forca_da_senha(nova_senha) < minimo:
            print(f"Senha fraca! Força {forca_da_senha(nova_senha)}, mas a categoria {nova_categoria} exige {minimo}.")
            print("Dica: use 8+ caracteres, letra maiúscula, número e símbolo.")
            nova_senha = input("Digite a nova senha: ")
        senha[index] = nova_senha
        observacoes[index] = input("Digite novas observações (opcional): ")
        data_ultimo_cadastro_ou_alteracao[index] = date.today().strftime("%d/%m/%Y")
        print("Credencial atualizada com sucesso!")
    else:
        print("Credencial não encontrada.")






def detectar_risco():
    lista_repetida = []
    lista = []
    with open("credenciais.txt", "r", encoding="utf-8") as file:
        for linha in file:
            linha = linha.strip().split("|")
            posicao_linha = 0
            if linha[2] not in lista:
                lista.append(linha[posicao_linha])
                lista.append(linha[2])
            else:
                x = lista.index(linha[2])
                lista_repetida.append(lista[x-1])
                lista_repetida.append(lista[x])
                lista_repetida.append(linha[0])
                lista_repetida.append(linha[2])
            posicao_linha += 1
        for i in range(0, len(lista_repetida), 2):
            print(f"Serviço: {lista_repetida[i]}, Senha: {lista_repetida[i+1][:2]}{'*' * (len(lista_repetida[i+1]) - 2)} - Risco de senha repetida!")
#-----------------------------#


def excluir_credencial():
    nome_credencial = input("Digite o nome do serviço que deseja excluir: ")
    with open("credenciais.txt", "r", encoding="utf-8") as file:
        linhas = file.readlines()

    with open("credenciais.txt", "w", encoding="utf-8") as file:
        for linha in linhas:
            if linha.strip().split("|")[0] != nome_credencial:
                file.write(linha)
            else:
                print(f"Credencial '{nome_credencial}' excluída com sucesso!")





#loop principal
while True:
    opcao = menu()
    if opcao == "7":
        break
    if opcao == "1":
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
        cadastrar_categoria(input("Digite o nome da nova categoria: ").lower())
    print("-"*30)
    detectar_risco()


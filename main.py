from datetime import date

#-----------------------------------------------------------------------------------verificacao de forca de senha--------------------------------------------------------------------------------------------------
x = str(input("digite a senha: "))
def verificar_senha(senha):
    status_maisculo = False
    status_minus = False
    tamanho = True
    num = False
    caracter = False

    lista = ["!", '@', "#", '$', '%', "&", "*", "-", "_", "?", "/","+","="]
    if len(x) >=6:
        for i in range(len(x)):
            if x[i]!=x[i].upper():
                for i in range(len(x)):
                        if x[i]!=x[i].lower():
                            for i in x:
                                if i.isdigit()== False:
                                    for i in lista:
                                        if i in x:
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

    if status_maisculo == False:
        print("Sem letra maiscula")
    if status_minus == False:
        print("Sem letra minuscula")
    if tamanho == False:
            print("Sem tamanho")
    if num == False:
            print("Sem numero")
    if caracter == False:
            print("Sem caracter especial")

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

#Ler

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
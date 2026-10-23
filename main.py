

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
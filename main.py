

#-----------------------------------------------------------------------------------verificacao de forca de senha--------------------------------------------------------------------------------------------------
x = str(input("digite a senha: "))
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

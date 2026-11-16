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
    else:
        return 0
        
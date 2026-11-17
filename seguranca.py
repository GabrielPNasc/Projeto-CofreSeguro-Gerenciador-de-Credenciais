import os


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
##
# ---------- criptografia ----------
CHAVE = os.getenv("CHAVE_MESTRA")
M = 0xFFFFFFFFFFFFFFFF

def _fluxo(tamanho_senha):
    estado = 14695981039346656037
    for b in CHAVE.encode():
        estado ^= b
        estado = (estado * 1099511628211) & M
    saida = []
    for _ in range(tamanho_senha):
        estado ^= (estado << 13) & M
        estado ^= estado >> 7
        estado ^= (estado << 17) & M
        saida.append(estado & 0xFF)
    return saida

def criptografar(senha):
    dados = senha.encode()
    fluxo = _fluxo(len(dados))
    return bytes(a ^ b for a, b in zip(dados, fluxo)).hex()

def descriptografar(senha_criptografada):
    cifrado = bytes.fromhex(senha_criptografada)
    fluxo = _fluxo(len(cifrado))
    return bytes(a ^ b for a, b in zip(cifrado, fluxo)).decode()

        ##
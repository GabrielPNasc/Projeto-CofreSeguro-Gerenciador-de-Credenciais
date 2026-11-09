"""
agente.py — Módulo do Agente LLM (biblioteca oficial groq)
CESAR School | Fundamentos de Programação | 2026.2

Permite fazer perguntas em linguagem natural sobre os dados do seu sistema.
O módulo lê um arquivo .csv ou .txt, monta um texto (prompt) com os dados e a
pergunta, envia esse texto para um modelo de linguagem e devolve a resposta.

COMO USAR NO SEU PROJETO
------------------------
Há duas formas de enviar os dados ao agente.

1) A partir dos dados na memória (lista de dicionários), montando o texto:

    from agente import falar_com_agente_texto

    texto = "servico,categoria\n"
    for credencial in credenciais:
        texto += credencial["servico"] + "," + credencial["categoria"] + "\n"

    pergunta = input("O que você quer perguntar sobre seus dados? > ")
    resposta = falar_com_agente_texto(texto, pergunta, "CofreSeguro")

2) A partir de um arquivo .csv ou .txt:

    from agente import falar_com_agente
    resposta = falar_com_agente("dados.csv", pergunta, "CofreSeguro")

As duas funções devolvem a resposta (texto) quando dá certo, ou None quando dá
errado. Como a pergunta é feita no SEU código, você pode registrá-la no log.

CONFIGURAÇÃO DA CHAVE
---------------------
A chave NÃO fica escrita no código. Ela fica num arquivo chamado .env, na
mesma pasta deste módulo:
    1. Acesse https://console.groq.com e crie uma conta gratuita
    2. Vá em "API Keys" e clique em "Create API Key"
    3. Copie o arquivo .env.example com o nome .env
    4. No .env, troque cole_sua_chave_aqui pela sua chave
O arquivo .env é seu: nunca o envie para o GitHub, nunca o compartilhe e
nunca o mostre em apresentações. Se a chave vazar, apague-a no console da
Groq e crie outra.

(Também funciona configurar a variável de ambiente GROQ_API_KEY no terminal.)

Observação: a biblioteca groq é uma exceção autorizada apenas para este módulo.
Instalação: pip install groq
"""

import os

try:
    from groq import Groq
except ImportError:
    Groq = None


# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

TEXTO_MODELO_CHAVE = "cole_sua_chave_aqui"


def carregar_arquivo_env():
    """
    Lê as variáveis do arquivo .env que está na mesma pasta deste módulo.
    Cada linha tem o formato NOME=valor. Linhas vazias ou com # são ignoradas.
    Uma variável já configurada no terminal tem prioridade sobre o .env.
    """
    pasta = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta, ".env")
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha or linha.startswith("#") or "=" not in linha:
                    continue
                nome, valor = linha.split("=", 1)
                nome = nome.strip()
                valor = valor.strip().strip('"').strip("'")
                if nome and nome not in os.environ:
                    os.environ[nome] = valor
    except FileNotFoundError:
        pass


carregar_arquivo_env()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if GROQ_API_KEY == TEXTO_MODELO_CHAVE:
    GROQ_API_KEY = ""

GROQ_MODEL = "llama-3.3-70b-versatile"

# Arquivos muito grandes ultrapassam o limite de texto do modelo.
LIMITE_CARACTERES = 20000


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def ler_dados(nome_arquivo):
    """Lê o arquivo de dados. Devolve o conteúdo (texto) ou None se houver erro."""
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
    except FileNotFoundError:
        print(f"\n[T.a.t.u] Arquivo '{nome_arquivo}' não encontrado.")
        return None
    except PermissionError:
        print(f"\n[T.a.t.u] Sem permissão para ler '{nome_arquivo}'.")
        return None
    except UnicodeDecodeError:
        print(f"\n[T.a.t.u] O arquivo '{nome_arquivo}' não está em UTF-8.")
        return None

    if not conteudo.strip():
        print("\n[T.a.t.u] O arquivo está vazio. Crie alguns registros antes de perguntar.")
        return None

    if len(conteudo) > LIMITE_CARACTERES:
        print(f"\n[T.a.t.u] O arquivo tem {len(conteudo)} caracteres, acima do limite de "
              f"{LIMITE_CARACTERES}.")
        print("         Envie apenas os registros necessários para a pergunta.")
        return None

    return conteudo


def montar_prompt(conteudo, pergunta, nome_sistema):
    """Junta as instruções, os dados e a pergunta num único texto."""
    return f"""Você é um assistente inteligente do sistema {nome_sistema}.

Seu papel é analisar os dados fornecidos e responder perguntas do usuário de forma clara, objetiva e útil.

DADOS DO SISTEMA:
---
{conteudo}
---

PERGUNTA DO USUÁRIO: {pergunta}

INSTRUÇÕES PARA SUA RESPOSTA:
1. Responda SEMPRE em português do Brasil
2. Baseie sua resposta APENAS nos dados fornecidos acima
3. Se os dados não contêm informação suficiente, diga isso claramente
4. Seja objetivo e direto, sem repetir a pergunta nem fazer preâmbulos longos
5. Use formatação clara (listas, números) quando apropriado
6. Se identificar padrões interessantes nos dados, mencione-os

Responda agora:"""


def criar_cliente():
    """Cria o cliente da Groq. Devolve o cliente ou None se houver problema."""
    if Groq is None:
        print("\n[T.a.t.u] A biblioteca groq não está instalada.")
        print("         Instale com: pip install groq")
        return None

    if not GROQ_API_KEY:
        print("\n[T.a.t.u] A chave da API não foi configurada.")
        print("         Crie o arquivo .env (copie o .env.example) e cole sua chave nele.")
        print("         Veja as instruções no início do arquivo agente.py.")
        return None

    try:
        return Groq(api_key=GROQ_API_KEY)
    except Exception as erro:
        print(f"\n[T.a.t.u] Erro ao inicializar o cliente: {erro}")
        return None


def explicar_erro(erro):
    """Mostra uma mensagem compreensível para os erros mais comuns da API."""
    texto = str(erro).lower()

    if "api_key" in texto or "authentication" in texto or "401" in texto:
        print("\n[T.a.t.u] Erro de autenticação: a chave é inválida ou expirou.")
        print("         Gere uma nova chave em https://console.groq.com/keys")
    elif "rate_limit" in texto or "429" in texto:
        print("\n[T.a.t.u] Limite de requisições excedido. Aguarde alguns minutos.")
    elif "quota" in texto or "exceeded" in texto:
        print("\n[T.a.t.u] Limite de uso da conta gratuita atingido.")
    elif "connection" in texto or "timeout" in texto:
        print("\n[T.a.t.u] Sem conexão com o serviço. Verifique a internet.")
    else:
        print(f"\n[T.a.t.u] Erro ao consultar a API: {erro}")


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def falar_com_agente(nome_arquivo, pergunta, nome_sistema="Sistema", streaming=False):
    """
    Responde a uma pergunta sobre os dados de um ARQUIVO usando um modelo de linguagem.

    Parâmetros:
        nome_arquivo: caminho do arquivo .csv ou .txt com os dados
        pergunta:     a pergunta do usuário (texto)
        nome_sistema: nome do sistema, usado no prompt
        streaming:    se True, mostra a resposta enquanto ela é gerada

    Devolve:
        a resposta do modelo (texto), ou None se algo der errado
    """
    conteudo = ler_dados(nome_arquivo)
    if conteudo is None:
        return None

    return falar_com_agente_texto(conteudo, pergunta, nome_sistema, streaming)


def falar_com_agente_texto(conteudo, pergunta, nome_sistema="Sistema", streaming=False):
    """
    Responde a uma pergunta sobre dados que VOCÊ monta como texto.

    Use esta função quando os dados estão na memória do seu programa
    (por exemplo, numa lista de dicionários). Você escolhe o que entra
    no texto, e só isso é enviado ao modelo.

    Parâmetros:
        conteudo:     os dados, em texto (por exemplo, uma linha por registro)
        pergunta:     a pergunta do usuário (texto)
        nome_sistema: nome do sistema, usado no prompt
        streaming:    se True, mostra a resposta enquanto ela é gerada

    Devolve:
        a resposta do modelo (texto), ou None se algo der errado
    """
    if not pergunta or not pergunta.strip():
        print("\n[T.a.t.u] Nenhuma pergunta foi digitada.")
        return None

    if not conteudo or not conteudo.strip():
        print("\n[T.a.t.u] Não há dados para enviar. Cadastre alguns registros antes.")
        return None

    if len(conteudo) > LIMITE_CARACTERES:
        print(f"\n[T.a.t.u] Os dados têm {len(conteudo)} caracteres, acima do limite de "
              f"{LIMITE_CARACTERES}.")
        print("         Envie apenas os registros necessários para a pergunta.")
        return None

    cliente = criar_cliente()
    if cliente is None:
        return None

    prompt = montar_prompt(conteudo, pergunta.strip(), nome_sistema)

    try:
        print("\nConsultando o agente...")
        completion = cliente.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_completion_tokens=1024,
            top_p=0.9,
            stream=streaming,
        )

        print("\n" + "=" * 70)
        print("AGENTE:")
        print("=" * 70)

        if streaming:
            resposta = ""
            for pedaco in completion:
                texto = pedaco.choices[0].delta.content or ""
                print(texto, end="", flush=True)
                resposta += texto
            print()
        else:
            resposta = completion.choices[0].message.content
            print(resposta)

        print("=" * 70)
        return resposta

    except Exception as erro:
        explicar_erro(erro)
        return None


# ============================================================================
# TESTE DIRETO DO MÓDULO (python agente.py)
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("=" * 70)

    if not GROQ_API_KEY:
        print("\nA chave da API não está configurada.")
        print("Veja as instruções no início do arquivo agente.py.")
    else:
        arquivo_teste = "teste_agente.csv"
        with open(arquivo_teste, "w", encoding="utf-8") as f:
            f.write("id,nome,categoria,valor,data_criacao\n")
            f.write("1,Notebook,Eletrônicos,3500.00,2026-05-20 10:30:00\n")
            f.write("2,Mouse,Eletrônicos,50.00,2026-05-21 14:15:00\n")
            f.write("3,Cadeira,Móveis,800.00,2026-05-22 09:00:00\n")
        print(f"\nArquivo de teste criado: {arquivo_teste}")

        pergunta_teste = input("\nFaça uma pergunta sobre os dados de teste > ")
        resposta = falar_com_agente(arquivo_teste, pergunta_teste, "Sistema de Teste")

        if resposta is None:
            print("\nO teste não foi concluído.")
        else:
            print("\nTeste concluído.")

import io
import re
import sys
import asyncio
import builtins
import traceback
from contextlib import redirect_stdout

import flet as ft

from agente import falar_com_agente
from crud import *
from login import *

# ---------- Tema do tatu: preto, branco e cinza ----------
PRETO = "#0A0A0A"
CARD = "#171717"
CARD2 = "#262626"
CINZA = "#9E9E9E"
BRANCO = "#FFFFFF"

# ---------- Animação de abertura (tempos em ms) ----------
PALAVRA = "TATU"
T_FADE = 700
T_LETRA = 0.7        # s entre uma letra e outra
T_JUNTAR = 1000
T_GIRO = 2500
LARGURA_LETRA = 60
TAM = 260
IMG_FINAL = 180
IMG_INICIAL = 70
VOLTA = 6.283185307179586   # 360 graus em radianos


def diag(*msg):
    print("[app]", *msg, file=sys.stderr, flush=True)


# ---------- Componentes ----------
def campo(label, **kw):
    return ft.TextField(
        label=label,
        color=BRANCO,
        bgcolor=CARD2,
        border_color=CARD2,
        focused_border_color=BRANCO,
        cursor_color=BRANCO,
        label_style=ft.TextStyle(color=CINZA),
        border_radius=10,
        **kw,
    )


def estilo(primario=True):
    return ft.ButtonStyle(
        bgcolor=BRANCO if primario else CARD2,
        color=PRETO if primario else BRANCO,
        shape=ft.RoundedRectangleBorder(radius=10),
    )


def botao(texto, ao_clicar, primario=True):
    return ft.ElevatedButton(texto, on_click=ao_clicar, height=46, style=estilo(primario))


def card(*controles):
    return ft.Container(
        bgcolor=CARD,
        border_radius=14,
        padding=14,
        content=ft.Column(
            list(controles),
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )


def titulo(texto):
    return ft.Text(texto, size=20, weight=ft.FontWeight.BOLD, color=BRANCO)


def logo(tamanho):
    return ft.Image(
        src="tatu.png",
        width=tamanho,
        height=tamanho,
        error_content=ft.Text("TATU", color=BRANCO, weight=ft.FontWeight.BOLD),
    )


def tile(icone, titulo_, sub, acao):
    return ft.Container(
        bgcolor=CARD,
        border_radius=14,
        padding=14,
        ink=True,
        on_click=lambda e: acao(),
        content=ft.Row(
            [
                ft.Icon(icone, color=BRANCO, size=26),
                ft.Column(
                    [
                        ft.Text(titulo_, color=BRANCO, weight=ft.FontWeight.BOLD),
                        ft.Text(sub, color=CINZA, size=12),
                    ],
                    spacing=0,
                    expand=True,
                ),
            ],
            spacing=14,
        ),
    )


def coluna(*controles):
    return ft.Column(
        list(controles),
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )


def tipo_campo(prompt):
    """Decide se a pergunta pede um número ou uma senha de verdade."""
    t = prompt.lower()
    numerico = bool(
        re.search(
            r"n[úu]mero|n[º°]|op[çc][ãa]o|[íi]ndice|posi[çc][ãa]o|linha|\bid\b|escolha"
            r"|qual .*(deseja|quer|atualizar|excluir|editar|apagar)"
            r"|(deseja|quer) (atualizar|excluir|editar|apagar)",
            t,
        )
    )
    senha = (not numerico) and "senha" in t
    return numerico, senha


# ---------- Infraestrutura para rodar as funções do CMD dentro da janela ----------
class Cancelado(BaseException):
    """Usuário saiu da tela no meio da ação."""


class Recusado(BaseException):
    """Usuário disse 'não' na confirmação."""


class Fluxo:
    def __init__(self, loop):
        self.loop = loop
        self.fut = None
        self.cancelado = False
        self.confirmado = False

    def cancelar(self):
        self.cancelado = True
        fut = self.fut
        if fut is not None:
            self.loop.call_soon_threadsafe(lambda: None if fut.done() else fut.set_result(None))


class Saida(io.TextIOBase):
    """Recebe tudo que as funções dão print()."""

    def __init__(self, ao_escrever):
        self.ao_escrever = ao_escrever

    def write(self, s):
        self.ao_escrever(s)
        return len(s)

    def flush(self):
        pass


# ---------- App ----------
def main(page: ft.Page):
    page.title = "TATU Cofre"
    page.window.width = 460
    page.window.height = 820
    page.bgcolor = PRETO
    page.padding = 0

    estado = {"usuario": None, "fluxo": None, "intro": False}

    # =============== AVISO (balão no topo) ===============
    aviso_txt = ft.Text("", expand=True, size=14)

    def fechar_aviso(e=None):
        aviso.visible = False
        page.update()

    aviso = ft.Container(
        visible=False,
        border_radius=12,
        padding=12,
        content=ft.Row(
            [aviso_txt, ft.IconButton(icon=ft.Icons.CLOSE, icon_size=18, on_click=fechar_aviso)],
            spacing=8,
        ),
    )

    def mensagem(texto, erro=False):
        aviso.bgcolor = BRANCO if erro else CARD2
        aviso_txt.color = PRETO if erro else BRANCO
        aviso_txt.value = ("⚠ " if erro else "✓ ") + texto
        aviso.visible = True
        page.update()

    # =============== ESTRUTURA COMUM ===============
    def montar(corpo, voltar=False, com_sair=False):
        antigo = estado.get("fluxo")
        if antigo:
            antigo.cancelar()
            estado["fluxo"] = None

        aviso.visible = False
        topo = []
        if voltar:
            topo.append(ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=BRANCO,
                                      tooltip="Voltar ao menu", on_click=lambda e: tela_menu()))
        topo.append(logo(40))
        topo.append(
            ft.Column(
                [
                    ft.Text("TATU", size=22, weight=ft.FontWeight.BOLD, color=BRANCO),
                    ft.Text("cofre de credenciais", size=11, color=CINZA),
                ],
                spacing=0,
                expand=True,
            )
        )
        if com_sair:
            topo.append(ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=BRANCO,
                                      tooltip="Sair", on_click=sair))
        page.clean()
        page.add(
            ft.Container(
                expand=True,
                padding=16,
                content=ft.Column(
                    [ft.Row(topo, spacing=10), aviso, ft.Container(content=corpo, expand=True)],
                    expand=True,
                    spacing=12,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
            )
        )

    # =============== EXECUTAR UMA FUNÇÃO DO CMD NA TELA ===============
    async def executar(titulo_, func, *args, log_acao=None, confirmar=None, **kwargs):
        diag("iniciando:", getattr(func, "__name__", func))
        loop = asyncio.get_running_loop()
        fluxo = Fluxo(loop)

        mensagens = ft.Column(spacing=8, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
        pergunta_box = ft.Container()
        carregando = ft.ProgressRing(color=BRANCO, width=22, height=22)
        rodape = ft.Container()

        corpo = ft.Column(
            [titulo(titulo_), mensagens, pergunta_box, ft.Row([carregando]), rodape],
            scroll=ft.ScrollMode.AUTO,
            auto_scroll=True,
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
        montar(corpo, voltar=True, com_sair=True)
        estado["fluxo"] = fluxo

        async def add_msg(texto, erro=False):
            if fluxo.cancelado:
                return
            mensagens.controls.append(
                ft.Container(
                    bgcolor=BRANCO if erro else CARD,
                    border_radius=12,
                    padding=12,
                    content=ft.Text(texto, color=PRETO if erro else BRANCO, selectable=True),
                )
            )
            page.update()

        def botao_voltar():
            return botao("Voltar ao menu", lambda e: tela_menu(), primario=False)

        async def perguntar(prompt):
            diag("pergunta:", prompt)
            texto = prompt.strip()
            numerico, senha = tipo_campo(texto)

            extra = {}
            if numerico:
                extra["keyboard_type"] = ft.KeyboardType.NUMBER
                if hasattr(ft, "NumbersOnlyInputFilter"):
                    extra["input_filter"] = ft.NumbersOnlyInputFilter()

            c = campo("Sua resposta", password=senha, can_reveal_password=senha,
                      autofocus=True, **extra)
            fut = loop.create_future()
            fluxo.fut = fut

            async def enviar(e):
                v = (c.value or "").strip() if numerico else (c.value or "")
                if numerico and not v.isdigit():
                    mensagem("Digite apenas números.", erro=True)
                    return
                if not fut.done():
                    fut.set_result(v)

            c.on_submit = enviar
            pergunta_box.content = card(ft.Text(texto, color=BRANCO), c, botao("Enviar", enviar))
            carregando.visible = False
            page.update()

            valor = await fut
            if fluxo.cancelado or valor is None:
                return ("cancelado", "")

            pergunta_box.content = None
            mostrado = "•" * len(valor) if senha else valor
            mensagens.controls.append(
                ft.Text(f"{texto.rstrip(':')}: {mostrado}", color=CINZA, size=12)
            )

            # ----- confirmação (usada no excluir) -----
            if confirmar and not fluxo.confirmado:
                fluxo.confirmado = True
                fut2 = loop.create_future()
                fluxo.fut = fut2

                async def sim(e):
                    if not fut2.done():
                        fut2.set_result(True)

                async def nao(e):
                    if not fut2.done():
                        fut2.set_result(False)

                pergunta_box.content = card(
                    ft.Text("Tem certeza?", size=18, weight=ft.FontWeight.BOLD, color=BRANCO),
                    ft.Text(f"{confirmar} (você escolheu: {valor}). Essa ação não pode ser desfeita.",
                            color=CINZA),
                    ft.Row(
                        [
                            ft.ElevatedButton("Cancelar", on_click=nao, height=46,
                                              style=estilo(False), expand=True),
                            ft.ElevatedButton("Sim, excluir", on_click=sim, height=46,
                                              style=estilo(True), expand=True),
                        ],
                        spacing=8,
                    ),
                )
                page.update()
                ok = await fut2
                if fluxo.cancelado or ok is None:
                    return ("cancelado", "")
                pergunta_box.content = None
                if not ok:
                    return ("recusado", "")

            carregando.visible = True
            page.update()
            return ("ok", valor)

        async def terminar(ret, erro):
            diag("terminou:", getattr(func, "__name__", func), "| erro:", erro)
            if fluxo.cancelado:
                return
            if isinstance(ret, str) and ret.strip():
                await add_msg(ret)
            if erro is not None:
                if isinstance(erro, ValueError):
                    await add_msg(f"Erro: valor inválido (a função esperava um número). {erro}", erro=True)
                else:
                    await add_msg(f"Erro: {erro}", erro=True)
            elif log_acao:
                try:
                    register_log(log_acao)
                except Exception as ex:
                    diag("register_log falhou:", ex)
            carregando.visible = False
            rodape.content = botao_voltar()
            page.update()

        async def recusado():
            if fluxo.cancelado:
                return
            await add_msg("Exclusão cancelada. Nada foi apagado.")
            carregando.visible = False
            rodape.content = botao_voltar()
            page.update()

        def trabalho():
            """Roda a SUA função em segundo plano. Todo acesso à tela passa pelo laço do Flet."""
            buffer = []

            def despejar():
                texto = "".join(buffer).strip()
                buffer.clear()
                if texto and not fluxo.cancelado:
                    asyncio.run_coroutine_threadsafe(add_msg(texto), loop).result()

            def meu_input(prompt=""):
                despejar()
                if fluxo.cancelado:
                    raise Cancelado()
                status, valor = asyncio.run_coroutine_threadsafe(
                    perguntar(str(prompt)), loop
                ).result()
                if status == "cancelado":
                    raise Cancelado()
                if status == "recusado":
                    raise Recusado()
                return valor

            original = builtins.input
            builtins.input = meu_input
            ret, erro, recusou = None, None, False
            try:
                with redirect_stdout(Saida(buffer.append)):
                    ret = func(*args, **kwargs)
            except Cancelado:
                return
            except Recusado:
                recusou = True
            except Exception as ex:
                erro = ex
                traceback.print_exc()
            finally:
                builtins.input = original

            despejar()
            if recusou:
                asyncio.run_coroutine_threadsafe(recusado(), loop).result()
            else:
                asyncio.run_coroutine_threadsafe(terminar(ret, erro), loop).result()

        await asyncio.to_thread(trabalho)

    def ir(titulo_, func, *args, log_acao=None, confirmar=None, **kwargs):
        page.run_task(executar, titulo_, func, *args,
                      log_acao=log_acao, confirmar=confirmar, **kwargs)

    def rodar_simples(func, *args):
        """Para funções sem input(): devolve (retorno, texto que elas imprimiram)."""
        buffer = io.StringIO()
        original = builtins.input

        def sem_input(prompt=""):
            raise RuntimeError("essa função pede input() e não funciona direto aqui")

        builtins.input = sem_input
        retorno = None
        try:
            with redirect_stdout(buffer):
                retorno = func(*args)
        except Exception as ex:
            traceback.print_exc()
            mensagem(f"Erro: {ex}", erro=True)
        finally:
            builtins.input = original
        return retorno, buffer.getvalue().strip()

    # =============== ANIMAÇÃO DE ABERTURA ===============
    async def intro():
        estado["intro"] = True
        meio = (len(PALAVRA) - 1) / 2

        letras = [
            ft.Container(
                width=LARGURA_LETRA,
                alignment=ft.Alignment(0, 0),
                content=ft.Text(l, size=60, weight=ft.FontWeight.BOLD, color=BRANCO),
                opacity=0,
                offset=ft.Offset(0, 0.6),
                animate_opacity=ft.Animation(T_FADE, ft.AnimationCurve.EASE_OUT),
                animate_offset=ft.Animation(T_JUNTAR, ft.AnimationCurve.EASE_IN_OUT),
            )
            for l in PALAVRA
        ]

        linha = ft.Container(
            width=TAM,
            height=TAM,
            left=0,
            top=0,
            alignment=ft.Alignment(0, 0),
            content=ft.Row(letras, spacing=0, tight=True),
        )

        imagem = ft.Container(
            content=ft.Image(src="tatu.png", width=IMG_FINAL, height=IMG_FINAL),
            width=TAM,
            height=TAM,
            left=0,
            top=0,
            alignment=ft.Alignment(0, 0),
            opacity=0,
            scale=IMG_INICIAL / IMG_FINAL,
            animate_opacity=ft.Animation(T_GIRO // 2, ft.AnimationCurve.EASE_IN),
            animate_scale=ft.Animation(T_GIRO // 2, ft.AnimationCurve.EASE_OUT),
        )

        grupo = ft.Container(
            width=TAM,
            height=TAM,
            content=ft.Stack([imagem, linha], width=TAM, height=TAM),
            rotate=ft.Rotate(angle=0),
            opacity=1,
            animate_rotation=ft.Animation(T_GIRO, ft.AnimationCurve.EASE_IN_OUT),
            animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_IN),
        )

        def pular(e):
            estado["intro"] = False
            tela_login()

        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=grupo),
                    ft.Container(content=ft.TextButton("Pular", on_click=pular), padding=16),
                ],
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

        try:
            await asyncio.sleep(0.8)   # deixa a tela desenhar o estado inicial

            # 1) letras aparecem uma por uma
            for c in letras:
                if not estado["intro"]:
                    return
                c.opacity = 1
                c.offset = ft.Offset(0, 0)
                page.update()
                await asyncio.sleep(T_LETRA)

            # 2) letras se juntam no centro, uma sobre a outra
            await asyncio.sleep(0.3)
            if not estado["intro"]:
                return
            for i, c in enumerate(letras):
                c.offset = ft.Offset(meio - i, 0)
            page.update()
            await asyncio.sleep(T_JUNTAR / 1000 + 0.2)

            # 3) giro de 360 graus e o tatu (pequeno) aparece
            if not estado["intro"]:
                return
            grupo.rotate = ft.Rotate(angle=VOLTA)
            imagem.opacity = 1
            page.update()
            await asyncio.sleep(T_GIRO / 2000)

            # 4) letras somem e o tatu cresce enquanto o giro termina
            if not estado["intro"]:
                return
            for c in letras:
                c.opacity = 0
            imagem.scale = 1
            page.update()
            await asyncio.sleep(T_GIRO / 2000 + 0.5)

            # 5) tudo some e abre o login
            if not estado["intro"]:
                return
            grupo.opacity = 0
            page.update()
            await asyncio.sleep(0.7)
        except Exception:
            traceback.print_exc()

        if estado["intro"]:
            estado["intro"] = False
            tela_login()

    # =============== LOGIN ===============
    def tela_login():
        c_user = campo("Usuário")
        c_senha = campo("Senha", password=True, can_reveal_password=True)

        def entrar(e):
            if not c_user.value or not c_senha.value:
                mensagem("Preencha usuário e senha.", erro=True)
                return
            ok, texto = rodar_simples(entrar_conta, c_user.value, c_senha.value)
            if ok:
                estado["usuario"] = c_user.value
                tela_menu()
                mensagem(f"Bem-vindo, {c_user.value}!")
            else:
                mensagem(texto or "Usuário ou senha inválidos.", erro=True)

        def cadastrar(e):
            if not c_user.value or not c_senha.value:
                mensagem("Preencha usuário e senha.", erro=True)
                return
            _, texto = rodar_simples(cadastrar_conta, c_user.value, c_senha.value)
            mensagem(texto or "Conta criada! Agora é só entrar.")

        c_senha.on_submit = entrar

        montar(
            coluna(
                ft.Container(content=logo(110), alignment=ft.Alignment(0, 0)),
                card(
                    titulo("Entrar"),
                    c_user,
                    c_senha,
                    botao("Entrar na conta", entrar),
                    botao("Cadastrar conta", cadastrar, primario=False),
                ),
            )
        )

    def sair(e=None):
        estado["usuario"] = None
        tela_login()
        mensagem("Você saiu da conta.")

    # =============== MENU ===============
    def tela_menu():
        u = lambda: estado["usuario"]
        montar(
            coluna(
                ft.Text(f"Olá, {u()}", size=18, color=BRANCO, weight=ft.FontWeight.BOLD),
                tile(ft.Icons.ADD_CIRCLE_OUTLINE, "1 - Adicionar credencial",
                     "Cadastrar uma nova senha",
                     lambda: ir("Adicionar credencial", adicionar_credencial, u(),
                                log_acao="Credencial adicionada")),
                tile(ft.Icons.LOCK_OUTLINE, "2 - Ler credenciais",
                     "Ver tudo que você guardou",
                     lambda: ir("Credenciais", ler_credenciais, u())),
                tile(ft.Icons.EDIT_OUTLINED, "3 - Atualizar credencial",
                     "Editar uma credencial existente",
                     lambda: ir("Atualizar credencial", atualizar_credencial, u(),
                                log_acao="Credencial atualizada")),
                tile(ft.Icons.LABEL_OUTLINE, "4 - Consultar categorias",
                     "Ver as categorias cadastradas",
                     lambda: ir("Categorias", consultar_categorias)),
                tile(ft.Icons.NEW_LABEL_OUTLINED, "5 - Cadastrar categoria",
                     "Criar uma nova categoria", lambda: tela_nova_categoria()),
                tile(ft.Icons.DELETE_OUTLINE, "6 - Excluir credencial",
                     "Apagar uma credencial (pede confirmação)",
                     lambda: ir("Excluir credencial", excluir_credencial, u(),
                                log_acao="Credencial excluída",
                                confirmar="Deseja mesmo excluir esta credencial?")),
                tile(ft.Icons.SMART_TOY_OUTLINED, "7 - Falar com tatuAI",
                     "Pergunte sobre suas credenciais", lambda: tela_agente()),
                tile(ft.Icons.WARNING_AMBER, "Senhas repetidas",
                     "Verificar riscos nas suas senhas",
                     lambda: ir("Senhas repetidas", senhas_repetidas, u())),
                tile(ft.Icons.LOGOUT, "8 - Sair", "Encerrar a sessão", lambda: sair()),
            ),
            com_sair=True,
        )

    # =============== 5) CADASTRAR CATEGORIA ===============
    def tela_nova_categoria():
        nova = campo("Nome da nova categoria", autofocus=True)

        def cadastrar(e):
            nome = nova.value.strip().lower()
            if not nome:
                mensagem("Digite o nome da categoria.", erro=True)
                return
            ir("Cadastrar categoria", cadastrar_categoria, nome,
               log_acao="Categoria cadastrada")

        nova.on_submit = cadastrar
        montar(
            coluna(card(titulo("Cadastrar categoria"), nova, botao("Cadastrar", cadastrar))),
            voltar=True,
            com_sair=True,
        )

    # =============== 7) FALAR COM A tatuAI ===============
    def tela_agente():
        usuario = estado["usuario"]
        pergunta = campo("Digite sua pergunta", multiline=True, min_lines=2, max_lines=4)

        def enviar(e):
            if not pergunta.value.strip():
                mensagem("Digite uma pergunta para a tatuAI.", erro=True)
                return
            ir("tatuAI", falar_com_agente,
               nome_arquivo=arquivo_user(usuario),
               pergunta=pergunta.value,
               log_acao="Usuário falou com o agente")

        montar(
            coluna(card(titulo("tatuAI"), pergunta, botao("Enviar pergunta", enviar))),
            voltar=True,
            com_sair=True,
        )

    # ---------- Começa pela animação ----------
    page.run_task(intro)


ft.run(main, assets_dir="assets")
# 🔐 CofreSeguro — Gerenciador de Credenciais

Gerenciador de credenciais em Python, executado direto no terminal (CMD), que ajuda a **organizar**, **avaliar** e **monitorar** suas senhas.

## 📖 Sobre

Muitas pessoas utilizam a mesma senha em diversos serviços ou armazenam suas credenciais em locais inseguros. Isso dificulta identificar senhas fracas, repetidas e os riscos de possíveis vazamentos.

O **CofreSeguro** ajuda a organizar credenciais, avaliar a força das senhas e visualizar riscos de segurança, tudo por meio de um menu simples no terminal.

## ✨ Funcionalidades

- **CRUD completo de credenciais**: adicionar, ler, atualizar e excluir.
- **Categorias com força mínima de senha**: cada categoria exige um nível mínimo de segurança.
- **Cadastro de novas categorias**: crie categorias personalizadas e defina a força mínima.
- **Análise de força da senha** em 3 níveis (fraca, média e forte), validada no momento do cadastro.
- **Detecção de senhas repetidas**: após cada operação, o sistema avisa quantas senhas estão repetidas.
- **Senhas mascaradas** na listagem (apenas os 2 primeiros caracteres são exibidos).
- **Registro de data** do cadastro ou da última alteração de cada credencial.

## 🗂️ Categorias padrão

| Categoria       | Força mínima |
|-----------------|:------------:|
| `banco`         | 3 (forte)    |
| `estudos`       | 3 (forte)    |
| `trabalho`      | 2 (média)    |
| `redes sociais` | 2 (média)    |
| `outros`        | 1 (fraca)    |

Se você informar uma categoria que não existe, o programa pergunta se deseja cadastrá-la; caso responda que não, a credencial vai para `outros`.

## 💪 Níveis de força da senha

| Nível | Classificação | Critérios principais |
|:-----:|---------------|----------------------|
| 1 | Fraca | Mínimo de 6 caracteres |
| 2 | Média | 6+ caracteres com maiúscula, minúscula e número |
| 3 | Forte | Tudo do nível 2 + caractere especial (`! @ # $ % & * - _ ? / + =`) |

## 🚀 Como executar

**Pré-requisitos:** [Python 3](https://www.python.org/downloads/) instalado. Não há dependências externas, apenas a biblioteca padrão.

```bash
# 1. Clone o repositório
git clone https://github.com/GabrielPNasc/Projeto-CofreSeguro-Gerenciador-de-Credenciais.git

# 2. Entre na pasta do projeto
cd Projeto-CofreSeguro-Gerenciador-de-Credenciais

# 3. Execute
python main.py
```

> O arquivo `credenciais.txt` é criado automaticamente na pasta onde o programa roda, a partir do primeiro cadastro.

## 🖥️ Menu

```
Menu:
------------------------------
1 - Adicionar credencial
2 - Ler credenciais
3 - Atualizar credencial
4 - Consultar categorias
5 - Cadastrar categoria
6 - Excluir credencial
7 - Sair
------------------------------
```

## 💾 Formato de armazenamento

As credenciais ficam em `credenciais.txt`, uma por linha, com os campos separados por `|`:

```
serviço|usuário_ou_email|senha|categoria|observações|data_cadastro|
```

Exemplo:

```
Nubank|pedro@gmail.com|Senha@123|banco|conta principal|11/07/2026|
```

## 📁 Estrutura do projeto

```
.
├── main.py          # Código principal da aplicação
├── README.md        # Documentação
├── log.txt          # Registro de alterações
└── .gitignore
```

## ⚠️ Avisos importantes

- As senhas são salvas em **texto puro** no `credenciais.txt`. Use o projeto para fins de estudo e **não armazene senhas reais** nele.
- Adicione `credenciais.txt` ao `.gitignore` para nunca enviá-lo ao GitHub.

## 🛣️ Próximos passos

- [ ] Criptografar as senhas armazenadas
- [ ] Proteger o acesso com uma senha mestra
- [ ] Mostrar quais serviços compartilham a mesma senha
- [ ] Gerador de senhas fortes
- [ ] Interface gráfica

## 👨‍💻 Autor

**Gabriel Nascimento** — [@GabrielPNasc](https://github.com/GabrielPNasc)

# Publicar o site — do VS Code ao ar livre

Guia passo a passo. Faça na ordem; cada bloco leva poucos minutos.

Você vai precisar de: **VS Code**, **Git** e uma **conta no GitHub** — que você
já tem.

---

## Antes de começar: confira se o Git está funcionando

No VS Code, abra o terminal (menu **Terminal → Novo Terminal**, ou `` Ctrl+` ``)
e digite:

```bash
git --version
```

Se aparecer algo como `git version 2.4x.x`, está tudo certo. Se der erro,
instale em <https://git-scm.com/download/win> e reabra o VS Code.

---

## Etapa 1 — Abrir o projeto no VS Code

1. Abra o VS Code.
2. **Arquivo → Abrir Pasta...**
3. Escolha `C:\Users\Thiago\projetos\correa-metalurgica`
4. Se aparecer "Deseja confiar nos autores?", clique em **Sim, confio**.

Você deve ver a árvore de arquivos à esquerda: `app`, `templates`, `static`,
`run.py`, `README.md`.

> **Dica:** instale a extensão **Python** (da Microsoft) se ainda não tiver.
> Ícone de blocos na barra esquerda → busque "Python" → Instalar.

---

## Etapa 2 — Dizer ao Git quem é você

Só na primeira vez, na vida. No terminal do VS Code:

```bash
git config --global user.name "Thiago"
git config --global user.email "seu-email@exemplo.com"
```

Use o **mesmo e-mail** da sua conta do GitHub.

---

## Etapa 3 — Transformar a pasta em um repositório

Ainda no terminal do VS Code, dentro da pasta do projeto:

```bash
git init
git add .
git commit -m "Site da Correa Metalurgica"
```

O que cada linha faz:

| Comando | O que faz |
|---|---|
| `git init` | Começa a rastrear mudanças nesta pasta |
| `git add .` | Marca todos os arquivos para serem salvos |
| `git commit -m "..."` | Salva uma "foto" do projeto, com um nome |

O arquivo `.gitignore` já cuida de **não** enviar o ambiente virtual (`.venv`),
suas senhas (`.env`) nem os orçamentos recebidos (`data/`).

---

## Etapa 4 — Criar o repositório no GitHub

1. Vá em <https://github.com/new>
2. **Repository name:** `correa-metalurgica`
3. Deixe em **Private** (só você vê o código; o site publicado continua aberto)
4. **NÃO** marque "Add a README", "Add .gitignore" nem "Choose a license" —
   o projeto já tem os dele
5. Clique em **Create repository**

Na tela seguinte, o GitHub mostra alguns comandos. Use estes, trocando
`SEU-USUARIO` pelo seu nome de usuário:

```bash
git remote add origin https://github.com/SEU-USUARIO/correa-metalurgica.git
git branch -M main
git push -u origin main
```

Vai abrir uma janela pedindo para entrar no GitHub — entre pelo navegador e
autorize. Terminou? Atualize a página do GitHub: seus arquivos estão lá.

---

## Etapa 5 — Publicar no Render (grátis)

O Render roda Python de verdade, então o site sobe do jeito que está.

1. Entre em <https://render.com> e clique em **Get Started** → **GitHub**
2. Autorize o Render a ver seus repositórios
3. No painel, clique em **New +** → **Web Service**
4. Escolha o repositório `correa-metalurgica`
5. O Render vai ler o arquivo `render.yaml` e preencher tudo sozinho:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free
6. Clique em **Create Web Service**

A primeira publicação leva de 3 a 5 minutos. Quando terminar, o endereço
aparece no topo da página, assim:

```
https://correa-metalurgica.onrender.com
```

Esse é o link que você manda para o Julimar.

---

## Etapa 6 — Como atualizar o site depois

Toda vez que mexer em alguma coisa (trocar um texto, subir uma foto nova):

```bash
git add .
git commit -m "Atualiza fotos do portfolio"
git push
```

O Render percebe sozinho e republica em poucos minutos. Não precisa fazer mais
nada.

No VS Code dá para fazer isso sem digitar: aba **Controle do Código-Fonte**
(o ícone de ramificação na barra esquerda) → escreva a mensagem → **Commit** →
**Sync Changes**.

---

## Duas coisas importantes sobre o plano grátis

**1. O site "dorme".** Depois de 15 minutos sem ninguém acessar, o Render
desliga o serviço. A próxima visita demora **uns 50 segundos** para carregar,
enquanto ele acorda. Depois fica rápido.

Isso importa na hora de mostrar ao Julimar: **abra o link uns 2 minutos antes**
de mandar para ele, para o site já estar acordado. Se for mandar por WhatsApp e
ele abrir depois, avise que a primeira vez demora um pouco.

**2. Os orçamentos recebidos não ficam guardados.** No plano grátis, o disco é
apagado a cada reinício. Os pedidos do formulário aparecem no log e somem.

Duas saídas:

- **O WhatsApp continua sendo o canal confiável** — ele não depende do servidor.
- **Ligue o aviso por e-mail:** no painel do Render, aba **Environment**,
  preencha `SITE_SMTP_HOST`, `SITE_SMTP_PORT`, `SITE_SMTP_USER`,
  `SITE_SMTP_PASSWORD` e `SITE_NOTIFY_TO`. Com Gmail, use
  `smtp.gmail.com` / `587` e uma **senha de app** (não a senha da conta):
  <https://myaccount.google.com/apppasswords>

---

## Se der problema

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `git push` pede senha e recusa | O GitHub não aceita mais senha comum | Entre pela janela do navegador que aparece |
| Render acusa erro no build | Falta alguma dependência | Abra a aba **Logs** no Render e me mande o texto do erro |
| O site abre sem estilo | Arquivos estáticos não subiram | Confira se a pasta `static/` foi enviada ao GitHub |
| Página em branco por muito tempo | O serviço está acordando | Espere 50 segundos e recarregue |

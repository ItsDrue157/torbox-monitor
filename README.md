# Torbox Monitor

Monitor Python executado continuamente em Docker. Ele consulta a API da Torbox a
cada 30 segundos, mantém o estado em SQLite e envia notificações quando o estado
de um download muda.

## Preparar um servidor Ubuntu

Este projeto usa apenas Docker Engine e a interface de linha de comando, sem o
Docker Desktop. Em Ubuntu 22.04, 24.04 ou 26.04, execute:

```bash
bash deploy/install-docker-ubuntu.sh
```

Se o usuário não tiver `sudo`, entre como `root` e informe qual usuário deverá
receber acesso ao Docker:

```bash
TARGET_USER=carlos bash deploy/install-docker-ubuntu.sh
```

O instalador adiciona o repositório oficial do Docker, instala Engine, CLI,
Compose, Buildx e Git e habilita o serviço no boot. Ao terminar, encerre e abra
novamente a sessão SSH para que seu usuário receba acesso ao Docker.

Se o servidor ainda não tiver uma cópia deste repositório, instale primeiro o
Git (`sudo apt update && sudo apt install -y git`), faça o clone e então rode o
instalador.

## Executar com Docker

Crie a configuração local sem publicar o token no Git:

```bash
cp .env.example .env
nano .env
```

Depois, construa e inicie o serviço:

```bash
docker compose up -d --build
docker compose logs -f --tail=100
```

O banco fica no volume persistente `torbox-data`. O contêiner tem limite de 256
MB de RAM, sem swap adicional, 0,5 CPU e no máximo 64 processos. Os logs também
são rotacionados para não consumirem o disco indefinidamente.

## Atualizar no servidor

```bash
git pull --ff-only
docker compose up -d --build
docker image prune -f
```

Para conferir o consumo:

```bash
docker stats torbox-monitor
```

## Git: pull e push

No servidor, configure apenas sua identidade de commit:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"
```

Use uma chave SSH para autenticação com GitHub, GitLab ou outro provedor. Nunca
adicione o arquivo `.env` ao repositório; ele contém o token da Torbox.

Crie uma chave no servidor, se ainda não houver uma:

```bash
ssh-keygen -t ed25519 -C "seu-email@exemplo.com"
cat ~/.ssh/id_ed25519.pub
```

Cadastre a chave pública exibida no seu provedor Git. Depois disso, remotos SSH
permitem tanto `git pull` quanto `git push`.

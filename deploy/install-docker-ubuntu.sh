#!/usr/bin/env bash
set -euo pipefail

if [[ ! -r /etc/os-release ]]; then
  echo "Nao foi possivel identificar o sistema operacional." >&2
  exit 1
fi

# shellcheck disable=SC1091
source /etc/os-release

if [[ "${ID:-}" != "ubuntu" ]]; then
  echo "Este instalador aceita Ubuntu; sistema detectado: ${ID:-desconhecido}." >&2
  exit 1
fi

if [[ "$EUID" -eq 0 ]]; then
  if [[ -z "${TARGET_USER:-}" ]]; then
    echo "Execute como: TARGET_USER=carlos bash $0" >&2
    exit 1
  fi
  ADMIN=()
  docker_user="$TARGET_USER"
else
  if ! command -v sudo >/dev/null || ! sudo -v; then
    echo "Este usuario nao possui acesso administrativo." >&2
    echo "Entre como root e execute: TARGET_USER=$USER bash $0" >&2
    exit 1
  fi
  ADMIN=(sudo)
  docker_user="$USER"
fi

"${ADMIN[@]}" apt-get update
"${ADMIN[@]}" apt-get install --yes ca-certificates curl git
"${ADMIN[@]}" install -m 0755 -d /etc/apt/keyrings
"${ADMIN[@]}" curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
"${ADMIN[@]}" chmod a+r /etc/apt/keyrings/docker.asc

architecture="$(dpkg --print-architecture)"
codename="${UBUNTU_CODENAME:-$VERSION_CODENAME}"

printf '%s\n' \
  'Types: deb' \
  'URIs: https://download.docker.com/linux/ubuntu' \
  "Suites: ${codename}" \
  'Components: stable' \
  "Architectures: ${architecture}" \
  'Signed-By: /etc/apt/keyrings/docker.asc' |
  "${ADMIN[@]}" tee /etc/apt/sources.list.d/docker.sources >/dev/null

"${ADMIN[@]}" apt-get update
"${ADMIN[@]}" apt-get install --yes \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin

"${ADMIN[@]}" systemctl enable --now docker
"${ADMIN[@]}" usermod -aG docker "$docker_user"

"${ADMIN[@]}" docker version
"${ADMIN[@]}" docker compose version
git --version

echo
echo "Instalacao concluida para $docker_user. Saia da sessao SSH e entre novamente."

#!/bin/bash
set -e

APP_NAME="appcar_cluster"
BASE_DIR="/opt/clusterqt"
RELEASES_DIR="$BASE_DIR/releases"
CURRENT_LINK="$BASE_DIR/current"
UPDATE_DIR="$BASE_DIR/update"
REPO="SEAME-pt/Team5_Senna_Tech"

mkdir -p "$RELEASES_DIR" "$UPDATE_DIR"

# Verifica se já existe versão atual
if [ -L "$CURRENT_LINK" ]; then
    CURRENT_VERSION=$(basename "$(readlink "$CURRENT_LINK")")
else
    CURRENT_VERSION=""
fi

# Obtém última versão do GitHub
LATEST_VERSION=$(curl -s \
  https://api.github.com/repos/$REPO/releases/latest \
  | grep '"tag_name"' | cut -d '"' -f4)

if [ -z "$LATEST_VERSION" ]; then
    echo "Erro: Não foi possível obter a última versão do GitHub."
    exit 1
fi

# Se já estiver atualizado
if [ -n "$CURRENT_VERSION" ] && [ "$CURRENT_VERSION" = "$LATEST_VERSION" ]; then
    echo "ClusterQT already up to date ($CURRENT_VERSION)"
    exit 0
fi

echo "Installing version: $LATEST_VERSION"

TMP=$(mktemp -d)
cd "$TMP"

# Baixa release
curl -LO "https://github.com/$REPO/releases/download/$LATEST_VERSION/appcar_cluster.tar.gz"
curl -LO "https://github.com/$REPO/releases/download/$LATEST_VERSION/appcar_cluster.tar.gz.sha256"

# Verifica hash
sha256sum -c appcar_cluster.tar.gz.sha256

# Extrai para releases
mkdir -p "$RELEASES_DIR/$LATEST_VERSION"
tar -xzf appcar_cluster.tar.gz -C "$RELEASES_DIR/$LATEST_VERSION"

# Remove current antigo (diretório ou symlink)
if [ -e "$CURRENT_LINK" ] || [ -L "$CURRENT_LINK" ]; then
    rm -rf "$CURRENT_LINK"
fi

# Cria novo symlink
ln -s "$RELEASES_DIR/$LATEST_VERSION" "$CURRENT_LINK"

#systemctl restart clusterqt

echo "ClusterQT updated to $LATEST_VERSION"

#!/bin/bash
set -e

APP_NAME="appcar_cluster"
BASE_DIR="/opt/clusterqt"
RELEASES_DIR="$BASE_DIR/releases"
CURRENT_LINK="$BASE_DIR/current"
UPDATE_DIR="$BASE_DIR/update"
REPO="SEAME-pt/Team5_Senna_Tech"

mkdir -p "$RELEASES_DIR" "$UPDATE_DIR"

CURRENT_VERSION=$(readlink "$CURRENT_LINK" | awk -F/ '{print $NF}')

LATEST_VERSION=$(curl -s \
  https://api.github.com/repos/$REPO/releases/latest \
  | grep '"tag_name"' | cut -d '"' -f4)

if [ "$CURRENT_VERSION" = "$LATEST_VERSION" ]; then
  echo "ClusterQT already up to date ($CURRENT_VERSION)"
  exit 0
fi

TMP=$(mktemp -d)
cd "$TMP"

curl -LO \
  https://github.com/$REPO/releases/download/$LATEST_VERSION/appcar_cluster.tar.gz
curl -LO \
  https://github.com/$REPO/releases/download/$LATEST_VERSION/appcar_cluster.tar.gz.sha256

sha256sum -c appcar_cluster.tar.gz.sha256

mkdir "$RELEASES_DIR/$LATEST_VERSION"
tar -xzf appcar_cluster.tar.gz -C "$RELEASES_DIR/$LATEST_VERSION"

ln -sfnT "$RELEASES_DIR/$LATEST_VERSION" "$CURRENT_LINK"

#systemctl restart clusterqt

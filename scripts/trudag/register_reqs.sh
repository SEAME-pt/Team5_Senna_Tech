#!/bin/bash

# Pastas para processar
DIRS=("assertions" "assumptions" "evidences" "expectations")
BASE_DIR="reqs"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "=== Iniciando Registro Seguro no Trudag ==="

# === PASSO 0: LIMPEZA DO BANCO (OPCIONAL) ===
read -p "Deseja limpar e reconstruir o banco de dados (.dotstop.dot)? [y/N] " response
if [[ "$response" =~ ^[yY]$ ]]; then
    echo -e "🧹 Limpando banco de dados antigo..."
    rm -f .dotstop.dot
    trudag init
    echo -e "${GREEN}[OK] Banco limpo.${NC}"
else
    echo -e "⚠️  Mantendo banco atual. Itens novos serão adicionados/atualizados."
fi

validate_file() {
    local file=$1
    local content=$(cat "$file")

    # 1. Verifica Normative
    if ! grep -q "normative: true" "$file"; then
        echo -e "${RED}[ERRO] $file ausente 'normative: true'.${NC}"
        return 1
    fi

    # 2. Verifica Score vazio (Causa crash no Trudag)
    if grep -q "^score:[[:space:]]*$" "$file"; then
        echo -e "${RED}[ERRO] $file contem campo 'score:' vazio. Remova-o ou defina um valor.${NC}"
        return 1
    fi

    # 3. Verifica ID vazio
    if grep -q "^id:[[:space:]]*$" "$file"; then
        echo -e "${RED}[ERRO] $file contem campo 'id:' vazio.${NC}"
        return 1
    fi
    
    return 0
}

for dir in "${DIRS[@]}"; do
    TARGET_DIR="$BASE_DIR/$dir"
    
    if [ ! -d "$TARGET_DIR" ]; then
        echo "Pasta $TARGET_DIR não encontrada, pulando..."
        continue
    fi

    echo ""
    echo -e "📂 Processando: ${YELLOW}$TARGET_DIR${NC} (recursivo)"
    
    # Usa find para buscar recursivamente e tratar nomes com espacos corretamente
    find "$TARGET_DIR" -type f -name "*.md" | while read -r file; do
        # Ignora arquivos temporários
        if [[ "$file" == *".tmp" ]]; then continue; fi

        # === ESTÁGIO 1: VALIDAÇÃO ===
        if ! validate_file "$file"; then
            echo -e "${RED}Aborting process due to validation error in $file.${NC}"
            # O exit aqui sai do subshell do pipe, nao do script pai, mas serve para alertar
            exit 1 
        fi

        filename=$(basename -- "$file")
        dirname=$(dirname -- "$file") # Captura o diretório real do arquivo
        name_no_ext="${filename%.*}"
        
        # === ESTÁGIO 2: EXTRAÇÃO INTELIGENTE DE PREFIXO ===
        # Quebra no ÚLTIMO hífen para suportar nomes como EVD-201-1
        id="${name_no_ext##*-}"
        prefix="${name_no_ext%-*}"

        echo -n "   -> Registrando $name_no_ext... "

        # === ESTÁGIO 3: REGISTRO (COM BACKUP) ===
        cp "$file" "$file.tmp" # Faz backup
        
        rm "$file"
        # Usa $dirname para registrar no local correto
        trudag manage create-item "$prefix" "$id" "$dirname" > /dev/null 2>&1
        res=$?
        
        # Restaura imediatamente
        mv "$file.tmp" "$file"

        if [ $res -eq 0 ]; then
            echo -e "${GREEN}[OK]${NC}"
        else
            echo -e "${YELLOW}[JÁ EXISTE/WARN]${NC}"
        fi
    done
done

# === PASSO 4: LINKAGEM AUTOMÁTICA ===
./scripts/trudag/link_reqs.sh

echo ""
echo -e "${GREEN}=== Concluído! ===${NC}"
echo "Execute 'trudag score' ou 'trudag manage show-graph' para validar."

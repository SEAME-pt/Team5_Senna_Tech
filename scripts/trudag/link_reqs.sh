#!/bin/bash

# Pastas para processar
DIRS=("assertions" "assumptions" "evidences" "expectations")
BASE_DIR="reqs"

# Cores
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "=== Iniciando Linkagem Automática dos Requisitos ==="

create_links_from_file() {
    local file=$1
    local child_id=$2 

    # 1. Link: Expectation (Pai) -> Assertion (Filho)
    # Procura por "related_expectation_id: VALOR"
    parent_exp=$(grep "^related_expectation_id:" "$file" | awk '{print $2}')
    # Remove espaços em branco extras e CRs (carriage returns) se houver
    parent_exp=$(echo "$parent_exp" | tr -d '\r')

    if [ ! -z "$parent_exp" ] && [ "$parent_exp" != "EXP-XXX" ]; then
        echo -n "   🔗 Linkando $parent_exp -> $child_id ... "
        trudag manage create-link "$parent_exp" "$child_id" > /dev/null 2>&1
        if [ $? -eq 0 ]; then 
            echo -e "${GREEN}[OK]${NC}"
        else 
            echo -e "\033[0;31m[ERRO] (Verifique se $parent_exp existe)${NC}"
        fi
    fi

    # 2. Link: Assertion (Pai) -> Evidence/Assumption (Filho)
    # Procura por "related_assertion_id: VALOR"
    parent_ast=$(grep "^related_assertion_id:" "$file" | awk '{print $2}')
    parent_ast=$(echo "$parent_ast" | tr -d '\r')

    if [ ! -z "$parent_ast" ] && [ "$parent_ast" != "AST-XXX" ]; then
        echo -n "   🔗 Linkando $parent_ast -> $child_id ... "
        trudag manage create-link "$parent_ast" "$child_id" > /dev/null 2>&1
        if [ $? -eq 0 ]; then 
            echo -e "${GREEN}[OK]${NC}"
        else 
            echo -e "\033[0;31m[ERRO] (Verifique se $parent_ast existe)${NC}"
        fi
    fi
}

for dir in "${DIRS[@]}"; do
    TARGET_DIR="$BASE_DIR/$dir"
    if [ ! -d "$TARGET_DIR" ]; then continue; fi
    
    echo ""
    echo -e "📂 Verificando links em: ${GREEN}$TARGET_DIR${NC}"
    
    find "$TARGET_DIR" -type f -name "*.md" | while read -r file; do
        if [[ "$file" == *".tmp" ]]; then continue; fi
        
        filename=$(basename -- "$file")
        name_no_ext="${filename%.*}"
        
        # O ID do item é o nome do arquivo (ex: AST-201)
        full_id="$name_no_ext" 

        create_links_from_file "$file" "$full_id"
    done
done

echo ""
echo -e "${GREEN}=== Linkagem Concluída! ===${NC}"

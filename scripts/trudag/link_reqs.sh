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
    # Procura por "related_expectation_id: VALOR1, VALOR2..."
    parents_exp=$(grep "^related_expectation_id:" "$file" | cut -d':' -f2 | tr -d ' \r')

    if [ ! -z "$parents_exp" ] && [ "$parents_exp" != "EXP-XXX" ]; then
        IFS=',' read -ra ADDR <<< "$parents_exp"
        for parent in "${ADDR[@]}"; do
            echo -n "   🔗 Linkando $parent -> $child_id ... "
            trudag manage create-link "$parent" "$child_id" > /dev/null 2>&1
            if [ $? -eq 0 ]; then 
                echo -e "${GREEN}[OK]${NC}"
            else 
                echo -e "\033[0;31m[ERRO] (Verifique se $parent existe)${NC}"
            fi
        done
    fi

    # 2. Link: Assertion (Pai) -> Evidence/Assumption (Filho)
    # Procura por "related_assertion_id: VALOR1, VALOR2..."
    parents_ast=$(grep "^related_assertion_id:" "$file" | cut -d':' -f2 | tr -d ' \r')

    if [ ! -z "$parents_ast" ] && [ "$parents_ast" != "AST-XXX" ]; then
        IFS=',' read -ra ADDR <<< "$parents_ast"
        for parent in "${ADDR[@]}"; do
            echo -n "   🔗 Linkando $parent -> $child_id ... "
            trudag manage create-link "$parent" "$child_id" > /dev/null 2>&1
            if [ $? -eq 0 ]; then 
                echo -e "${GREEN}[OK]${NC}"
            else 
                echo -e "\033[0;31m[ERRO] (Verifique se $parent existe)${NC}"
            fi
        done
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

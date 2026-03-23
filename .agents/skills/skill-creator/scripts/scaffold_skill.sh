#!/bin/bash

# scaffold_skill.sh - Crea la estructura de una nueva skill
# Uso: ./scaffold_skill.sh <nombre_skill>

NAME="$1"

if [ -z "$NAME" ]; then
    echo "Error: Se requiere el nombre de la skill"
    echo "Uso: $0 <nombre_skill>"
    exit 1
fi

SKILL_PATH=".agents/skills/$NAME"

if [ -d "$SKILL_PATH" ]; then
    echo "Error: La habilidad '$NAME' ya existe en $SKILL_PATH"
    exit 1
fi

mkdir -p "$SKILL_PATH/scripts"
mkdir -p "$SKILL_PATH/examples"
mkdir -p "$SKILL_PATH/resources"

cat > "$SKILL_PATH/SKILL.md" << 'EOF'
---
name: NAME_PLACEHOLDER
description: Descripcion de la habilidad NAME_PLACEHOLDER.
---

# NAME_PLACEHOLDER

## Cuando usar esta habilidad
- 

## Como usarla
- 
EOF

sed -i "s/NAME_PLACEHOLDER/$NAME/g" "$SKILL_PATH/SKILL.md"

echo "Estructura de la habilidad '$NAME' creada exitosamente en $SKILL_PATH"
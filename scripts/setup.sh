#!/bin/bash
set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              OpenNemesis Setup Script                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Create virtual environment if not exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}→ Creando entorno virtual...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}✓ Entorno virtual creado${NC}"
else
    echo -e "${GREEN}✓ Entorno virtual ya existe${NC}"
fi

# Activate venv
source .venv/bin/activate

# 2. Install dependencies
echo -e "${YELLOW}→ Instalando dependencias...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencias instaladas${NC}"

# 3. Copy GOG binary if exists in /opt/gog
if [ -f "/opt/gog" ]; then
    echo -e "${YELLOW}→ Copiando binario GOG...${NC}"
    mkdir -p bin
    cp /opt/gog bin/gog
    chmod +x bin/gog
    echo -e "${GREEN}✓ GOG copiado a bin/gog${NC}"
else
    if [ ! -f "bin/gog" ]; then
        echo -e "${YELLOW}⚠ GOG no encontrado. Copia /opt/gog a bin/gog manualmente${NC}"
    else
        echo -e "${GREEN}✓ GOG ya existe en bin/gog${NC}"
    fi
fi

# 4. Copy .env.local to .env if not exists
if [ ! -f ".env" ]; then
    if [ -f ".env.local" ]; then
        echo -e "${YELLOW}→ Copiando .env.local a .env...${NC}"
        cp .env.local .env
        echo -e "${GREEN}✓ .env creado${NC}"
    else
        echo -e "${YELLOW}⚠ .env.local no encontrado. Crea uno manualmente.${NC}"
    fi
else
    echo -e "${GREEN}✓ .env ya existe${NC}"
fi

# 5. Initialize database (optional - already done on bot start)
if [ -f "data/db.py" ]; then
    echo -e "${YELLOW}→ Inicializando base de datos...${NC}"
    python -c "from data.db import init_db; init_db()" 2>/dev/null || true
    echo -e "${GREEN}✓ Base de datos inicializada${NC}"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  Setup completado. Ejecuta:                              ║"
echo "║                                                            ║"
echo "║    python main.py        → Validar conexiones            ║"
echo "║    python main.py run   → Iniciar bot                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"

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

# 3. Verify GOG binary
if [ -f "bin/gogcli/gog" ]; then
    echo -e "${GREEN}✓ GOG encontrado en bin/gogcli/gog${NC}"
else
    echo -e "${YELLOW}⚠ GOG no encontrado en bin/gogcli/gog${NC}"
    echo -e "${YELLOW}  Descarga el binario desde: https://github.com/steipete/gogcli/releases${NC}"
    echo -e "${YELLOW}  Guárdalo en: bin/gogcli/gog${NC}"
fi

# 4. Copy .env.example to .env if not exists
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo -e "${YELLOW}→ Copiando .env.example a .env...${NC}"
        cp .env.example .env
        echo -e "${GREEN}✓ .env creado desde plantilla${NC}"
        echo -e "${YELLOW}⚠ IMPORTANTE: Edita .env con tus credenciales${NC}"
    else
        echo -e "${YELLOW}⚠ .env.example no encontrado. Créalo manualmente.${NC}"
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

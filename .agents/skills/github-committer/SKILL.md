---
name: github-committer
description: Estandariza la creación de commits en GitHub usando Conventional Commits, emojis representativos y un límite de 50 caracteres.
---

# GitHub Committer

Esta habilidad asegura que todos los commits en el repositorio sigan un estándar profesional, legible y consistente.

## Cuándo usar esta habilidad
- Siempre que necesites realizar un commit de cambios en Git.
- Al colaborar en proyectos que requieran mensajes de commit estructurados.

## Formato del Mensaje de Commit
El formato obligatorio es:
`:emoji: tipo(ámbito): descripción`

### Tipos y Emojis
| Tipo | Emoji | Descripción |
| :--- | :--- | :--- |
| **feat** | ✨ | Una nueva funcionalidad |
| **fix** | 🐛 | Una corrección de error |
| **docs** | 📝 | Cambios en la documentación |
| **style** | 🎨 | Cambios que no afectan al significado del código (espaciado, formato) |
| **refactor** | ♻️ | Cambio de código que ni corrige un error ni añade una funcionalidad |
| **test** | ✅ | Añadir o corregir pruebas |
| **chore** | 🔧 | Cambios en el proceso de construcción o herramientas auxiliares |

### Reglas Críticas
1. **Longitud**: La descripción (después del tipo y ámbito) no debe exceder los **50 caracteres**.
2. **Imperativo**: Usa el tiempo imperativo en la descripción (ej: "añadir botón" en lugar de "añadido botón").
3. **Emojis**: El emoji debe ser el primer carácter del mensaje.

## Ejemplo Correcto
`✨ feat(ui): añadir botón de guardado rápido`

## Herramientas

### Linux/Mac
```bash
# Hacer ejecutable
chmod +x .agents/skills/github-committer/scripts/git-commit-helper.sh

# Modo interactivo
.agents/skills/github-committer/scripts/git-commit-helper.sh

# Con argumentos: tipo ámbito mensaje
.agents/skills/github-committer/scripts/git-commit-helper.sh feat ui "añadir botón"
```

### Windows (PowerShell)
```powershell
# Ejecutar
.agents/skills/github-committer/scripts/git-commit-helper.ps1

# Con argumentos
.agents/skills/github-committer/scripts/git-commit-helper.ps1 -Type feat -Scope ui -Message "añadir botón"
```

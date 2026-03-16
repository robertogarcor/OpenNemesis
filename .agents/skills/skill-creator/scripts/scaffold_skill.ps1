param (
    [Parameter(Mandatory=$true)]
    [string]$Name
)

$SkillPath = ".agents/skills/$Name"
$Metadata = @"
---
name: $Name
description: Descripcion de la habilidad $Name.
---

# $Name

## Cuando usar esta habilidad
- 

## Como usarla
- 
"@

if (Test-Path $SkillPath) {
    Write-Error "La habilidad '$Name' ya existe en $SkillPath"
    return
}

New-Item -ItemType Directory -Path $SkillPath -Force | Out-Null
New-Item -ItemType Directory -Path "$SkillPath/scripts" -Force | Out-Null
New-Item -ItemType Directory -Path "$SkillPath/examples" -Force | Out-Null
New-Item -ItemType Directory -Path "$SkillPath/resources" -Force | Out-Null

Set-Content -Path "$SkillPath/SKILL.md" -Value $Metadata -Encoding UTF8

Write-Host "Estructura de la habilidad '$Name' creada exitosamente en $SkillPath"

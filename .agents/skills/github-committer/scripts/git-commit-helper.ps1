param (
    [Parameter(Mandatory=$false)]
    [ValidateSet("feat", "fix", "docs", "style", "refactor", "test", "chore")]
    [string]$Type,

    [Parameter(Mandatory=$false)]
    [string]$Scope,

    [Parameter(Mandatory=$false)]
    [string]$Message
)

# Usamos códigos Unicode para evitar problemas de codificación en el archivo
$Emojis = @{
    "feat"     = [char]::ConvertFromUtf32(0x2728) # ✨
    "fix"      = [char]::ConvertFromUtf32(0x1F41B) # 🐛
    "docs"     = [char]::ConvertFromUtf32(0x1F4DD) # 📝
    "style"    = [char]::ConvertFromUtf32(0x1F3A8) # 🎨
    "refactor" = [char]::ConvertFromUtf32(0x267B) + [char]::ConvertFromUtf32(0xFE0F) # ♻️
    "test"     = [char]::ConvertFromUtf32(0x2705) # ✅
    "chore"    = [char]::ConvertFromUtf32(0x1F527) # 🔧
}

if (-not $Type) {
    Write-Host "Seleccione el tipo de commit:"
    $i = 1
    $typesArr = $Emojis.Keys | Sort-Object
    foreach ($t in $typesArr) {
        Write-Host "$i) $t $($Emojis[$t])"
        $i++
    }
    $choice = Read-Host "Opción"
    $Type = $typesArr[$choice - 1]
}

if (-not $Scope) {
    $Scope = Read-Host "Indique el ámbito (opcional, ej: ui, core, deps)"
}

if (-not $Message) {
    $Message = Read-Host "Escriba la descripción (máx 50 caracteres)"
}

if ($Message.Length -gt 50) {
    Write-Error "La descripción es demasiado larga ($($Message.Length) caracteres). Máximo 50."
    return
}

$Emoji = $Emojis[$Type]
$FinalMessage = "$Emoji $Type"
if ($Scope) { $FinalMessage += "($Scope)" }
$FinalMessage += ": $Message"

Write-Host "`nCommit sugerido:" -ForegroundColor Green
Write-Host $FinalMessage -ForegroundColor Cyan
Write-Host "`nComando git sugerido:" -ForegroundColor Gray
Write-Host "git commit -m `"$FinalMessage`""

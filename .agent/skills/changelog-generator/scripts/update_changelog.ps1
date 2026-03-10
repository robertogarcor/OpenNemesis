param (
    [string]$ChangelogFile = "CHANGELOG.md"
)

# Force UTF-8 encoding for input and output
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Get all commits in reverse chronological order
$commits = git log --pretty=format:"%h|%ad|%s" --date=short

if ($null -eq $commits) {
    Write-Host "No commits found."
    return
}

$changelogContent = "# Changelog`n`n"
$currentDate = ""

foreach ($line in $commits) {
    $parts = $line.Split("|")
    if ($parts.Length -ge 3) {
        $hash = $parts[0]
        $date = $parts[1]
        $subject = $parts[2]

        if ($date -ne $currentDate) {
            $changelogContent += "## [$date]`n"
            $currentDate = $date
        }
        $changelogContent += "- $subject ($hash)`n"
    }
}

Set-Content -Path $ChangelogFile -Value $changelogContent -Encoding UTF8
Write-Host "Updated $ChangelogFile with $(($commits | Measure-Object).Count) commits."

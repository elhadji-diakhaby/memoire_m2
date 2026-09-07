param(
    [string]$ProjectPath = "",
    [string]$RepoUrl = "",
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
if (-not $ProjectPath) { $ProjectPath = Read-Host "Chemin complet du dossier github_ready_vatencul_lidar" }
if (-not $RepoUrl) { $RepoUrl = Read-Host "URL du dépôt GitHub (ex. https://github.com/UTILISATEUR/DEPOT.git)" }
if (-not (Test-Path -LiteralPath $ProjectPath -PathType Container)) { throw "Dossier introuvable : $ProjectPath" }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "Git n'est pas installé : https://git-scm.com/download/win" }

Set-Location -LiteralPath $ProjectPath
$large = Get-ChildItem -Recurse -File | Where-Object { $_.Length -ge 100MB }
if ($large) { $large | ForEach-Object { Write-Host "Fichier >=100 Mio : $($_.FullName)" }; throw "GitHub refuse les fichiers de 100 Mio ou plus." }
if (-not (Test-Path .git)) { git init }
if (-not (git config user.name)) { git config user.name (Read-Host "Nom à associer aux commits") }
if (-not (git config user.email)) { git config user.email (Read-Host "E-mail à associer aux commits") }
git branch -M $Branch
git add --all
$pending = git status --porcelain
if ($pending) { git commit -m "Publication initiale du mémoire LiDAR Vatencul" } else { Write-Host "Aucune modification à valider." }
if ((git remote) -contains "origin") { git remote set-url origin $RepoUrl } else { git remote add origin $RepoUrl }
git push -u origin $Branch
Write-Host "Import terminé : $RepoUrl"

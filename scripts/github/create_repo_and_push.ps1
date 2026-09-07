param(
    [string]$ProjectPath = "",
    [string]$RepoName = "",
    [ValidateSet("public", "private")][string]$Visibility = "public"
)

$ErrorActionPreference = "Stop"
if (-not $ProjectPath) { $ProjectPath = Read-Host "Chemin complet du dossier github_ready_vatencul_lidar" }
if (-not $RepoName) { $RepoName = Read-Host "Nom GitHub UTILISATEUR/DEPOT" }
if (-not (Test-Path -LiteralPath $ProjectPath -PathType Container)) { throw "Dossier introuvable : $ProjectPath" }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "Installez Git : https://git-scm.com/download/win" }
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw "Installez GitHub CLI : https://cli.github.com/" }

gh auth status 2>$null
if ($LASTEXITCODE -ne 0) { gh auth login --web }
Set-Location -LiteralPath $ProjectPath
$large = Get-ChildItem -Recurse -File | Where-Object { $_.Length -ge 100MB }
if ($large) { throw "Un fichier atteint 100 Mio. Retirez-le ou utilisez Git LFS." }
if (-not (Test-Path .git)) { git init }
if (-not (git config user.name)) { git config user.name (Read-Host "Nom à associer aux commits") }
if (-not (git config user.email)) { git config user.email (Read-Host "E-mail à associer aux commits") }
git branch -M main
git add --all
$pending = git status --porcelain
if ($pending) { git commit -m "Publication initiale du mémoire LiDAR Vatencul" }
gh repo create $RepoName --$Visibility --source . --remote origin --push
Write-Host "Dépôt créé : https://github.com/$RepoName"

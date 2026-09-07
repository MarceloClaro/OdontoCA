# Push repository to GitHub via REST API
# This script uploads/updates all files in the local repository folder to the remote GitHub repository.
# It uses a Personal Access Token (PAT) with the 'repo' scope.
# IMPORTANT: Run this script in PowerShell.

$repoOwner = "MarceloClaro"
$repoName  = "OdontoCA"
$branch    = "main"

# Prompt for PAT (do NOT store it in the script)
$pat = Read-Host -Prompt "Enter your GitHub Personal Access Token (PAT)"
if (-not $pat) { Write-Error "PAT is required"; exit 1 }

# Base64-encoded auth header
$authHeader = "Bearer $pat"

# Helper to call GitHub API
function Invoke-GitHubApi {
    param(
        [string]$Method,
        [string]$Uri,
        $Body = $null
    )
    $headers = @{ Authorization = $authHeader; "User-Agent" = "PowerShell" }
    if ($Body) {
        $json = $Body | ConvertTo-Json -Depth 10
        Invoke-RestMethod -Method $Method -Uri $Uri -Headers $headers -Body $json -ContentType "application/json"
    } else {
        Invoke-RestMethod -Method $Method -Uri $Uri -Headers $headers
    }
}

# Get reference (SHA) of the target branch
$refUrl = "https://api.github.com/repos/$repoOwner/$repoName/git/refs/heads/$branch"
$ref = Invoke-GitHubApi -Method GET -Uri $refUrl
$baseSha = $ref.object.sha

# Create a new tree with all files in the current directory (recursively)
$repoRoot = Get-Location
$files = Get-ChildItem -Path $repoRoot -Recurse -File | Where-Object { $_.FullName -notmatch "\.git" }
$treeItems = @()
foreach ($file in $files) {
    $content = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Content -Raw -Path $file.FullName)))
    $blob = Invoke-GitHubApi -Method POST -Uri "https://api.github.com/repos/$repoOwner/$repoName/git/blobs" -Body @{ content = $content; encoding = "base64" }
    $relativePath = $file.FullName.Substring($repoRoot.Path.Length + 1).Replace("\\", "/")
    $treeItems += @{ path = $relativePath; mode = "100644"; type = "blob"; sha = $blob.sha }
}

# Create tree
$tree = Invoke-GitHubApi -Method POST -Uri "https://api.github.com/repos/$repoOwner/$repoName/git/trees" -Body @{ base_tree = $baseSha; tree = $treeItems }

# Create commit
$commitMessage = "Automated push via PowerShell script"
$commit = Invoke-GitHubApi -Method POST -Uri "https://api.github.com/repos/$repoOwner/$repoName/git/commits" -Body @{ message = $commitMessage; tree = $tree.sha; parents = @($baseSha) }

# Update reference to point to new commit
Invoke-GitHubApi -Method PATCH -Uri $refUrl -Body @{ sha = $commit.sha }

Write-Host "Push completed successfully. New commit SHA: $($commit.sha)"

# Fix Commit Author - Change AURA Bot to David Bhattarai
# This script will rewrite git history to change the author

Write-Host "🔧 Fixing Commit Author" -ForegroundColor Cyan
Write-Host "=" * 60

# Check current commits
Write-Host "`n📋 Current commits:" -ForegroundColor Yellow
git log --oneline -5

Write-Host "`n⚠️  WARNING: This will rewrite git history!" -ForegroundColor Red
Write-Host "This will change AURA Bot commits to David Bhattarai" -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "Do you want to continue? (yes/no)"

if ($confirm -ne "yes") {
    Write-Host "❌ Cancelled" -ForegroundColor Red
    exit
}

Write-Host "`n🔄 Rewriting git history..." -ForegroundColor Cyan

# Use git filter-branch to change author
$env:FILTER_BRANCH_SQUELCH_WARNING = "1"

git filter-branch --env-filter '
OLD_EMAIL="aurabot@mindbridge.com"
CORRECT_NAME="David Bhattarai"
CORRECT_EMAIL="davidbhattarai02@gmail.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags

Write-Host "`n✅ Git history rewritten!" -ForegroundColor Green

# Show updated commits
Write-Host "`n📋 Updated commits:" -ForegroundColor Yellow
git log --oneline -5

Write-Host "`n🚀 Now you need to force push:" -ForegroundColor Cyan
Write-Host "git push origin main --force" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  Note: Force push will overwrite remote history" -ForegroundColor Red
Write-Host ""

$push = Read-Host "Do you want to force push now? (yes/no)"

if ($push -eq "yes") {
    Write-Host "`n📤 Force pushing to origin..." -ForegroundColor Cyan
    git push origin main --force
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Successfully pushed! All commits now show David Bhattarai" -ForegroundColor Green
    } else {
        Write-Host "`n❌ Push failed. You may need to push manually:" -ForegroundColor Red
        Write-Host "git push origin main --force" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n💡 Run this command when ready:" -ForegroundColor Yellow
    Write-Host "git push origin main --force" -ForegroundColor Cyan
}

Write-Host "`n✅ Done!" -ForegroundColor Green

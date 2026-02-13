# Fix Single Commit (b9af3de) - Change author to David Bhattarai
Write-Host "🔧 Fixing Commit b9af3de Author" -ForegroundColor Cyan
Write-Host "=" * 60

Write-Host "`n📋 Current commits:" -ForegroundColor Yellow
git log --oneline -3

Write-Host "`n⚠️  This will change only b9af3de commit author" -ForegroundColor Yellow
Write-Host "Commit: 'Update Gemini AI integration'" -ForegroundColor Cyan
Write-Host "New Author: David Bhattarai <davidbhattarai02@gmail.com>" -ForegroundColor Green
Write-Host ""

$confirm = Read-Host "Continue? (yes/no)"

if ($confirm -ne "yes") {
    Write-Host "❌ Cancelled" -ForegroundColor Red
    exit
}

Write-Host "`n🔄 Changing commit author..." -ForegroundColor Cyan

# Use interactive rebase to edit the specific commit
$env:GIT_SEQUENCE_EDITOR = "sed -i '1s/^pick/edit/'"

# Start rebase
git rebase -i b9af3de~1

# Change the author
git commit --amend --author="David Bhattarai <davidbhattarai02@gmail.com>" --no-edit

# Continue rebase
git rebase --continue

Write-Host "`n✅ Commit author changed!" -ForegroundColor Green

Write-Host "`n📋 Updated commits:" -ForegroundColor Yellow
git log --oneline -3

Write-Host "`n🚀 Now push with:" -ForegroundColor Cyan
Write-Host "git push origin main --force" -ForegroundColor Yellow

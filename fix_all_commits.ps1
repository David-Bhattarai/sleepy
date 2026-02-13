# Fix All Commits - Change to David Bhattarai email
Write-Host "🔧 Fixing All Commits to David Bhattarai" -ForegroundColor Cyan
Write-Host "=" * 60

# Step 1: Reset to base commit
Write-Host "`n📍 Step 1: Reset to base commit (77369fc)" -ForegroundColor Yellow
git reset --hard 77369fc

# Step 2: Cherry-pick Gemini AI integration commit
Write-Host "`n📍 Step 2: Cherry-pick Gemini AI integration" -ForegroundColor Yellow
git cherry-pick b9af3de

# Step 3: Change author to David Bhattarai
Write-Host "`n📍 Step 3: Change author to David Bhattarai" -ForegroundColor Yellow
git commit --amend --author="David Bhattarai <davidbhattarai02@gmail.com>" --no-edit

# Step 4: Cherry-pick Remove unwanted files commit
Write-Host "`n📍 Step 4: Cherry-pick Remove unwanted files" -ForegroundColor Yellow
git cherry-pick aa83946

# Step 5: Show final commits
Write-Host "`n✅ Final commits:" -ForegroundColor Green
git log --oneline -3

Write-Host "`n🚀 Ready to push!" -ForegroundColor Cyan
Write-Host "Run: git push origin main --force" -ForegroundColor Yellow

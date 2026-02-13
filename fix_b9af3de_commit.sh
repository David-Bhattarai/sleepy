#!/bin/bash
# Fix b9af3de commit author to David Bhattarai

echo "🔧 Fixing commit b9af3de author"
echo "======================================"

# Use git filter-branch to change specific commit
git filter-branch --env-filter '
if [ "$GIT_COMMIT" = "b9af3de" ]; then
    export GIT_AUTHOR_NAME="David Bhattarai"
    export GIT_AUTHOR_EMAIL="davidbhattarai02@gmail.com"
    export GIT_COMMITTER_NAME="David Bhattarai"
    export GIT_COMMITTER_EMAIL="davidbhattarai02@gmail.com"
fi
' -- --all

echo ""
echo "✅ Commit author changed!"
echo ""
echo "📋 Updated commits:"
git log --oneline -3
echo ""
echo "🚀 Now run: git push origin main --force"

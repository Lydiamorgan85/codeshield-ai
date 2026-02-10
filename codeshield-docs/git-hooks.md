# Git Hooks Integration

Catch security vulnerabilities before they reach your repository using Git hooks and CodeShield AI.

## Pre-commit Hook

### Automatic Installation

```bash
# Install pre-commit hook
npx codeshield install-hooks
```

This creates `.git/hooks/pre-commit` that runs automatically before each commit.

### Manual Installation

Create `.git/hooks/pre-commit`:

```bash
#!/bin/sh

# Run CodeShield on staged files
npx codeshield analyze --staged --fail-on-critical

if [ $? -ne 0 ]; then
    echo "❌ Security vulnerabilities detected!"
    echo "Fix issues or use 'git commit --no-verify' to bypass"
    exit 1
fi

echo "✅ Security scan passed"
exit 0
```

Make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

## Pre-push Hook

Scan before pushing to remote:

Create `.git/hooks/pre-push`:

```bash
#!/bin/sh

echo "Running security scan before push..."

# Scan all files
npx codeshield analyze ./src --fail-on-critical

if [ $? -ne 0 ]; then
    echo "❌ Security issues found. Push blocked."
    exit 1
fi

echo "✅ Security scan passed. Proceeding with push."
exit 0
```

Make it executable:

```bash
chmod +x .git/hooks/pre-push
```

## Commit Message Hook

Require security scan reference in commit messages:

Create `.git/hooks/commit-msg`:

```bash
#!/bin/sh

# Run quick scan
SCAN_RESULT=$(npx codeshield analyze --staged --quiet)

if [ $? -ne 0 ]; then
    # Append scan warning to commit message
    echo "" >> "$1"
    echo "⚠️ WARNING: Security issues detected but not blocking commit" >> "$1"
    echo "Run 'npx codeshield analyze' for details" >> "$1"
fi

exit 0
```

## Husky Integration

### Installation

```bash
# Install Husky
npm install --save-dev husky

# Initialize Husky
npx husky init
```

### Configure Pre-commit

```bash
# Add pre-commit hook
npx husky add .husky/pre-commit "npx codeshield analyze --staged --fail-on-critical"
```

### Configure Pre-push

```bash
# Add pre-push hook
npx husky add .husky/pre-push "npx codeshield analyze ./src"
```

### package.json Configuration

```json
{
  "scripts": {
    "prepare": "husky install"
  },
  "devDependencies": {
    "husky": "^8.0.0"
  }
}
```

## Lint-staged Integration

Scan only changed files for faster commits.

### Installation

```bash
npm install --save-dev lint-staged
```

### Configuration

Add to `package.json`:

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "npx codeshield analyze --fail-on-critical"
    ],
    "*.py": [
      "npx codeshield analyze --language python --fail-on-critical"
    ]
  }
}
```

### Husky + Lint-staged

`.husky/pre-commit`:

```bash
#!/bin/sh
npx lint-staged
```

## Advanced Configurations

### Scan Only Modified Lines

```bash
#!/bin/sh

# Get modified files
MODIFIED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$MODIFIED_FILES" ]; then
    exit 0
fi

# Scan only modified files
echo "$MODIFIED_FILES" | xargs npx codeshield analyze --fail-on-critical
```

### Progressive Scanning

Increase strictness based on branch:

```bash
#!/bin/sh

BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    # Strictest for main branch
    npx codeshield analyze --severity critical,high,medium --fail-on-any
elif [ "$BRANCH" = "develop" ]; then
    # Medium strictness for develop
    npx codeshield analyze --fail-on-critical,high
else
    # Lenient for feature branches
    npx codeshield analyze --fail-on-critical
fi
```

### Skip Hook When Needed

```bash
# Bypass pre-commit hook
git commit --no-verify -m "Emergency fix"

# Or set environment variable
SKIP_CODESHIELD=1 git commit -m "Skip security scan"
```

Update hook to respect flag:

```bash
#!/bin/sh

if [ "$SKIP_CODESHIELD" = "1" ]; then
    echo "⚠️ Skipping security scan"
    exit 0
fi

npx codeshield analyze --staged --fail-on-critical
```

## Team Configuration

### Shared Hooks via Repository

Store hooks in repo for team consistency:

```bash
# Create hooks directory
mkdir -p .githooks

# Create shared pre-commit
cat > .githooks/pre-commit << 'EOF'
#!/bin/sh
npx codeshield analyze --staged --fail-on-critical
EOF

chmod +x .githooks/pre-commit
```

Configure Git to use repo hooks:

```bash
git config core.hooksPath .githooks
```

Add to README:

```markdown
## Setup
After cloning, run:
\`\`\`bash
git config core.hooksPath .githooks
\`\`\`
```

### Automated Setup Script

Create `scripts/setup-hooks.sh`:

```bash
#!/bin/bash

echo "Setting up CodeShield git hooks..."

# Configure hooks path
git config core.hooksPath .githooks

# Make hooks executable
chmod +x .githooks/*

echo "✅ Git hooks configured successfully"
```

## CI/CD Fallback

Ensure CI catches what hooks miss:

```yaml
# .github/workflows/security.yml
name: Security Fallback

on:
  push:
    branches: [ main, develop ]

jobs:
  security-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Full Security Scan
        run: npx codeshield analyze ./src --fail-on-critical
        
      - name: Comment on PR if issues found
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '⚠️ Security issues detected! Please run local security scan.'
            })
```

## Notification on Bypass

Alert team when hooks are bypassed:

```bash
#!/bin/sh

# In pre-commit hook
LOG_FILE=".git/hooks-bypassed.log"

if [ -f "$LOG_FILE" ]; then
    # Send notification (Slack, email, etc.)
    curl -X POST https://hooks.slack.com/... \
         -d "{\"text\":\"Security hook bypassed by $(git config user.name)\"}"
fi
```

## Performance Optimization

### Cache Scan Results

```bash
#!/bin/sh

CACHE_FILE=".git/codeshield-cache"
CURRENT_HASH=$(git diff --cached | sha256sum)

if [ -f "$CACHE_FILE" ]; then
    CACHED_HASH=$(cat "$CACHE_FILE")
    if [ "$CURRENT_HASH" = "$CACHED_HASH" ]; then
        echo "✅ Using cached scan result"
        exit 0
    fi
fi

# Run scan
npx codeshield analyze --staged

if [ $? -eq 0 ]; then
    echo "$CURRENT_HASH" > "$CACHE_FILE"
fi
```

### Parallel Scanning

```bash
#!/bin/sh

# Scan different file types in parallel
npx codeshield analyze "**/*.js" &
PID1=$!

npx codeshield analyze "**/*.py" &
PID2=$!

# Wait for all scans
wait $PID1
RESULT1=$?

wait $PID2
RESULT2=$?

if [ $RESULT1 -ne 0 ] || [ $RESULT2 -ne 0 ]; then
    exit 1
fi
```

## Troubleshooting

### Hook Not Running

```bash
# Check if hooks are executable
ls -la .git/hooks/

# Make executable
chmod +x .git/hooks/pre-commit
```

### Wrong Node Version

```bash
# Use nvm in hook
#!/bin/sh
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 18

npx codeshield analyze --staged
```

### Slow Commits

```bash
# Scan only staged files
npx codeshield analyze --staged

# Or use cache
npx codeshield analyze --cached
```

## Best Practices

1. **Use pre-commit for fast feedback** - Catch issues early
2. **Use pre-push as safety net** - Double-check before sharing
3. **Keep scans fast** - Only scan changed files
4. **Provide bypass option** - For emergencies
5. **Log bypasses** - Track when security is skipped
6. **Educate team** - Explain why hooks exist
7. **Keep hooks in repo** - Ensure consistency

## Examples

### Minimal Pre-commit

```bash
#!/bin/sh
npx codeshield analyze --staged --fail-on-critical || exit 1
```

### Full-featured Pre-commit

```bash
#!/bin/sh

echo "🔒 Running CodeShield security scan..."

# Respect bypass flag
if [ "$SKIP_CODESHIELD" = "1" ]; then
    echo "⚠️ Security scan skipped"
    exit 0
fi

# Run scan
npx codeshield analyze --staged --output .git/last-scan.json

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Security vulnerabilities detected!"
    echo "   Review: cat .git/last-scan.json"
    echo "   Bypass: SKIP_CODESHIELD=1 git commit"
    exit 1
fi

echo "✅ Security scan passed"
exit 0
```

## Support

Issues with Git hooks?
- Check [Troubleshooting Guide](troubleshooting.md)
- Open an issue on GitHub
- Email: lydiamorgan000@gmail.com

# Quick Security Checklist

## ⚠️ URGENT: Token Exposed in PR #33

### Immediate Actions (Do This Now!)

1. [ ] Go to https://github.com/settings/tokens
2. [ ] Revoke/delete the exposed token
3. [ ] Edit or close PR #33 to remove token from description
4. [ ] Check audit logs at: Settings → Security → Audit log
5. [ ] Enable secret scanning: Settings → Code security and analysis

### Token Recovery Steps

```bash
# 1. List your tokens (via GitHub UI)
Visit: https://github.com/settings/tokens

# 2. Revoke the compromised token
# Click "Delete" next to the token

# 3. Create a new token (if needed)
# Use fine-grained tokens with minimal scopes
# Set expiration date (90 days recommended)

# 4. Update your local environment
export GITHUB_TOKEN="new_token_here"
# Or add to .env file (which is gitignored)
```

### Verify Security Settings

```bash
# 1. Check what's in .gitignore
cat .gitignore | grep -A 5 "Security"

# 2. Ensure .env is not tracked
git check-ignore .env
# Should output: .env

# 3. Check for any secrets in git history
git log --all --oneline | grep -i "token\|secret\|key"
```

### Enable GitHub Security Features

Repository Settings → Code security and analysis:
- [x] Dependency graph
- [x] Dependabot alerts  
- [x] Dependabot security updates
- [x] Secret scanning
- [x] Push protection

### Using Tokens Securely

```python
# ✅ GOOD: Use environment variables
import os
api_key = os.environ.get("API_KEY")

# ❌ BAD: Never hard-code
# api_key = "ghp_abc123..."
```

```bash
# ✅ GOOD: Use .env file (gitignored)
echo "GITHUB_TOKEN=your_token" >> .env

# ✅ GOOD: Use GitHub Secrets for Actions
# Settings → Secrets → New repository secret
```

### Pre-commit Secret Detection (Optional but Recommended)

```bash
# Install detect-secrets
pip install detect-secrets

# Scan for secrets
detect-secrets scan

# Set up pre-commit hook
pip install pre-commit
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
EOF
pre-commit install
```

### Files to Review

- `SECURITY_INCIDENT_REPORT.md` - Full incident details
- `.github/SECURITY.md` - Complete security policy
- `SECURITY_ALERT.md` - Overview of the issue
- `.env.example` - Environment variable template

### Still Stuck?

1. See full guides in the files above
2. GitHub docs: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure
3. Contact repository maintainers

---

**Remember:** The exposed token in PR #33 must be revoked ASAP!

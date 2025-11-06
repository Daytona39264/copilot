# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this repository, please report it by:

1. **DO NOT** create a public issue
2. Email the repository maintainers directly
3. Or use GitHub's private security advisory feature:
   - Go to the Security tab
   - Click "Report a vulnerability"
   - Provide detailed information

## Secure Development Practices

### Managing Secrets and Tokens

#### ❌ NEVER Do This
- Commit tokens, API keys, or passwords to the repository
- Include secrets in PR descriptions or issue comments
- Share credentials via chat, email, or public channels
- Hard-code sensitive values in source code

#### ✅ ALWAYS Do This
- Use environment variables for sensitive configuration
- Store secrets in GitHub Secrets for CI/CD workflows
- Use `.env` files (and add them to `.gitignore`)
- Rotate tokens and credentials regularly
- Use minimal scopes/permissions for tokens
- Set expiration dates on tokens

### Example: Secure Configuration

```python
import os
from pathlib import Path

# ✅ CORRECT: Load from environment
API_KEY = os.environ.get("API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")

# ❌ WRONG: Never hard-code secrets
# API_KEY = "ghp_abc123def456..."
# DATABASE_URL = "postgresql://user:pass@host/db"
```

### Using .env Files Securely

Create a `.env.example` file to document required variables:
```env
# .env.example - Safe to commit
ANTHROPIC_API_KEY=your_api_key_here
GITHUB_TOKEN=your_github_token_here
DATABASE_URL=postgresql://localhost/mydb
```

Create actual `.env` file (never commit this):
```env
# .env - Add to .gitignore
ANTHROPIC_API_KEY=sk-ant-actual-key-here
GITHUB_TOKEN=ghp_actual_token_here
DATABASE_URL=postgresql://user:pass@host/db
```

Ensure `.gitignore` includes:
```gitignore
.env
.env.local
.env.*.local
*.key
*.token
secrets.*
credentials.*
```

### GitHub Personal Access Tokens

When creating GitHub tokens:

1. **Use Fine-Grained Tokens** (recommended)
   - Go to: Settings → Developer settings → Personal access tokens → Fine-grained tokens
   - Select specific repositories
   - Choose minimal permissions needed
   - Set expiration (max 90 days recommended)

2. **Classic Tokens** (legacy)
   - Only if fine-grained tokens don't meet your needs
   - Select minimal scopes required
   - Set expiration date

3. **Store Securely**
   ```bash
   # Use environment variable
   export GITHUB_TOKEN="ghp_yourtoken"
   
   # Or GitHub CLI
   gh auth login
   
   # For scripts, use credential manager
   # macOS: Keychain Access
   # Linux: gnome-keyring, pass, or similar
   # Windows: Windows Credential Manager
   ```

### Pre-commit Hooks for Secret Detection

Install and configure detect-secrets:

```bash
# Install
pip install detect-secrets

# Initialize
detect-secrets scan --baseline .secrets.baseline

# Add to .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### GitHub Secret Scanning

Enable built-in security features:

1. **Navigate to:** Repository Settings → Code security and analysis

2. **Enable:**
   - ✅ Dependency graph
   - ✅ Dependabot alerts
   - ✅ Dependabot security updates
   - ✅ Secret scanning
   - ✅ Push protection (prevents pushing secrets)

3. **Configure custom patterns** if needed for project-specific secrets

### CI/CD Security

For GitHub Actions:

```yaml
# .github/workflows/example.yml
name: Example Workflow

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # ✅ CORRECT: Use GitHub Secrets
      - name: Run with secrets
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: |
          # Your commands here
          echo "API_KEY is set: ${API_KEY:+yes}"
      
      # ❌ WRONG: Never echo secrets
      # - run: echo "${{ secrets.API_KEY }}"
```

### Dependency Security

1. **Keep dependencies updated**
   ```bash
   # Python
   pip install --upgrade pip
   pip list --outdated
   
   # Or use Dependabot (enabled by default)
   ```

2. **Review dependency vulnerabilities**
   ```bash
   # Check for known vulnerabilities
   pip install safety
   safety check
   ```

3. **Use lock files**
   - `requirements.txt` with pinned versions
   - Or use `poetry.lock`, `Pipfile.lock`

### Code Review Checklist

Before merging any PR:

- [ ] No secrets or tokens in code
- [ ] No secrets in commit messages
- [ ] No secrets in PR description
- [ ] Dependencies are up to date
- [ ] No hardcoded credentials
- [ ] Environment variables used correctly
- [ ] .gitignore is comprehensive

## Incident Response

If a secret is accidentally exposed:

1. **Immediately revoke/rotate** the compromised credential
2. **Review audit logs** for unauthorized access
3. **Notify the security team**
4. **Remove the secret** from Git history if committed:
   ```bash
   # Use BFG Repo-Cleaner or git-filter-repo
   # WARNING: This rewrites history
   git filter-repo --invert-paths --path-glob '**/*secret*'
   ```
5. **Document the incident**
6. **Review and improve** security practices

## Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security/getting-started/github-security-features)
- [Secret Scanning Documentation](https://docs.github.com/en/code-security/secret-scanning)
- [Securing Your Workflows](https://docs.github.com/en/actions/security-guides)

## Questions?

If you have questions about security practices for this repository, please contact the maintainers.

---

**Remember:** Security is everyone's responsibility. When in doubt, ask!

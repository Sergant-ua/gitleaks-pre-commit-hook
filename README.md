# gitleaks-pre-commit-hook

## Getting Started

### Requirements
  1. Python 3.8, 3.9, or 3.10, 3.11, 3.12.
  2. Add to .gitignore leaks-report.json

### Installing

Copy pre-commit.py file to {your repo}.git/hooks/pre-commit

### Enable/Disable Gitleaks
```
git config hooks.gitleaks.enable true  # Enable
git config hooks.gitleaks.enable false # Disable
```


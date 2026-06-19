# Contributing Guide

This document defines the Git workflow, branch naming conventions, commit standards, and pull request requirements for the Ecommerce API project.

---

# Branching Model

The project follows a three-level branching strategy:

main (Production)
└── develop (Integration)
    └── feature/*
    └── fix/*
    └── chore/*
    └── hotfix/*

## Branch Purpose

### main
- Production-ready code only.
- Protected branch.
- No direct pushes allowed.
- Changes arrive only through Pull Requests.

### develop
- Integration branch for completed work.
- Features are merged here before reaching production.

### Feature Branches
Created from `develop`.

Examples:

```text
feature/user-registration
feature/product-search
```

### Fix Branches
Created from `develop`.

Examples:

```text
fix/login-validation
fix/cart-calculation
```

### Chore Branches
Created from `develop`.

Examples:

```text
chore/update-dependencies
chore/config-cleanup
```

### Hotfix Branches
Created from `main` when urgent production issues must be fixed.

Examples:

```text
hotfix/payment-failure
hotfix/security-patch
```

---

# Branch Naming Convention

Use lowercase letters and hyphens.

Format:

```text
feature/short-description
fix/short-description
chore/short-description
hotfix/short-description
```

Examples:

```text
feature/user-authentication
fix/email-validation
chore/update-eslint-config
hotfix/payment-timeout
```

Do not use:

```text
Feature/Login
my-branch
test123
```

---

# Commit Message Convention

Format:

```text
type: short description
```

Examples:

```text
feat: add user registration endpoint
fix: correct password validation logic
chore: update dependencies
docs: add API setup instructions
refactor: simplify authentication service
test: add user service unit tests
```

## Allowed Types

```text
feat
fix
chore
docs
refactor
test
```

---

# Pull Request Process

All changes must be submitted through a Pull Request.

## PR Title

Use a clear title.

Examples:

```text
feat: implement user registration
fix: resolve cart total calculation bug
```

## PR Description

Every PR should explain:

- What was changed
- Why it was changed
- Any important implementation notes
- Testing performed

Example:

```text
## What
Implemented user registration endpoint.

## Why
Required for account creation functionality.

## Testing
- Unit tests added
- Manual API testing completed
```

## Merge Requirements

Before a PR can be merged:

- At least 1 reviewer approval is required
- All automated checks must pass
- No unresolved comments remain
- Branch must be up to date with target branch

---

# Development Workflow

1. Pull latest changes from develop

```bash
git checkout develop
git pull origin develop
```

2. Create a branch

```bash
git checkout -b feature/user-registration
```

3. Make changes and commit

```bash
git add .
git commit -m "feat: add user registration endpoint"
```

4. Push branch

```bash
git push origin feature/user-registration
```

5. Open Pull Request into develop

6. Obtain review approval

7. Merge after all checks pass

---

Following this guide ensures a consistent and predictable Git workflow across the project.
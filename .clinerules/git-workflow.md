---
description: Standard Git workflow and best practices for all projects
author: AI-Dev-Tools
version: 1.0
tags: ["git", "workflow", "version-control", "branching", "commits"]
globs: ["**/*"]
---

# Git Workflow and Best Practices

## Purpose

This rule defines a standard Git workflow and best practices to be followed across all projects. A consistent Git workflow improves collaboration, maintains a clean project history, facilitates code reviews, and makes it easier to track changes and releases.

## Guidelines

### Core Principles

- **Clean History**: Maintain a clean, meaningful commit history
- **Feature Isolation**: Develop features in isolation using branches
- **Continuous Integration**: Integrate changes frequently
- **Code Review**: Review code before merging to main branches
- **Semantic Versioning**: Use semantic versioning for releases

### Branching Strategy

We follow a modified Git Flow branching strategy:

#### Main Branches

- **main** (or **master**): Production-ready code
  - Always deployable
  - Never commit directly to main
  - Protected branch requiring pull request approvals

- **develop**: Integration branch for features
  - Contains the latest delivered development changes
  - Serves as integration branch for features
  - Should be stable but may contain features not yet ready for production

#### Supporting Branches

- **feature/[feature-name]**: New features
  - Branch from: `develop`
  - Merge back into: `develop`
  - Naming convention: `feature/user-authentication`, `feature/payment-gateway`

- **bugfix/[bug-name]**: Bug fixes for issues in development
  - Branch from: `develop`
  - Merge back into: `develop`
  - Naming convention: `bugfix/login-validation`, `bugfix/calculation-error`

- **hotfix/[hotfix-name]**: Urgent fixes for production issues
  - Branch from: `main`
  - Merge back into: `main` AND `develop`
  - Naming convention: `hotfix/security-vulnerability`, `hotfix/critical-error`

- **release/[version]**: Preparing for a new production release
  - Branch from: `develop`
  - Merge back into: `main` AND `develop`
  - Naming convention: `release/1.2.0`, `release/2.0.0`

### Workflow Process

#### Starting a New Feature

1. Ensure you have the latest `develop` branch:
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. Create a new feature branch:
   ```bash
   git checkout -b feature/my-new-feature
   ```

3. Work on your feature, committing changes regularly

#### Working on Your Feature

1. Make small, focused commits:
   ```bash
   git add [specific files]
   git commit -m "Add user authentication form"
   ```

2. Keep your branch updated with develop:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout feature/my-new-feature
   git merge develop
   ```

3. Resolve any merge conflicts

#### Completing a Feature

1. Ensure your code meets standards and passes tests:
   ```bash
   # Run linters and tests
   npm run lint
   npm test
   ```

2. Push your branch to the remote repository:
   ```bash
   git push origin feature/my-new-feature
   ```

3. Create a pull request to merge into `develop`

4. Address code review feedback

5. Once approved, merge the pull request

#### Creating a Release

1. Create a release branch from develop:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/1.2.0
   ```

2. Make any release-specific changes (version numbers, etc.)

3. Test thoroughly

4. Create a pull request to merge into `main`

5. Once approved, merge the pull request

6. Tag the release on main:
   ```bash
   git checkout main
   git pull origin main
   git tag -a v1.2.0 -m "Version 1.2.0"
   git push origin v1.2.0
   ```

7. Merge the release back into develop:
   ```bash
   git checkout develop
   git merge main
   git push origin develop
   ```

### Commit Guidelines

#### Commit Message Format

Follow the Conventional Commits specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Changes that don't affect code functionality (formatting, etc.)
- **refactor**: Code changes that neither fix a bug nor add a feature
- **perf**: Performance improvements
- **test**: Adding or correcting tests
- **chore**: Changes to build process or auxiliary tools

Examples:
```
feat(auth): add user authentication system

Implement JWT-based authentication with login, logout, and token refresh.

Closes #123
```

```
fix(payment): correct calculation error in tax processing

The tax was being calculated after discounts were applied, which is incorrect.
Now taxes are calculated on the pre-discount amount.

Fixes #456
```

#### Commit Best Practices

- Make small, focused commits that do one thing
- Write clear, descriptive commit messages
- Include the issue/ticket number in the commit message when applicable
- Don't commit commented-out code
- Don't commit temporary files, logs, or build artifacts
- Don't commit secrets or credentials

### Pull Request Guidelines

#### Creating Pull Requests

- Give your PR a clear, descriptive title
- Fill out the PR template completely
- Link to relevant issues
- Describe what changes were made and why
- Include screenshots for UI changes
- List any new dependencies
- Mention any breaking changes

#### Reviewing Pull Requests

- Be respectful and constructive
- Focus on the code, not the person
- Consider both functionality and code quality
- Approve only when all issues are addressed
- Use the PR checklist to ensure all standards are met

## Examples

### Good Commit Messages

```
feat(user): add password reset functionality

Implement password reset flow with email verification and secure token handling.
The token expires after 24 hours for security.

Closes #789
```

```
refactor(api): simplify error handling middleware

Consolidate error handling into a single middleware function to reduce
duplication and ensure consistent error responses across all API endpoints.
```

### Bad Commit Messages

```
fix stuff
```

```
WIP
```

```
Update code based on John's feedback
```

### Good Pull Request Title

"feat(checkout): Implement one-click purchase functionality"

### Bad Pull Request Title

"Fixed the things we talked about yesterday"

## Special Cases and Exceptions

- **Hotfixes**: In case of critical production issues, hotfixes can bypass the normal workflow but still require code review.
- **Small Projects**: For very small projects or prototypes, a simplified workflow with just `main` and feature branches may be used.
- **Monorepos**: For monorepos, consider using a scope in commit messages to indicate which package/app is affected.

## Related Rules

- [Code Review Process](./code-review-process.md): Detailed guidelines for code reviews
- [Release Process](./release-process.md): Guidelines for versioning and releasing software

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Semantic Versioning](https://semver.org/)

## Changelog

- v1.0 (2025-05-18): Initial version

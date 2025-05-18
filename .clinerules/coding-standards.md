---
description: Universal coding standards to be applied across all projects
author: AI-Dev-Tools
version: 1.0
tags: ["coding", "standards", "formatting", "best-practices"]
globs: ["**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx", "**/*.py", "**/*.html", "**/*.css"]
---

# Universal Coding Standards

## Purpose

This rule defines universal coding standards to be followed across all projects. Consistent coding standards improve readability, reduce errors, facilitate collaboration, and make maintenance easier. These standards represent best practices that should be applied regardless of the specific project or technology.

## Guidelines

### Core Principles

- **Readability First**: Code should be written for humans to read and understand. Prioritize clarity over cleverness.
- **Consistency**: Follow consistent patterns and conventions throughout the codebase.
- **Simplicity**: Prefer simple, straightforward solutions over complex ones when possible.
- **Self-Documentation**: Code should be self-documenting with clear variable names and structure.
- **DRY (Don't Repeat Yourself)**: Avoid duplication by abstracting common functionality.

### Specific Rules

#### Formatting

- **Indentation**: 
  - Use 2 spaces for JavaScript, TypeScript, HTML, and CSS
  - Use 4 spaces for Python
  - Never use tabs
- **Line Length**: Limit lines to 80-100 characters when possible
- **Whitespace**: 
  - Use blank lines to separate logical sections of code
  - Use consistent spacing around operators and after commas
- **Brackets**: 
  - Opening brackets on the same line as the statement (for JS/TS)
  - Closing brackets aligned with the opening statement

#### Naming Conventions

- **JavaScript/TypeScript**:
  - Use camelCase for variables and functions
  - Use PascalCase for classes and React components
  - Use UPPER_SNAKE_CASE for constants
  - Use kebab-case for file names
- **Python**:
  - Use snake_case for variables and functions
  - Use PascalCase for classes
  - Use UPPER_SNAKE_CASE for constants
  - Use snake_case for file names
- **General**:
  - Names should be descriptive and meaningful
  - Avoid abbreviations unless they are well-known
  - Boolean variables should have prefixes like "is", "has", or "should"

#### Code Organization

- **File Structure**:
  - One primary concern per file
  - Related functionality grouped together
  - Imports at the top, organized by type
- **Function Design**:
  - Functions should do one thing and do it well
  - Keep functions small (under 30 lines when possible)
  - Limit parameters (no more than 3-4 parameters)
- **Comments**:
  - Use comments to explain "why", not "what"
  - Keep comments up-to-date with code changes
  - Use JSDoc/TSDoc for JavaScript/TypeScript functions
  - Use docstrings for Python functions

## Examples

### Good Examples

```javascript
// JavaScript/TypeScript
function calculateTotalPrice(items, taxRate) {
  // Early return for edge cases
  if (!items || items.length === 0) {
    return 0;
  }

  // Calculate subtotal
  const subtotal = items.reduce((total, item) => {
    return total + (item.price * item.quantity);
  }, 0);

  // Apply tax and return
  return subtotal * (1 + taxRate);
}
```

```python
# Python
def calculate_total_price(items, tax_rate):
    # Early return for edge cases
    if not items:
        return 0
    
    # Calculate subtotal
    subtotal = sum(item.price * item.quantity for item in items)
    
    # Apply tax and return
    return subtotal * (1 + tax_rate)
```

### Bad Examples

```javascript
// JavaScript/TypeScript - Bad Example
function calc(i, t) {
  let tot = 0;
  if(i && i.length > 0) {
    for(let x = 0; x < i.length; x++) {
      tot += i[x].p * i[x].q;
    }
    tot = tot * (1 + t);
    return tot;
  } else {
    return 0;
  }
}
```

```python
# Python - Bad Example
def calc(i, t):
    tot = 0
    if i and len(i) > 0:
        for x in range(len(i)):
            tot += i[x].p * i[x].q
        tot = tot * (1 + t)
        return tot
    else:
        return 0
```

## Special Cases and Exceptions

- **Legacy Code**: When working with legacy code, follow the existing conventions of that codebase for consistency, even if they differ from these standards.
- **Framework-Specific Conventions**: Some frameworks have their own conventions that should take precedence (e.g., Angular's specific naming patterns).
- **Performance-Critical Code**: In rare cases where performance is critical, readability might be sacrificed for performance, but such cases should be well-documented.

## Related Rules

- Documentation Guidelines: More detailed standards for code documentation
- Code Review Process: How these standards are enforced during code reviews

## References

- [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html)
- [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)

## Changelog

- v1.0 (2025-05-18): Initial version

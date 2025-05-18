---
description: Guidelines for organizing and managing global and workspace-specific rules for Cline
author: AI-Dev-Tools
version: 1.0
tags: ["clinerules", "organization", "global-rules", "workspace-rules"]
globs: ["**/*"]
---

# Organizing Global and Workspace Rules

This guide explains how to organize and manage both global and workspace-specific rules for Cline, ensuring a clear separation of concerns while maintaining consistency across projects.

## Rule Types Overview

Cline uses two types of rules:

1. **Global Rules**: Apply across all projects
   - Located in: `/Users/oz/Documents/Cline/Rules/`
   - Contain universal standards, patterns, and workflows
   - Can be toggled on/off for any project

2. **Workspace Rules**: Apply to a specific project only
   - Located in: `/Users/oz/Sites/ai-dev-tools/.clinerules/`
   - Contain project-specific guidelines and requirements

## When to Use Each Type

### Use Global Rules For:

- Coding standards that apply across all projects
- Technology-specific patterns you use consistently
- Standard workflows (Git, deployment, etc.)
- Documentation standards
- Common architectural patterns
- Security best practices

### Use Workspace Rules For:

- Project-specific architecture decisions
- Custom component structures for this project
- Project-specific naming conventions
- Domain-specific guidelines
- Team agreements for the current project
- Project-specific workflows

## Directory Structure

### Global Rules Structure

```
/Users/oz/Documents/Cline/Rules/
├── memory-bank.md                 # Memory Bank system documentation
├── coding-standards.md            # General coding standards
├── react-patterns.md              # React best practices
├── git-workflow.md                # Git branching and commit standards
└── ...
```

In this project, we use a symbolic link to access these global rules:

```
/Users/oz/Sites/ai-dev-tools/global-rules/ -> /Users/oz/Documents/Cline/Rules/
```

### Workspace Rules Structure

```
/Users/oz/Sites/ai-dev-tools/.clinerules/
├── next-js-supabase-stripe.md     # Project-specific Next.js, Supabase, and Stripe integration
├── cline-for-webdev-ui.md         # Web design guidelines for this project
└── ...
```

### Project-Specific Documentation

```
/Users/oz/Sites/ai-dev-tools/ai-dev-docs/7-clinerules/
├── README.md                      # Overview of the rules system
├── project-specific-rules.md      # Core project guidelines
├── rule-organization-guide.md     # This guide
├── continuous-improvement-rules.md # How to improve rules over time
├── knowledge-gap-rules.md         # Handling knowledge gaps
└── workflow-rules.md              # Project workflow guidelines
```

## Rule Precedence

When both global and workspace rules exist:

1. **Workspace rules take precedence** when they explicitly override global rules
2. **Global rules provide the foundation** that workspace rules build upon
3. **Both should be considered** when working on a project

## Integration Approach

### 1. Reference Global Rules in Workspace Rules

In your workspace rules, explicitly reference relevant global rules:

```markdown
## Related Global Rules

This project follows these global rules with the following project-specific adaptations:

- [Coding Standards](../global-rules/coding-standards.md)
- [React Patterns](../global-rules/react-patterns.md)
- [Next.js Patterns](../global-rules/nextjs-patterns.md)
- [Git Workflow](../global-rules/git-workflow.md)
```

### 2. Specify Exceptions in Workspace Rules

When a workspace rule needs to override a global rule, clearly document the exception:

```markdown
## Exceptions to Global Rules

While we generally follow the global React patterns, this project has the following exceptions:

1. **Component Organization**: Due to the microservices architecture of this project, 
   components are organized by domain rather than by type.

2. **State Management**: This project uses Redux instead of the Context API 
   recommended in the global rules.
```

### 3. Use Consistent Formatting

Use the same formatting and structure for both global and workspace rules to make them easier to compare and understand.

## Creating New Rules

### Creating a New Global Rule

1. Identify which category the rule belongs to
2. Copy the template from `global-rules/templates/rule-template.md`
3. Create the file in the appropriate directory
4. Fill in the content following the template structure
5. Reference any related workspace rules if applicable

### Creating a New Workspace Rule

1. Identify the specific project need
2. Create a new file in `ai-dev-docs/7-clinerules/`
3. Follow the same structure as global rules for consistency
4. Reference any related global rules
5. Clearly specify any exceptions to global rules

## Maintaining Rules

### Updating Global Rules

When updating a global rule:

1. Increment the version number
2. Add a changelog entry
3. Consider the impact on all projects using this rule
4. Update any workspace rules that reference this global rule

### Updating Workspace Rules

When updating a workspace rule:

1. Increment the version number
2. Add a changelog entry
3. Ensure it remains consistent with global rules or clearly documents exceptions
4. Update the project's Memory Bank to reflect the changes

## Best Practices

1. **Start with Global Rules**: Begin by establishing solid global rules before creating workspace-specific exceptions
2. **Minimize Exceptions**: Try to follow global rules when possible to maintain consistency
3. **Document Rationale**: Always explain why a workspace rule differs from a global rule
4. **Regular Review**: Periodically review both global and workspace rules to ensure they remain relevant
5. **Promote Reuse**: If you find a workspace rule that could benefit all projects, consider promoting it to a global rule

## Example: React Component Structure

### Global Rule (Excerpt from react-patterns.md)

```markdown
## Component Structure

- Use functional components with hooks
- One component per file
- Group related components in folders
- Use index.js to export components
```

### Workspace Rule (Excerpt from component-structure.md)

```markdown
## Component Structure

We follow the global React patterns with these project-specific adaptations:

- Components are organized by domain (users, products, orders)
- Each domain has its own components, hooks, and tests directories
- We use Atomic Design principles (atoms, molecules, organisms)

### Exception to Global Rules

While the global rules recommend one component per file, this project allows 
multiple small, related components in a single file when they are tightly coupled
and under 50 lines of code combined.
```

## Conclusion

By clearly separating global and workspace-specific rules, you can maintain consistency across projects while allowing for project-specific adaptations. This approach provides the best of both worlds: standardization where it makes sense and customization where it's needed.

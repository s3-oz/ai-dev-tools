# Cline Rules Documentation

This directory contains documentation about the Cline Rules system, which provides structured guidelines and standards for AI-assisted development.

## What are Cline Rules?

Cline Rules are structured guidelines that help maintain consistency, quality, and best practices across projects. They serve as a knowledge base that Cline can reference to understand project standards and expectations.

## Rule Locations

Cline Rules are stored in two primary locations:

1. **Global Rules**: 
   - Located in: `/Users/oz/Documents/Cline/Rules/`
   - Apply to all projects across your system
   - Include fundamental rules like `memory-bank.md`, `coding-standards.md`, and `git-workflow.md`
   - Can be toggled on/off for any project

2. **Workspace-Specific Rules**:
   - Located in: `/Users/oz/Sites/ai-dev-tools/.clinerules/`
   - Apply only to the current project/workspace
   - Contain project-specific guidelines and requirements

In this project, we use a symbolic link (`global-rules/`) that points to the global rules directory, making it easier to reference global rules from within the project.

## Rule Hierarchy

When both global and workspace-specific rules exist:

1. Workspace-specific rules take precedence when they explicitly override global rules
2. Global rules provide the foundation that workspace-specific rules build upon
3. Global rules can be toggled on/off for specific projects as needed

## Using Cline Rules

To reference these rules in your interactions with Cline:

1. For general guidance: "Please follow the coding standards in our clinerules"
2. For specific rule application: "Apply the Next.js patterns from our clinerules to this component"
3. To update rules: "Let's update the React patterns rule to include the new hook pattern"

## Updating Rules

When you need to update a rule:

1. Edit the appropriate file in the `.clinerules/` directory
2. Increment the version number in the frontmatter
3. Add a changelog entry at the bottom of the file
4. Consider the impact on existing code

## Memory Bank Integration

The Cline Rules system integrates with the Memory Bank system:

1. Rules provide standards and patterns
2. Memory Bank tracks how these are applied to the specific project
3. Together they ensure consistent, high-quality development across sessions

# Cline Rules Documentation

This directory contains documentation about the Cline Rules system, which provides structured guidelines and standards for AI-assisted development.

## What are Cline Rules?

Cline Rules are structured guidelines that help maintain consistency, quality, and best practices across projects. They serve as a knowledge base that Cline can reference to understand project standards and expectations.

## Rule Locations

Cline Rules are stored in two primary locations:

1. **User-Level Global Rules**: 
   - Located in: `/Users/oz/Documents/Cline/Rules/`
   - Apply to all projects across your system
   - Include fundamental rules like `memory-bank.md` and `git-workflow.md`

2. **Project-Level Global Rules**:
   - Located in: `/Users/oz/Sites/ai-dev-tools/.clinerules/`
   - Apply to all parts of the current project
   - Include:
     - `memory-bank.md` - Memory Bank system documentation
     - `coding-standards.md` - General coding standards
     - `react-patterns.md` - React best practices
     - `nextjs-patterns.md` - Next.js best practices
     - `git-workflow.md` - Git branching and commit standards

## Rule Hierarchy

When both user-level and project-level rules exist:

1. Project-level rules take precedence when they explicitly override user-level rules
2. User-level rules provide the foundation that project-level rules build upon

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

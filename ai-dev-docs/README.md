# AI-Assisted Development Documentation System

This documentation system provides a structured approach to maintaining project context, knowledge, and workflows when working with AI assistants like Claude. It's designed to solve the problem of context loss between sessions and enable seamless transitions between multiple projects.

## Directory Structure

The documentation is organized into 8 main categories, with some categories having parallel tracks for different aspects of documentation:

```
ai-dev-docs/
├── 0-memory-bank/             # Core memory structure for AI assistants
├── 1-project-foundation/      # Project goals, requirements, and scope
├── 2-collaboration-framework/ # Team collaboration guidelines
├── 3-architecture-design/     # System architecture and design patterns
├── 3-knowledge-management/    # Documentation standards and knowledge sharing
├── 4-brand-and-content/       # Brand guidelines and content strategy
├── 4-development-guides/      # Development standards and practices
├── 5-development-guides/      # (Alternative location for development guides)
├── 5-technical-specifications/# Detailed technical specifications
├── 6-automation-workflows/    # CI/CD and automation documentation
├── 6-operations-deployment/   # Operations and deployment documentation
├── 7-clinerules/              # AI behavior rules documentation
├── 7-user-documentation/      # End-user documentation
└── 8-project-transitions/     # Project transition management
```

> **Note on Numbering**: The system uses parallel tracks with duplicate numbers (e.g., two "3-" directories) to separate technical and non-technical documentation. When implementing this system for your project, you can choose to maintain this structure or simplify it with a linear numbering scheme.

## Key Features

### 1. Memory Bank System

The Memory Bank system (in `0-memory-bank/`) provides a structured way for AI assistants to maintain context across sessions. It consists of six core files:

- `projectbrief.md` - Foundation document defining project goals and requirements
- `productContext.md` - Why the project exists and how it should work
- `systemPatterns.md` - Technical architecture and design patterns
- `techContext.md` - Technical environment and constraints
- `activeContext.md` - Current work focus and recent changes
- `progress.md` - Overall project progress tracking

See the [Memory Bank README](0-memory-bank/README.md) for detailed information.

### 2. Project Transitions

The Project Transitions system (in `8-project-transitions/`) enables seamless switching between multiple projects. It provides:

- Command triggers for project management (`!project-snapshot`, `!switch-to`, etc.)
- Project snapshots for capturing project state
- Project index for tracking all projects

See the [Command Cheat Sheet](8-project-transitions/command-cheat-sheet.md) for usage instructions.

## Quick Start Guide

### Minimal Setup (5 Minutes)

1. Create a `memory-bank` directory in your project
2. Create these essential files:
   - `projectbrief.md`: Basic project description and goals
   - `activeContext.md`: What you're currently working on
   - `progress.md`: What's done and what's next
3. Type `!update-memory-bank` to have the AI read these files

### First Project Setup (15 Minutes)

1. Copy the template files from `0-memory-bank/*.template` to your project
2. Fill out `projectbrief.md` with your project's basic information:
   ```markdown
   # Project Brief: [Your Project Name]
   
   ## Overview
   [1-2 sentences describing your project]
   
   ## Objectives
   - [Primary goal]
   - [Secondary goal]
   
   ## Requirements
   - [Core requirement 1]
   - [Core requirement 2]
   ```
3. Add minimal information to `activeContext.md`:
   ```markdown
   # Active Context
   
   ## Current Focus
   [What you're working on right now]
   
   ## Next Steps
   1. [First task]
   2. [Second task]
   ```
4. Type `!project-snapshot` to create your first project snapshot

### Working with the AI

1. Start each session by having the AI review your memory bank
2. Use `!update-memory-bank` at the end of significant work sessions
3. When referencing development standards, point the AI to specific guides
4. Let the AI suggest updates to documentation as patterns emerge

## Getting Started

### Initial Setup (Detailed)

1. Create the memory bank files for your project in `0-memory-bank/`
   - Copy the template files (*.template) to create your initial files
   - At minimum, create `projectbrief.md`, `activeContext.md`, and `progress.md`
   - Other files can be added as your project develops

2. Fill in the `projectbrief.md` file with your project information
   - Include project goals, requirements, and scope
   - This serves as the foundation for all other documentation

3. Gradually populate the other memory bank files as your project progresses
   - `productContext.md`: Add user experience goals and key features
   - `systemPatterns.md`: Document your technical architecture as it evolves
   - `techContext.md`: List technologies and development environment details

4. Use the `!project-snapshot` command to create your first project snapshot
   - This captures the current state of your project
   - It's stored in `8-project-transitions/project-snapshots/`

### Daily Workflow

1. Start your day with `!project-status` to see all your projects
2. Use `!switch-to [project-name]` if you need to change projects
3. Work on your project as normal
4. Use `!update-memory-bank` at the end of your session to update the memory bank
5. Use `!project-snapshot` to capture the current state before ending your session

### Adding Documentation

As your project grows, add documentation to the appropriate categories:

- Technical documentation in `3-knowledge-management/`
- Development standards in `4-development-guides/` or `5-development-guides/`
- Brand guidelines in `4-brand-and-content/`
- Technical specifications in `5-technical-specifications/`
- Automation workflows in `6-automation-workflows/`
- AI behavior rules in `7-clinerules/`

> **Note**: You don't need to implement all categories at once. Start with the Memory Bank and add other documentation as needed.

## Command Reference

| Command | Description |
|---------|-------------|
| `!project-snapshot` | Creates a snapshot of the current project state |
| `!switch-to [project-name]` | Switches to the specified project |
| `!project-status` | Lists all projects and their status |
| `!update-memory-bank` | Updates all memory bank files |

See the [Command Cheat Sheet](8-project-transitions/command-cheat-sheet.md) for detailed usage instructions.

## Best Practices

1. **Keep the memory bank updated** - The memory bank is the primary source of context for AI assistants
2. **Create snapshots regularly** - Snapshots capture the current state of your project
3. **Use the command triggers** - They automate the process of managing project context
4. **Organize documentation logically** - Put documentation in the appropriate category
5. **Cross-reference between files** - Link related information to create a connected knowledge base
6. **Start minimal and grow** - Begin with just the essential files and expand as needed
7. **Be consistent with updates** - Regular updates are better than occasional comprehensive ones
8. **Let the AI help maintain docs** - The AI can suggest updates based on your work patterns

## How the AI Interacts with Documentation

- **Reading**: The AI reads the memory bank files at the start of each session to understand context
- **Referencing**: The AI references development guides and other documentation when writing code
- **Updating**: When you use `!update-memory-bank`, the AI reviews and updates relevant files
- **Creating**: The AI can create new documentation based on patterns it observes in your project
- **Suggesting**: The AI may suggest improvements to documentation as your project evolves

## Contributing

Feel free to customize this documentation structure to fit your specific needs. Add new categories, modify existing ones, or create new command triggers as needed.

## License

This documentation system is provided as-is with no warranty. You are free to use, modify, and distribute it as you see fit.

# Project Transition Commands Cheat Sheet

This cheat sheet provides a quick reference for all project transition commands defined in the `.clinerules/project-transitions.md` file.

## Core Commands

| Command | Description | When to Use |
|---------|-------------|-------------|
| `!project-snapshot` | Creates a comprehensive snapshot of the current project state | Before switching to another project |
| `!switch-to [project-name]` | Switches to the specified project and loads its snapshot | When starting work on a different project |
| `!project-status` | Lists all projects and their status | When planning work across multiple projects |
| `!update-memory-bank` | Updates all memory bank files with current state | Periodically to maintain accurate context |

## Command Details

### `!project-snapshot`

**Usage:** Simply type `!project-snapshot` in the chat.

**What it does:**
- Generates a comprehensive snapshot of the current project state
- Saves it to `/ai-dev-docs/8-project-transitions/project-snapshots/[project-name]-snapshot.md`
- Updates the project index at `/ai-dev-docs/8-project-transitions/project-index.md`
- Confirms completion with a summary of what was captured

**Example:**
```
User: !project-snapshot
AI: Creating snapshot for project "ai-dev-tools"...
    Snapshot saved to /ai-dev-docs/8-project-transitions/project-snapshots/ai-dev-tools-snapshot.md
    Project index updated.
    
    Snapshot summary:
    - 4 active tasks captured
    - 3 recently completed items
    - 4 planned next steps
```

### `!switch-to [project-name]`

**Usage:** Type `!switch-to` followed by the project name.

**What it does:**
- Generates a snapshot of the current project (if applicable)
- Loads the specified project's snapshot
- Reviews the memory bank for that project
- Provides a re-orientation summary

**Example:**
```
User: !switch-to SimStudio-v2
AI: Switching to project "SimStudio-v2"...
    Creating snapshot of current project "ai-dev-tools"...
    Loading SimStudio-v2 snapshot...
    
    Re-orientation Summary:
    - You were working on: Email notification system
    - Last activity: Added booking confirmation templates
    - Next steps: Implement cancellation workflow
```

### `!project-status`

**Usage:** Simply type `!project-status` in the chat.

**What it does:**
- Lists all projects in the project index
- Shows their current status and last activity date
- Highlights any pending tasks or next steps

**Example:**
```
User: !project-status
AI: Project Status Overview:
    
    Active Projects:
    1. ai-dev-tools (Active, Last activity: 2025-05-14)
       - Next steps: Create memory bank templates
    
    2. SimStudio-v2 (Active, Last activity: 2025-05-14)
       - Next steps: Complete email notification system
```

### `!update-memory-bank`

**Usage:** Simply type `!update-memory-bank` in the chat.

**What it does:**
- Reviews ALL memory bank files
- Updates them with current project state
- Focuses particularly on activeContext.md and progress.md
- Confirms completion with a summary of updates

**Example:**
```
User: !update-memory-bank
AI: Updating memory bank for project "ai-dev-tools"...
    
    Files updated:
    - activeContext.md: Added recent work on project transitions
    - progress.md: Updated status of documentation structure
    - systemPatterns.md: Added project transition workflow
    
    Memory bank is now up to date with current project state.
```

## Best Practices

1. **Create snapshots regularly** - Even if you're not switching projects, create snapshots at key milestones
2. **Update the memory bank** - Run `!update-memory-bank` at the end of each significant work session
3. **Check project status** - Use `!project-status` at the start of your day to plan your work
4. **Always snapshot before switching** - Create a snapshot before switching to ensure no context is lost

## Troubleshooting

If a command doesn't work as expected:

1. Check that the `.clinerules/project-transitions.md` file exists and is properly formatted
2. Ensure the AI has access to the necessary directories
3. Try restarting the conversation if the AI seems to have lost context
4. Manually create a snapshot if the automatic process fails

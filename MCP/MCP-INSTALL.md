# MCP Server Installation and Configuration Guide

*Date: 4th June 2025 (AEST) - Updated with correct Claude Code MCP configuration*

## Overview

This guide documents how to properly install and configure MCP (Model Context Protocol) servers for Claude Code. Based on extensive testing with the actual Claude Code MCP system.

## Key Concepts

### MCP Server Scopes

**User Scope (Recommended):**
- Available across ALL your projects
- Added with: `claude mcp add -s user`
- Perfect for tools you want everywhere

**Project Scope:**
- Shared with team via `.mcp.json` file
- Added with: `claude mcp add -s project`
- Good for team-specific tools

**Local Scope:**
- Only available to you in current project
- Added with: `claude mcp add` (default)
- For project-specific tools

**Project Permissions:**
- Control which MCP servers each project can access
- Configured in `.claude/settings.local.json`
- Each project decides what MCP servers it wants to use

### The MCP Philosophy

MCP servers are **reusable services** that any project can access:
- Install once globally
- Configure access per-project
- Perfect for automation tooling across multiple projects

## Installation Process

### 1. Add MCP Servers via Claude Code CLI

**IMPORTANT:** Don't use `npm install -g`. Use Claude Code's MCP system instead.

```bash
# Context7 - Documentation and library assistance
claude mcp add context7 -s user -- npx @upstash/context7-mcp

# GitHub integration
claude mcp add github -s user -- npx @modelcontextprotocol/server-github

# Slack integration (with environment variables)
claude mcp add slack -s user -e SLACK_BOT_TOKEN=xoxb-your-token -e SLACK_TEAM_ID=T123456 -e SLACK_CHANNEL_IDS=C123456,C789012 -- npx @modelcontextprotocol/server-slack

# Supabase database operations
claude mcp add supabase -s user -e SUPABASE_ACCESS_TOKEN=your-token -- npx @supabase/mcp-server-supabase

# Brave search capabilities
claude mcp add brave-search -s user -e BRAVE_API_KEY=your-key -- npx @modelcontextprotocol/server-brave-search
```

### 2. Verify MCP Server Installation

Check that MCP servers are configured:

```bash
claude mcp list
```

Should show your configured servers like:
```
context7: npx @upstash/context7-mcp
slack: npx @modelcontextprotocol/server-slack
github: npx @modelcontextprotocol/server-github
```

### 3. Configure Project Access

In each project, create/edit `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "mcp__context7__*",
      "mcp__github__*",
      "mcp__slack__*",
      "mcp__supabase__*",
      "mcp__brave-search__*",
      "Bash(python:*)",
      "Bash(ls:*)",
      "Bash(grep:*)",
      "WebFetch(domain:docs.anthropic.com)"
    ],
    "deny": []
  },
  "enableAllProjectMcpServers": true
}
```

## Key Configuration Settings

### enableAllProjectMcpServers

```json
"enableAllProjectMcpServers": true
```

**CRITICAL:** This must be `true` to access user-scope MCP servers. Without this, only local/project-specific servers work.

### MCP Permissions

Each MCP server needs specific permissions in the `allow` array:

```json
"mcp__context7__*",           // All Context7 operations
"mcp__github__*",             // All GitHub operations
"mcp__slack__*",              // All Slack operations
"mcp__supabase__*",           // All Supabase operations
"mcp__brave-search__*"        // All Brave search operations
```

**Use `*` wildcard** for all operations, or specific function names for granular control.

## Working Example

### Complete Setup Example

**Step 1: Add user-scope MCP servers**
```bash
claude mcp add context7 -s user -- npx @upstash/context7-mcp
claude mcp add github -s user -- npx @modelcontextprotocol/server-github
```

**Step 2: Project configuration**
File: `/Users/oz/Sites/your-project/.claude/settings.local.json`

```json
{
  "permissions": {
    "allow": [
      "mcp__context7__*",
      "mcp__github__*",
      "Bash(python:*)",
      "WebFetch(domain:localhost)"
    ],
    "deny": []
  },
  "enableAllProjectMcpServers": true
}
```

## Testing MCP Installation

### 1. Check MCP Configuration

List configured MCP servers:

```bash
claude mcp list
```

Should show your configured servers:
```
context7: npx @upstash/context7-mcp
github: npx @modelcontextprotocol/server-github
slack: npx @modelcontextprotocol/server-slack
```

### 2. Debug Failed Connections

If a server shows as "failed":

```bash
claude --mcp-debug
```

This shows error logs inline.

### 3. Check Log Files

MCP logs are stored in:
```
/Users/oz/Library/Caches/claude-cli-nodejs/-Users-oz-Sites-[project-name]/
```

## Common Issues and Solutions

### "No token data found"

**Problem:** MCP server needs authentication
**Solution:** Add environment variables or API keys to project settings

### "enableAllProjectMcpServers": false

**Problem:** Global MCP servers disabled
**Solution:** Change to `true` in `.claude/settings.local.json`

### Permission Denied

**Problem:** Missing MCP permissions
**Solution:** Add specific `mcp__[server]__*` permissions to allow array

### Server Not Found

**Problem:** MCP server not installed globally
**Solution:** Install with `npm install -g @[package-name]`

## Creating Custom MCP Servers

### For Your Automation Projects

You can create custom MCP servers for your Python tools:

```bash
# Example: Make your concrete industry collector a global MCP server
npm install -g your-concrete-industry-mcp-server
```

Then any project can access it by adding permissions:

```json
"mcp__concrete-industry__collect-data",
"mcp__concrete-industry__search-companies"
```

## Best Practices

### 1. Install Once, Use Everywhere

- Install MCP servers globally
- Don't reinstall for each project
- Manage access through project permissions

### 2. Minimal Permissions

Grant permissions your project needs:

```json
// Recommended - use wildcards for simplicity
"mcp__context7__*"

// Alternative - specific permissions for granular control
"mcp__context7__resolve-library-id",
"mcp__context7__get-library-docs"
```

### 3. Environment Variables

For MCP servers requiring API keys, add them when configuring the server:

```bash
# Add environment variables directly to MCP server config
claude mcp add github -s user -e GITHUB_TOKEN=your-token -- npx @modelcontextprotocol/server-github
claude mcp add slack -s user -e SLACK_BOT_TOKEN=xoxb-token -e SLACK_TEAM_ID=T123456 -- npx @modelcontextprotocol/server-slack
```

### 4. Project Templates

Create a template `.claude/settings.local.json` for new projects:

```json
{
  "permissions": {
    "allow": [
      "mcp__context7__*",
      "mcp__github__*",
      "Bash(python:*)",
      "Bash(ls:*)",
      "Bash(grep:*)"
    ],
    "deny": []
  },
  "enableAllProjectMcpServers": true
}
```

## Troubleshooting Commands

```bash
# List configured MCP servers
claude mcp list

# Get details about a specific server
claude mcp get context7

# Remove and re-add a problematic server
claude mcp remove context7 -s user
claude mcp add context7 -s user -- npx @upstash/context7-mcp

# Check Claude Code version
claude --version

# Check MCP server status
claude mcp list

# View MCP logs
ls -la ~/Library/Caches/claude-cli-nodejs/
```

## Directory Structure

```
~/.claude/                           # Claude Code global settings
├── settings.json                    # Global Claude settings
└── settings.local.json              # Global local overrides

[project]/.claude/                   # Project-specific settings
├── settings.json                    # Project settings
└── settings.local.json              # Project local overrides (this is where MCP permissions go)

~/Library/Caches/claude-cli-nodejs/  # MCP logs and cache
└── -Users-oz-Sites-[project]/       # Project-specific MCP logs
```

## Conclusion

MCP servers are powerful once you understand the scope system:

1. **Add servers with correct scope** - Use `claude mcp add -s user` for global access
2. **Configure per-project permissions** - Control access through `.claude/settings.local.json`
3. **Enable user-scope access** - `"enableAllProjectMcpServers": true`
4. **Use wildcard permissions** - `"mcp__servername__*"` for simplicity

This approach lets you build a **reusable services ecosystem** where any project can access the MCP tools it needs through simple permission configuration.

---

*This guide was updated after extensive testing with Claude Code's actual MCP system. The key insight: Use `claude mcp add -s user` for global servers, control access per-project with permissions.*
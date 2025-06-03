# MCP Server Installation and Configuration Guide

*Date: 3rd June 2025 (AEST)*

## Overview

This guide documents how to properly install and configure MCP (Model Context Protocol) servers for Claude Code. The official documentation is confusing as fuck, so this is a practical guide based on real-world testing.

## Key Concepts

### Global vs Project MCP Servers

**Global MCP Servers:**
- Installed once on your machine
- Available to ALL projects
- Live in system directories (npm global packages)
- Think of them as "services" you can call from any project

**Project Settings:**
- Control which global servers a project can access
- Just permission gates, NOT installations
- Each project decides what MCP servers it wants to use

### The MCP Philosophy

MCP servers are **reusable services** that any project can access:
- Install once globally
- Configure access per-project
- Perfect for automation tooling across multiple projects

## Installation Process

### 1. Install MCP Servers Globally

Install MCP servers system-wide using npm:

```bash
# Context7 - Documentation and library assistance
npm install -g @upstash/context7-mcp

# GitHub integration
npm install -g @modelcontextprotocol/server-github

# Supabase database operations
npm install -g @supabase/mcp-server-supabase

# Brave search capabilities
npm install -g @modelcontextprotocol/server-brave-search

# Sequential thinking enhancement
npm install -g @modelcontextprotocol/server-sequential-thinking
```

### 2. Verify Global Installation

Check that MCP servers are installed globally:

```bash
npm list -g | grep mcp
```

### 3. Configure Project Access

In each project, create/edit `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "mcp__context7__resolve-library-id",
      "mcp__context7__get-library-docs",
      "mcp__github__*",
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

**CRITICAL:** This must be `true` to access global MCP servers. Without this, only project-specific servers work.

### MCP Permissions

Each MCP server needs specific permissions in the `allow` array:

```json
"mcp__context7__resolve-library-id",     // Context7 library resolution
"mcp__context7__get-library-docs",       // Context7 documentation
"mcp__github__*",                        // All GitHub operations
"mcp__supabase__*",                      // All Supabase operations
"mcp__brave-search__*"                   // All Brave search operations
```

## Working Example

### s3multi Project (Working Configuration)

File: `/Users/oz/Sites/s3multi/.claude/settings.local.json`

```json
{
  "permissions": {
    "allow": [
      "mcp__context7__resolve-library-id",
      "mcp__context7__get-library-docs",
      "Bash(supabase db push:*)",
      "Bash(python:*)",
      "mcp__supabase__list_migrations",
      "mcp__supabase__execute_sql",
      "WebFetch(domain:localhost)"
    ],
    "deny": []
  },
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": [
    "supabase"
  ]
}
```

## Testing MCP Installation

### 1. Check MCP Status

From any project directory:

```bash
claude mcp
```

Should show status of available MCP servers. Example output:
```
MCP Server Status

• context7: connected
• github: connected
• supabase: connected
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

Only grant permissions your project actually needs:

```json
// Good - specific permissions
"mcp__context7__resolve-library-id"

// Avoid - overly broad (unless needed)
"mcp__context7__*"
```

### 3. Environment Variables

For MCP servers requiring API keys, set them globally:

```bash
export GITHUB_TOKEN="your-token"
export SUPABASE_ACCESS_TOKEN="your-token"
```

### 4. Project Templates

Create a template `.claude/settings.local.json` for new projects:

```json
{
  "permissions": {
    "allow": [
      "mcp__context7__resolve-library-id",
      "mcp__context7__get-library-docs",
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
# List installed global npm packages
npm list -g --depth=0

# Check Claude Code version
claude --version

# Debug MCP connections
claude --mcp-debug

# Check MCP status
claude mcp

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

MCP servers are powerful once you understand the global/project distinction:

1. **Install globally** - One-time setup for each MCP server
2. **Configure per-project** - Control access through permissions
3. **Enable global access** - `"enableAllProjectMcpServers": true`
4. **Grant specific permissions** - Only what each project needs

This approach lets you build a **reusable services ecosystem** where any automation project can access the tools it needs without reinstalling everything.

---

*This guide was created after fighting through the confusing official MCP documentation. The key insight: MCP servers are global services, project settings are just access controls.*
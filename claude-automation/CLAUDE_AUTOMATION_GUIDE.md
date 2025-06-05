# Claude Automation Guide - Unmanned Sessions with Slack
*Created: January 9, 2025 8:11 PM AEST*

## Overview
This guide explains how to run unmanned Claude sessions that can monitor Slack and respond autonomously.

## The Challenge
Claude operates in a request-response pattern - it can't independently decide to check Slack or take actions without being prompted. This creates a challenge for unmanned operation.

## Solution Architecture

### 1. External Orchestration
We use external scripts to:
- Periodically trigger Claude to check Slack
- Pass Claude's responses back to Slack
- Maintain state between checks

### 2. Available Scripts

#### Basic Node.js Monitor (`claude-slack-monitor.js`)
Simple monitoring script that checks Slack every 30 seconds.

```bash
# Basic monitoring
node claude-slack-monitor.js

# With task context
node claude-slack-monitor.js --context "Building JWT authentication"

# Custom interval (60 seconds)
node claude-slack-monitor.js --interval 60000
```

#### Advanced Python System (`claude_slack_automation.py`)
More sophisticated system with state persistence and session management.

```bash
# Basic monitoring
python3 claude_slack_automation.py

# With named session (persists state)
python3 claude_slack_automation.py --session auth-project --task "Implement JWT authentication"

# Test single cycle
python3 claude_slack_automation.py --test --task "Check for questions"

# Custom channel and interval
python3 claude_slack_automation.py --channel C12345 --interval 60
```

## How It Works

1. **Periodic Execution**: Scripts run Claude CLI commands at intervals
2. **Slack Checking**: Claude uses MCP tools to check for new messages
3. **Intelligent Response**: Claude determines if messages need responses
4. **Task Continuation**: Claude can continue working on tasks between checks
5. **State Persistence**: Advanced script maintains state across restarts

## Setup Requirements

1. **Claude CLI**: Must be installed and authenticated
2. **Slack MCP**: Already configured in your `mcp.json`
3. **Permissions**: Ensure `.claude/settings.local.json` allows Slack operations
4. **Node.js/Python**: Required for running automation scripts

## Use Cases

### 1. Development Support
Run Claude to monitor a dev channel and answer questions while you're away:
```bash
python3 claude_slack_automation.py --session dev-support --task "Answer questions about our API"
```

### 2. Automated Testing
Have Claude run tests and report results:
```bash
python3 claude_slack_automation.py --task "Run test suite every hour and report failures to Slack"
```

### 3. Documentation Updates
Monitor for documentation requests:
```bash
node claude-slack-monitor.js --context "Update documentation based on Slack requests"
```

## Limitations

1. **Not True Autonomy**: Still requires external script to trigger Claude
2. **Token Usage**: Each check consumes tokens, even if no action needed
3. **Context Limits**: Long-running sessions may hit context limits
4. **Error Recovery**: Scripts need manual restart on critical errors

## Advanced Features

### Session Recovery
The Python script maintains session state:
- Tracks processed messages (won't respond twice)
- Saves checkpoints for task progress
- Recovers from restarts

### Custom Prompts
You can modify the scripts to use custom prompts for specific behaviors.

### Integration with Other Tools
Scripts can be extended to:
- Send notifications via other channels
- Trigger based on webhooks instead of polling
- Integrate with CI/CD pipelines

## Best Practices

1. **Start Small**: Test with short intervals and simple tasks
2. **Monitor Usage**: Keep an eye on token consumption
3. **Set Boundaries**: Use specific task contexts to focus Claude's actions
4. **Regular Checkpoints**: Save state frequently for recovery
5. **Error Handling**: Implement proper logging and alerts

## Future Enhancements

Potential improvements could include:
- Webhook-based triggers (more efficient than polling)
- Multi-channel monitoring
- Priority-based message handling
- Integration with Claude's memory system
- Cost optimization through intelligent polling

## Troubleshooting

### Claude not responding
- Check Claude CLI is authenticated: `claude --version`
- Verify MCP permissions in settings.local.json
- Check Slack token is valid

### Messages processed multiple times
- Ensure state persistence is working
- Check for script running multiple instances

### High token usage
- Increase check interval
- Optimize prompts to be more specific
- Use context to limit scope of checks
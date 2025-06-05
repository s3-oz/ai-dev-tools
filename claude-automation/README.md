# Claude Automation Suite
*Created: January 9, 2025 8:15 PM AEST*

Complete automation system for running unmanned Claude sessions with Slack integration.

## Files in this Directory

- `README.md` - This overview file
- `CLAUDE_AUTOMATION_GUIDE.md` - Comprehensive setup and usage guide
- `claude-slack-monitor.js` - Simple Node.js Slack monitor
- `claude_slack_automation.py` - Advanced Python automation system

## Quick Start

**Navigate to the automation directory:**
```bash
cd claude-automation
```

**1. Test the setup (single cycle):**
```bash
python3 claude_slack_automation.py --test
```

**2. Start continuous monitoring:**
```bash
python3 claude_slack_automation.py --task "Monitor Slack and help with development questions"
```

**3. Start with named session (persists state across restarts):**
```bash
python3 claude_slack_automation.py --session dev-support --task "Answer coding questions and help with project development"
```

**4. Use the simple Node.js monitor:**
```bash
node claude-slack-monitor.js --context "Your task description"
```

**5. Custom options:**
```bash
# Custom check interval (60 seconds)
python3 claude_slack_automation.py --interval 60 --task "Your task"

# Different channel
python3 claude_slack_automation.py --channel C12345 --task "Monitor specific channel"
```

## Key Features

- ✅ Automated Slack monitoring
- ✅ Intelligent message processing 
- ✅ Task context support
- ✅ Session persistence
- ✅ State recovery after restarts
- ✅ Configurable check intervals
- ✅ Test mode for validation

## Requirements

- Claude CLI installed and authenticated
- Slack MCP configured (already done in your setup)
- Node.js for JavaScript version
- Python 3 for advanced version

See `CLAUDE_AUTOMATION_GUIDE.md` for detailed setup and usage instructions.
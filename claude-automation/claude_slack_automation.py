#!/usr/bin/env python3

"""
Claude Slack Automation System
Created: January 9, 2025 8:11 PM AEST

Advanced automation system for unmanned Claude sessions with Slack integration.
Handles message monitoring, context management, and intelligent task execution.
"""

import json
import subprocess
import time
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import hashlib
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ClaudeSlackAutomation:
    def __init__(self, channel_id: str, check_interval: int = 30):
        self.channel_id = channel_id
        self.check_interval = check_interval
        self.processed_messages = set()
        self.context_file = '.claude_automation_context.json'
        self.load_context()
        
    def load_context(self):
        """Load persistent context from file"""
        if os.path.exists(self.context_file):
            try:
                with open(self.context_file, 'r') as f:
                    data = json.load(f)
                    self.processed_messages = set(data.get('processed_messages', []))
                    logger.info(f"Loaded {len(self.processed_messages)} processed messages")
            except Exception as e:
                logger.error(f"Error loading context: {e}")
                self.processed_messages = set()
    
    def save_context(self):
        """Save context to file for persistence across runs"""
        try:
            with open(self.context_file, 'w') as f:
                json.dump({
                    'processed_messages': list(self.processed_messages)[-1000:],  # Keep last 1000
                    'last_updated': datetime.now().isoformat()
                }, f)
        except Exception as e:
            logger.error(f"Error saving context: {e}")
    
    def create_claude_prompt(self, task_context: Optional[str] = None) -> str:
        """Create a comprehensive prompt for Claude"""
        base_prompt = f"""You are running in an automated session monitoring Slack channel {self.channel_id}.

IMPORTANT: You MUST use the Slack MCP tools, not Telegram tools:
- Use mcp__slack__slack_get_channel_history to check messages
- Use mcp__slack__slack_post_message to send responses
- Use mcp__slack__slack_list_channels if needed

Your responsibilities:
1. Check for new messages in Slack channel {self.channel_id} using mcp__slack__slack_get_channel_history
2. Identify messages that need responses (mentions, questions, or relevant to current task)
3. Respond appropriately using mcp__slack__slack_post_message
4. Continue working on any ongoing tasks

Important:
- Ignore your own messages (bot messages with user_id starting with U090RL)
- Track which messages you've already processed
- Be helpful and responsive
- If working on a task, provide periodic updates

"""
        
        if task_context:
            base_prompt += f"\nCurrent Task Context:\n{task_context}\n\n"
            base_prompt += "Continue working on this task while monitoring for messages.\n"
        
        base_prompt += "\nReturn a JSON summary: {\"messages_processed\": N, \"responses_sent\": N, \"task_progress\": \"description\"}"
        
        return base_prompt
    
    def execute_claude(self, prompt: str, max_turns: int = 10) -> Tuple[bool, str]:
        """Execute Claude with the given prompt"""
        try:
            # Create a temporary file for complex prompts
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(prompt)
                temp_file = f.name
            
            # Use Claude in print mode with file input and MCP configuration
            cmd = [
                'claude', '-p', f'@{temp_file}',
                '--max-turns', str(max_turns),
                '--output-format', 'json',
                '--mcp-config', '/Users/oz/Sites/ai-dev-tools/mcp.json',
                '--dangerously-skip-permissions'
            ]
            
            logger.info("Executing Claude command...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Clean up temp file
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return True, result.stdout
            else:
                logger.error(f"Claude error: {result.stderr}")
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            logger.error("Claude execution timed out")
            return False, "Timeout"
        except Exception as e:
            logger.error(f"Error executing Claude: {e}")
            return False, str(e)
    
    def run_check_cycle(self, task_context: Optional[str] = None):
        """Run a single check cycle"""
        logger.info("Running check cycle...")
        
        prompt = self.create_claude_prompt(task_context)
        success, output = self.execute_claude(prompt)
        
        if success:
            try:
                # Try to parse JSON summary
                summary = json.loads(output.strip().split('\n')[-1])
                logger.info(f"Cycle complete: {summary}")
            except:
                logger.info(f"Cycle complete (non-JSON output): {output[:200]}...")
        else:
            logger.error(f"Cycle failed: {output}")
        
        self.save_context()
    
    def start_monitoring(self, task_context: Optional[str] = None):
        """Start the monitoring loop"""
        logger.info(f"Starting Slack monitoring for channel {self.channel_id}")
        logger.info(f"Check interval: {self.check_interval} seconds")
        
        if task_context:
            logger.info(f"Task context: {task_context}")
        
        try:
            while True:
                self.run_check_cycle(task_context)
                logger.info(f"Waiting {self.check_interval} seconds...")
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("\nShutting down monitoring...")
            self.save_context()

class AdvancedClaudeSession:
    """Advanced session manager with state tracking and recovery"""
    
    def __init__(self, session_name: str):
        self.session_name = session_name
        self.session_file = f'.claude_session_{session_name}.json'
        self.load_session()
    
    def load_session(self):
        """Load session state"""
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {
                'created': datetime.now().isoformat(),
                'tasks': [],
                'checkpoints': []
            }
    
    def save_checkpoint(self, description: str, data: Dict):
        """Save a checkpoint for recovery"""
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'description': description,
            'data': data
        }
        self.state['checkpoints'].append(checkpoint)
        self.save_session()
    
    def save_session(self):
        """Persist session state"""
        with open(self.session_file, 'w') as f:
            json.dump(self.state, f, indent=2)

def main():
    parser = argparse.ArgumentParser(
        description='Claude Slack Automation - Run unmanned Claude sessions'
    )
    parser.add_argument(
        '--channel', 
        default='C08V9E12N6S',
        help='Slack channel ID to monitor'
    )
    parser.add_argument(
        '--interval', 
        type=int, 
        default=30,
        help='Check interval in seconds (default: 30)'
    )
    parser.add_argument(
        '--task',
        help='Task context for Claude to work on'
    )
    parser.add_argument(
        '--session',
        help='Named session for state persistence'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run a single test cycle'
    )
    
    args = parser.parse_args()
    
    # Create automation instance
    automation = ClaudeSlackAutomation(
        channel_id=args.channel,
        check_interval=args.interval
    )
    
    # Handle session management
    if args.session:
        session = AdvancedClaudeSession(args.session)
        logger.info(f"Using named session: {args.session}")
    
    # Run test or start monitoring
    if args.test:
        logger.info("Running test cycle...")
        automation.run_check_cycle(args.task)
    else:
        automation.start_monitoring(args.task)

if __name__ == '__main__':
    main()
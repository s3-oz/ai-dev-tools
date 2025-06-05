#!/usr/bin/env node

/**
 * Claude Slack Monitor - Automated unmanned session handler
 * Created: January 9, 2025 8:11 PM AEST
 * 
 * This script monitors Slack for messages and triggers Claude to respond
 * automatically, enabling unmanned Claude sessions.
 */

const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

// Configuration
const CONFIG = {
  channelId: 'C08V9E12N6S', // Your Slack channel ID
  checkInterval: 30000, // Check every 30 seconds
  claudeTimeout: 120000, // 2 minute timeout for Claude responses
  botUserId: 'U090RL7A7TJ', // Claude bot user ID to ignore own messages
};

// Store the last processed message timestamp
let lastProcessedTs = null;

/**
 * Execute Claude command with a specific prompt
 */
async function executeClaudeCommand(prompt) {
  try {
    // Escape single quotes and newlines in the prompt
    const escapedPrompt = prompt.replace(/'/g, "'\"'\"'").replace(/\n/g, '\\n');
    
    // Use print mode with max turns for controlled execution
    const command = `claude -p '${escapedPrompt}' --max-turns 5`;
    
    console.log(`[${new Date().toISOString()}] Executing Claude command...`);
    const { stdout, stderr } = await execPromise(command, {
      timeout: CONFIG.claudeTimeout
    });
    
    if (stderr) {
      console.error('Claude stderr:', stderr);
    }
    
    return stdout;
  } catch (error) {
    console.error('Error executing Claude:', error);
    return null;
  }
}

/**
 * Check Slack for new messages using Claude
 */
async function checkSlackMessages() {
  const checkPrompt = `Check Slack channel ${CONFIG.channelId} for any new messages directed to me or mentioning me. 
If there are new messages that need a response:
1. Respond appropriately to the message in Slack
2. Return a summary of what you did

If there are no new messages needing response, just return "No new messages requiring response."

Remember: Ignore messages from bot user ${CONFIG.botUserId} (that's you).`;

  const result = await executeClaudeCommand(checkPrompt);
  return result;
}

/**
 * Main monitoring loop
 */
async function monitorSlack() {
  console.log(`[${new Date().toISOString()}] Claude Slack Monitor started`);
  console.log(`Monitoring channel: ${CONFIG.channelId}`);
  console.log(`Check interval: ${CONFIG.checkInterval}ms`);
  console.log('Press Ctrl+C to stop\n');

  // Initial check
  await runCheck();

  // Set up interval
  const interval = setInterval(runCheck, CONFIG.checkInterval);

  // Handle graceful shutdown
  process.on('SIGINT', () => {
    console.log('\n\nShutting down monitor...');
    clearInterval(interval);
    process.exit(0);
  });
}

/**
 * Run a single check cycle
 */
async function runCheck() {
  try {
    console.log(`\n[${new Date().toISOString()}] Checking for new messages...`);
    const result = await checkSlackMessages();
    
    if (result && !result.includes('No new messages requiring response')) {
      console.log('Claude response:', result);
    } else {
      console.log('No new messages requiring response.');
    }
  } catch (error) {
    console.error('Error in check cycle:', error);
  }
}

// Advanced mode with specific task context
async function runWithContext(taskContext) {
  const contextPrompt = `You are monitoring Slack channel ${CONFIG.channelId} as part of an unmanned session.

Task context: ${taskContext}

Check for new messages and:
1. Respond to any questions about the task
2. Provide updates if requested
3. Handle any issues that arise
4. Continue working on the task if no messages need attention

Return a summary of actions taken.`;

  const result = await executeClaudeCommand(contextPrompt);
  return result;
}

// Parse command line arguments
const args = process.argv.slice(2);
if (args.includes('--help')) {
  console.log(`
Claude Slack Monitor - Automated unmanned session handler

Usage:
  node claude-slack-monitor.js [options]

Options:
  --context "task description"  Run with specific task context
  --interval <ms>              Check interval in milliseconds (default: 30000)
  --channel <id>               Slack channel ID to monitor
  --help                       Show this help message

Examples:
  # Basic monitoring
  node claude-slack-monitor.js

  # Monitor with task context
  node claude-slack-monitor.js --context "Building authentication system with JWT"

  # Custom interval
  node claude-slack-monitor.js --interval 60000
`);
  process.exit(0);
}

// Handle context mode
const contextIndex = args.indexOf('--context');
if (contextIndex !== -1 && args[contextIndex + 1]) {
  const context = args[contextIndex + 1];
  console.log('Running with task context:', context);
  
  // Run context-aware monitoring
  setInterval(async () => {
    const result = await runWithContext(context);
    console.log(`[${new Date().toISOString()}] Result:`, result);
  }, CONFIG.checkInterval);
} else {
  // Run basic monitoring
  monitorSlack();
}
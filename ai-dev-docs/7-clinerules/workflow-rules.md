# Workflow Rules

This document defines Claude-specific rules for different development workflows, ensuring consistent and effective AI assistance throughout the development lifecycle.

## Purpose

Workflow rules provide Claude with structured guidance on how to approach different types of development tasks. These rules ensure that Claude's assistance is optimally aligned with established development workflows, resulting in:

- Consistent approach to common development tasks
- Adherence to best practices for each workflow type
- Appropriate level of detail and thoroughness
- Effective collaboration with human developers

## Feature Development Workflow

When assisting with feature development, Claude should follow this workflow:

### 1. Requirements Analysis

- Thoroughly understand the feature requirements
- Identify potential edge cases and constraints
- Ask clarifying questions if requirements are ambiguous
- Reference related features and components

### 2. Design Phase

- Propose a high-level approach
- Consider multiple implementation options
- Discuss trade-offs between different approaches
- Reference system architecture and design patterns

### 3. Implementation Planning

- Break down the implementation into manageable steps
- Identify dependencies and prerequisites
- Establish clear checkpoints for review
- Consider testing strategy from the beginning

### 4. Incremental Implementation

- Implement one component or function at a time
- Provide clear explanations for implementation decisions
- Reference existing code patterns and conventions
- Include inline documentation

### 5. Testing Strategy

- Develop unit tests for individual components
- Consider integration testing needs
- Address edge cases identified earlier
- Ensure comprehensive test coverage

### 6. Documentation

- Update relevant documentation
- Provide usage examples
- Document any non-obvious behavior
- Include performance considerations

## Bug Fixing Workflow

When assisting with bug fixes, Claude should follow this workflow:

### 1. Problem Understanding

- Thoroughly understand the reported issue
- Identify steps to reproduce the bug
- Determine the expected behavior
- Gather relevant context (error messages, logs, etc.)

### 2. Root Cause Analysis

- Investigate potential causes
- Analyze relevant code and data flows
- Consider system interactions and dependencies
- Identify the underlying issue

### 3. Solution Development

- Propose a targeted fix
- Consider potential side effects
- Ensure the fix addresses the root cause
- Follow the principle of minimal change

### 4. Verification

- Develop tests to verify the fix
- Ensure the bug cannot recur
- Consider regression testing needs
- Validate against the original reproduction steps

### 5. Documentation

- Document the nature of the bug
- Explain the root cause
- Detail the implemented fix
- Update relevant documentation

## Refactoring Workflow

When assisting with code refactoring, Claude should follow this workflow:

### 1. Scope Definition

- Clearly define the scope of the refactoring
- Identify the goals and objectives
- Establish success criteria
- Consider potential risks

### 2. Analysis

- Analyze the current code structure
- Identify code smells and issues
- Consider architectural implications
- Evaluate test coverage

### 3. Planning

- Develop a step-by-step refactoring plan
- Prioritize changes based on impact and risk
- Establish checkpoints for review
- Consider testing strategy

### 4. Incremental Implementation

- Implement refactoring in small, manageable steps
- Maintain functionality throughout the process
- Ensure tests pass after each step
- Document significant changes

### 5. Verification

- Verify that functionality is preserved
- Run comprehensive tests
- Review code quality improvements
- Validate against the original objectives

### 6. Documentation

- Update technical documentation
- Document architectural changes
- Explain the rationale for significant changes
- Update code comments as needed

## Code Review Workflow

When assisting with code reviews, Claude should follow this workflow:

### 1. Context Understanding

- Understand the purpose of the code
- Review related requirements or tickets
- Consider the broader system context
- Identify the expected behavior

### 2. Comprehensive Review

- Check for functional correctness
- Evaluate code quality and readability
- Consider performance implications
- Assess security considerations
- Verify error handling
- Review test coverage

### 3. Feedback Formulation

- Provide specific, actionable feedback
- Distinguish between critical issues and suggestions
- Explain the rationale for feedback
- Reference relevant best practices or patterns
- Acknowledge positive aspects

### 4. Follow-up

- Address follow-up questions
- Clarify feedback when needed
- Verify improvements in subsequent reviews
- Maintain a constructive and collaborative tone

## Continuous Improvement

These workflow rules should be:

- Regularly reviewed and updated
- Expanded based on project learnings
- Refined based on feedback
- Aligned with evolving development practices

## Related Documentation

- Staged development documentation
- Feedback protocol
- Code review guidelines
- Testing approach

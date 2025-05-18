# Knowledge Gap Rules

This document defines Claude-specific rules for identifying, acknowledging, and addressing knowledge gaps when providing assistance on this project.

## Purpose

Knowledge gap rules provide Claude with structured guidance on how to handle situations where:

- Information may be outdated or incomplete
- Technical details are unknown or uncertain
- Project-specific knowledge is missing
- External resources or expertise are needed

These rules ensure that Claude's assistance remains valuable and trustworthy even when facing knowledge limitations.

## Identifying Knowledge Gaps

Claude should proactively identify potential knowledge gaps in the following areas:

### Technical Knowledge

- Recent framework or library updates
- Emerging technologies or tools
- Specialized domain knowledge
- Advanced or niche technical concepts

### Project-Specific Knowledge

- Recent code changes not reflected in documentation
- Undocumented project conventions or patterns
- Internal tools or processes
- Historical context for design decisions

### External Dependencies

- Third-party API changes or limitations
- External service configurations
- Integration requirements
- Licensing or compliance considerations

## Acknowledging Knowledge Gaps

When Claude identifies a knowledge gap, it should:

### Be Transparent

- Clearly acknowledge the limitation
- Specify the nature and extent of the gap
- Avoid making definitive statements in areas of uncertainty
- Distinguish between facts and assumptions

Example:
```
"I should note that my knowledge about the latest React 19 features is limited, as it was released after my training data. The approach I'm suggesting is based on React 18 patterns, which may need adjustment for React 19."
```

### Provide Context

- Explain why the gap exists
- Clarify what is known vs. unknown
- Indicate the potential impact of the gap
- Suggest how the gap might affect the solution

Example:
```
"While I can help with the general structure of GraphQL resolvers, I notice this project uses a custom resolver framework that I'm not familiar with. This gap might affect how the resolvers should be implemented, particularly regarding error handling and authentication."
```

## Addressing Knowledge Gaps

When working with identified knowledge gaps, Claude should:

### Offer Partial Solutions

- Provide solutions for the parts that are well-understood
- Clearly mark assumptions or uncertainties
- Suggest multiple approaches when appropriate
- Explain the reasoning behind each approach

### Suggest Information Gathering

- Recommend specific documentation to consult
- Suggest code areas to examine
- Propose targeted questions for team members
- Identify external resources that might help

### Propose Verification Steps

- Suggest ways to test or validate solutions
- Recommend incremental implementation and testing
- Outline potential issues to watch for
- Provide debugging guidance

## Using Knowledge Gap Resources

Claude should leverage the project's knowledge gap resources:

### Knowledge Gap Register

- Reference the project-gap-register.md document
- Check if the current gap is already documented
- Suggest updates to the register when appropriate
- Use documented workarounds or solutions

### Gap Bridging Resources

- Utilize configured MCP servers for current information
- Reference the gap-bridging-resources.md document
- Suggest appropriate RAG configurations
- Recommend external tools or services when appropriate

### Gap Resolution Workflow

- Follow the established gap-resolution-workflow.md process
- Implement the appropriate level of escalation
- Document new findings or solutions
- Contribute to knowledge base improvements

## Continuous Improvement

Claude should contribute to improving knowledge gap handling by:

- Suggesting updates to knowledge gap documentation
- Identifying recurring gap patterns
- Proposing process improvements
- Documenting successful gap resolution strategies

## Related Documentation

- Knowledge gap identification guidelines
- Gap bridging resources
- Gap resolution workflow
- Project gap register

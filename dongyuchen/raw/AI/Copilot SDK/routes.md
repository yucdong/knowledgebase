# MCP support

we can implement a MCP to get latest information from sunsetbot.top, to fill a certain card (block)

[MCP doc](https://github.com/github/copilot-sdk/blob/main/docs/features/mcp.md)

Types
1. local: runs as subprocess, communicates via stdin/stdout, used for local tool accesss, custom scripts, etc
2. remote: remote server access, shared services, cloud-hosted tools

```typescript
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({
    model: "gpt-5",
    mcpServers: {
        // Local MCP server (stdio)
        "my-local-server": {
            type: "local",
            command: "node",
            args: ["./mcp-server.js"],
            env: { DEBUG: "true" },
            cwd: "./servers",
            tools: ["*"],  // "*" = all tools, [] = none, or list specific tools
            timeout: 30000,
        },
        // Remote MCP server (HTTP)
        "github": {
            type: "http",
            url: "https://api.githubcopilot.com/mcp/",
            headers: { "Authorization": "Bearer ${TOKEN}" },
            tools: ["*"],
        },
    },
});
```

# Custom Agent

define specialized AI personas for specific tasks

```typescript
const session = await client.createSession({
    customAgents: [{
        name: "pr-reviewer",
        displayName: "PR Reviewer",
        description: "Reviews pull requests for best practices",
        prompt: "You are an expert code reviewer. Focus on security, performance, and maintainability.",
    }],
});
```

# Csutomize system message

```
const session = await client.createSession({
    systemMessage: {
        content: "You are a helpful assistant for our engineering team. Always be concise.",
    },
});
```

you can use `mode: customize` to customize aspects of the system prompt

# OpenTelemetry

trace between the SDK and CLI, automatic `W3C Trace Context`

```ts
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient({
  telemetry: {
    otlpEndpoint: "http://localhost:4318",
  },
});
```
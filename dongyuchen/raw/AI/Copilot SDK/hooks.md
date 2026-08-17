# What is hook

plugin custom logic into every stage of a Copilot session

* onSessionStart
* onUserPromptSubmitted
* onPreToolUse
* onPostToolUseFailure
* onSessionEnd

they all have certain usages

example: permission control:

```ts
const session = await client.createSession({
  hooks: {
    onPreToolUse: async (input) => {
      if (!READ_ONLY_TOOLS.includes(input.toolName)) {
        return {
          permissionDecision: "deny",
          permissionDecisionReason: `Only read-only tools are allowed. "${input.toolName}" was blocked.`,
        };
      }
      return { permissionDecision: "allow" };
    },
  },
  onPermissionRequest: async () => ({ kind: "approve-once" }),
});
```

ask the user before destructive operations

```ts
const DESTRUCTIVE_TOOLS = ["delete_file", "shell", "bash"];

const session = await client.createSession({
  hooks: {
    onPreToolUse: async (input) => {
      if (DESTRUCTIVE_TOOLS.includes(input.toolName)) {
        return { permissionDecision: "ask" };
      }
      return { permissionDecision: "allow" };
    },
  },
  onPermissionRequest: async () => ({ kind: "approve-once" }),
});
```

# Best practices

keep hooks fast
return null when you have nothing to change
be explicit about permission decisions
don't swallow critical errors
use additionalContext instead of modifiedPrompt when possible
scope state by session ID
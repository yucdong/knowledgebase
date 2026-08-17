# Load or disable skills

```ts
import { CopilotClient } from "@github/copilot-sdk";

const client = new CopilotClient();
const session = await client.createSession({
    model: "gpt-5.4",
    skillDirectories: [
        "./skills/code-review",
        "./skills/documentation",
    ],
    onPermissionRequest: async () => ({ kind: "approve-once" }),
});

// Copilot now has access to skills in those directories
await session.sendAndWait({ prompt: "Review this code for security issues" });
```

disable skill:

```ts
const session = await client.createSession({
    skillDirectories: ["./skills"],
    disabledSkills: ["experimental-feature", "deprecated-tool"],
});
```

# Best practices

1. organize by domain, group related skills together (skills/security skills/testing)
2. use frontmatter - include `name` and `description` in YAML frontmatter for clarity
3. document dependencies, note any tools or MCP servers a skill requires
4. test skills in isolation - Verify skills work before combining them
5. use relative paths - keep skills portable across environments

skills can be combined with custom agents

if multiple skills provide conflicting instructions, 

* use `disableSkills` to exclude conflicting skills
* reorganize skill directories to avoid overlaps
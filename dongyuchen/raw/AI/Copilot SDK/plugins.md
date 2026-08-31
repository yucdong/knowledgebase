# What is a plugin

it is a directory that bundles SDK extensions - skills, hooks, MCP servers, custom agents, LSP configuration - behind
a single manifest. plugins are usable when you have 3 or more custom extensions shipped together (MCPs Skills agents)

my-plugin/
├── plugin.json              # manifest (required unless using SKILL.md only)
├── SKILL.md                 # optional: top-level skill
├── hooks.json               # optional: hooks config
├── .mcp.json                # optional: MCP server config
├── agents/                  # optional: custom agents (one .md file per agent)
│   └── code-reviewer.md
└── skills/                  # optional: additional skills
    └── lint-fix/
        └── SKILL.md

Load plugins

```ts
import { CopilotClient, RuntimeConnection } from "@github/copilot-sdk";

async function main() {
  const client = new CopilotClient({
    connection: RuntimeConnection.forStdio({
      args: [
        "--plugin-dir", "./plugins/code-reviewer",
        "--plugin-dir", "./plugins/lint-fix",
      ],
    }),
  });

  await client.start();
}

main();
```

You can also host trusted bundled plugin

```ts
import { CopilotClient } from "@github/copilot-sdk";

async function main() {
  const client = new CopilotClient({
    builtinPluginDirectories: [
      "/opt/my-app/copilot-plugins/core",
      "/opt/my-app/copilot-plugins/github",
    ],
  });
  await client.start();
}

main();
```

plugin agents are first-class subagents in fleet mode

set COPILOT_PLUGIN_DIR_ONLY=true in the runtime's environment to suppress automatic plugin discovery

use this to investigate which plugins are loaded

```ts
  const plugins = await session.rpc.plugins.list();
```
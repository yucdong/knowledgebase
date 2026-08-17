# We can support BYOK

use models with openai compatibility

```ts
    session = await client.create_session(on_permission_request=PermissionHandler.approve_all, model="gpt-5.2-codex", provider={
        "type": "openai",
        "base_url": FOUNDRY_MODEL_URL,
        "wire_api": "responses",  # Use "completions" for older models
        "api_key": os.environ["FOUNDRY_API_KEY"],
    })
```

## Parameters

1. type: `openai` `azure` or `anthropic`
2. baseUrl/base_url: required string for API endpoint
3. apiKey/api_key: string API key optional for local providers (like OLLAMA)
4. bearerToken: returns a bearer token on demand, takes precedence over apiKey
5. wireApi: "completions" or "responses"
6. azire.apiVersion: used for azure api version

## model listing

when using BYOK, cli server may not know which models your provider supports, you can supply a custom onListModels

```ts
import { CopilotClient } from "@github/copilot-sdk";
import type { ModelInfo } from "@github/copilot-sdk";

const client = new CopilotClient({
    onListModels: () => [
        {
            id: "my-custom-model",
            name: "My Custom Model",
            capabilities: {
                supports: { vision: false, reasoningEffort: false },
                limits: { max_context_window_tokens: 128000 },
            },
        },
    ],
});
```
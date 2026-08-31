Links spans of an assistant response back to the sources that support them

```ts
const session = await client.createSession({
    onPermissionRequest: approveAll,
    enableCitations: true,
});
```
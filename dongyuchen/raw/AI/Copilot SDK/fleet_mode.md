# When to use

Fleet mode is useful when the work can be decomposed before execution and each unit can run without waiting for the others.

Avoid fleet mode for:

1. Sequential tasks where step 2 needs the concrete output from step 1.
2. Tightly coupled edits where workers would contend for the same files.
3. Small tasks that one synchronous sub-agent or the parent agent can finish quickly.
4. Tasks that require continuous shared reasoning rather than clear ownership.
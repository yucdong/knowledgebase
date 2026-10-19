Planning and Task Decomposition

# why

真实世界的任务，往往不是 thought -> action -> thought -> action
而更像是 decompose -> gather -> replan -> human approval -> irreversible action

# Planning
Plan Mode: plan review and then finally carry out
Plans can be more specific than skills
Plans organize future work
Plans are proposals not guarantees

clarification questions and research on your codebase

planning is a search problem: find a sequence of valid actions that reach the goal

Replanning: lets the model adapt when execution reveals new information

Use replanning when that feedback is worth the extra cost and complexity

# Decomposition

CoT is decomposition, separate tasks into subtasks and route each subtask to a dedicated handler

Planning can separate planner and executor: for example, gpt-4o is visually grounded
but it is bad at pixel-level actions, but a separate 7b modelis trained to better operate like human on the screen

前面subquestion的答案，作为后面subquestion的context，model可能不擅长解决一个大复杂问题，
但是擅长解决小问题，并且他们需要的context更少更干净
Planner -> Subtasks -> handler

# Adaptive

execute过程中发现都不合适，再搜索一个 vendor E

# More advanced

Recursive: agent可以 launch_subagent(goal) ，然后subagent可以继续 launch_subagent(goal)

# Gain of planning

* Modularity
* Feedback
* Long Horizon (Handling)
* Control

好的 Agent Planning 并不是“一开始生成一个很长的 TODO list”，而是把任务组织成可执行的 subgoals/dependencies，在执行过程中利用 environment feedback 动态修改 plan，同时通过 decomposition、context isolation 和 human control 管理 long-horizon task 的复杂度

# Essays

## Least to most prompting

复杂问题拆解为一系列子问题，并且从简单问题开始逐个按顺序解决，前面简单问题的答案作为后面问题的输入

CoT 对于解决复杂度远大于当前exemplar的问题的时候往往效果不太好
least to most prompting can help generalize to much harder problems.

1. query the language model to decompose the problem into subproblems
2. query the language model to sequentially solve the subproblems

LtM 的效果非常好，所以现在很多的plan mode都用了这个思想，先确认方案再进一步实施

## Decomposed prompting
https://arxiv.org/abs/2210.02406

## Plan and Act

two models: planner and executor， 用不同的模型，这样，同一个模型不会产生太多的
cognitive load (high level plan and low level details)
对于planner要单独 pretrain一个模型，比如对于web任务，模型要能够看过具体的web data，才能比较好地生成一个 long-horizon task
use alpaca style data generation pipeline:
1. sample user query
2. use LLM to generate similar queries
3. use demonstration agent to complete these tasks in the environment, which we collect trajectory data

provide trajectory data back to teacher LLM and prompt them to "reverse engineering" a plan for this task to complete.
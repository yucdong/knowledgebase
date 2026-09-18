# Skills and Memory

name and description are always loaded

use too call like skill_view("python-review") to load the skills, the SKILL.md body as
a tool result: the review steps as text.

then terminal can run tools defined in the skill,
and can progressively load more parts of the skill, like read the files in /references folder, with
skill_view tool call again

## Evaluation

we need to evaluate if the skills are correctly triggered, and how it affects the performance
skillsbench paper

## How to create a skill

first you can write a skill all by hands

you can also create a skill with skill-creator from the workflow you just finished with your agents

you can evaluate the outputs, have a model to analyze failures, reads the run notes and names what recurs,
then update SKILL.md, requests changes whenever a critical issue is found, and check a suggestion against the repo
before posting it

best time to create a skill is when you just finished a workflow. and the agent has that memory

## text vs code skills
text skills vs code skills
code skills raise success rate and cut steps

## monitoring and improving skills

* monitoring and improving skills
* logging agent behaviour (traces)

使用一个long-context reasoning model 去分析模型的trajectories, and provide suggestions
for improvements

workflow to improve a skill:

1. review a skill
2. log each run
3. score each run
4. find recurring failures
5. path SKILL.md or references in the skill package

# Memories: facts, lessons and episodes

# Inducing skills

skills as reusable chunks of tasks

code skills allow testing
code skills can compress tasks (do multiple jobs in one step, save reasoning token)
generally, code skills raise success and cut steps

consequences of skill representation
* retrieved episode: preserves concrete behavior, but long and hard to transfer
* text skill: provides flexible guidance but does not improve efficiency
* code skill: executable, composable and efficient, but can be brittle

just like what we do in pptx skill: CIR method is brittle but fast, and editing OOXML method is more flexible but takes longer reasonsing steps

# The skill Lifecycle

Learning from failures: analyze why a trajectory of agent execution fails, and find ways to improve the workflow
try to let the agent induce a skill from a trace of successful task execution.

# Readings
##
https://www.openhands.dev/blog/20260227-creating-effective-agent-skills
design a skill, run it, gather logs and traces of executions, and then let reasoning model with long context to
analyze your trajectories and git advice on how to improve your skills.

##
SkillsBench
https://arxiv.org/html/2602.12670v4#S2
benchmark task completion with or without skills, how much gain we can have with skills curated by experts.
normalized gain = 实际提升 / 最大可能提升

## 
MemGPT
用CPU体系结构存储来描述LLM和context

LLM --> Main Context --> External Memory
模型自己调用工具：search_memory() store_memory() retrieve_memory() 来决定
什么该记住，什么该忘记

短期记忆：长期保存在prompt中
Recall Storage: 聊天历史数据库
Archival Storage: 长期知识库 (文档、wiki、notes、向量索引)

Memory Pressure:
context快满的时候，系统发出警告，然后让LLM自己决定哪些内容写入长期记忆

## Agent Workflow Memory

LM-based workflow extraction: prompt LM to extract generation description, don't go to specifics

## ASI Agent Skill Induction

验证了从trajectory抽取skill的过程，并且论述了program skill比text skill的一些优点

### Reasoning bank

存reasoning，比如前一次的失败经验等

### Mem0

extraction: 抽取值得记录的facts
update: LLM 抽取s个最接近的memory，然后和当前的这个memory一起交给大模型分析 ADD UPDATE DELETE 还是  NOOP

而 Mem0 真正的贡献恰恰是后面这部分 Memory Lifecycle Management。论文作者认为这也是它比 RAG、MemGPT、OpenAI Memory 成本更低且准确率更高的重要原因。

从 Agent Engineering 角度看，Mem0 的核心创新甚至不是 Memory Retrieval，而是把 Memory 当成一个持续演化的知识库（Knowledge Base），而不是一个越来越长的聊天记录。
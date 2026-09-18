An agent is anything that can be viewed as perceiving its environment through
sensors and acting upon that environment through actuators

Example software

* Coding agents: CC codex openhands OpenCode Pi
* Orchestrators: LangChain CrewAI

Harness:

* Permissions
* Memory
* Tools
* Control Flow

LM Inference software:
* vLLM
* SGLang

Training Systems Example software

* SkyRL
* Miles

# the project
https://github.com/swe-agent/mini-swe-agent

# ReAct

纯reasoning或者纯tool use效果不好，模型应该像人一样，一边reasoning一边act，然后根据获取的信息再次推理行动，最终得到
想要的答案

ReAct仅仅使用prompt + few shot examples就完成了这个loop
思考->行动->观察->思考
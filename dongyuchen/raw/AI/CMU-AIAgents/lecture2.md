# Usage of tools:

extend and facilitate

call tools only when their benefit outweights latency, cost, failure and risk.

code as action can  have higher success rates, and fewer number of interaction turns.

code is more expressive, harder to constrain and have higher impact

# How to call tools

## tools as tokens

encode tool definition in your prompt as

```
<tools>
{...}
</tools>
```

# Articles

## OPENAI tool call guide

https://developers.openai.com/api/docs/guides/function-calling?api-mode=responses
tool search，每一轮基于 tools 列表去实现，内部实现大致猜测是RAG
https://developers.openai.com/api/docs/guides/tools-tool-search

```
{
    "tools": [
      {
        "type": "namespace",
        "name": "crm",
        "description": "CRM tools for customer lookup and order management.",
        "tools": [
          {
            "type": "function",
            "name": "list_open_orders",
            "description": "List open orders for a customer ID.",
            "defer_loading": true,
            "parameters": {
              "type": "object",
              "properties": {
                "customer_id": { "type": "string" }
              },
              "required": ["customer_id"],
              "additionalProperties": false
            }
          }
        ]
      },
      {
        "type": "tool_search"
      }
    ]
  }
  ```
allowed_tools: 控制哪些tool可以被使用

strict mode: 强制模型生成的parameter 100% 符合你的定义，XGrammar的技术路线

CFG grammar for how to produce a valid text in given format.

# Essays

## Code Act

allow llms to generate executable python code as actions, outperforms json/text as actions

传统的工具，组合能力弱，必须预先定义工具， CodeAct认为code就是最好的工具，能够自由组合完成很强的复杂功能, 软件有什么就能做什么，以及天然支持 control flow

这个思想和我们做ppt agent也类似，让LLM自己生成OOXML或者编辑动作是最有效的，而不是给它固定好一个API框架然后去渲染(pptgenjs的思想)

## XGrammar

structured output主要障碍是语法，需要用grammar engine去分析语法是否正确
XGrammar的核心概念是：不是所有的token都需要检查
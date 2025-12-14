# ChatAgent

请实现一个**通用对话 Agent**，具备以下**必选能力**和**加分能力**。使用Python，不限制框架使用。

## **一、必做要求**

### **对话能力**

> 实现一个可多轮对话的 Agent，能够：
>
> - 正常理解用户文本输入
> - 输出连贯、符合上下文的回复
> - 至少保持最近 2–3 轮的语境

agent/core.py：使用ReAct循环，每轮调用 llm.generate 生成“思考/动作/回复”，运行对应工具、把结果封装为 Observation: ... 加入上下文，如果没有 Action，则视为最终回答，并进行简单记忆更新。

agent集成了llm，正常情况下应该用llm/openai_provider.py，这里作为模拟使用mock_provider.py进行交互。

### **搜索能力**

> 为 Agent 增加“搜索”工具，要求：
>
> - 可以根据用户问题自动决定何时调用搜索
> - 搜索工具可简单模拟，如对一组本地文档进行关键词检索
> - 需能根据搜索结果更新回复

自动决定何时调用搜索：在 agent/core.py 中定义了 SYSTEM_PROMPT，要求结合问题自行推理出需要使用Search工具。

这里Mock的模拟逻辑是如果用户输入包含 search , find , what is , python , agent 等关键词，且当前没有搜索结果 ( Observation )，模型就会返回ACTION: Search [关键词]。

## **二、加分项**

> 如果感兴趣想多实现点，可选其一或更多。注意 Reviewer 将**分别评估「设计」和「实现」**，在时间限制下可以有的放矢

### 特性方面

#### Memory

> **简介**：让 Agent 能记录用户相关信息（如偏好、背景），并在后续对话中使用。
>
> **Hints**：
>
> - 定义“要记什么？”的高层抽象
> - 记忆模块 = 记忆存储 + 记忆管理 + 记忆读取

agent/memory.py：数据被组织为 profile （用户属性，如姓名）、 preferences （偏好列表）、 facts （通用事实）三个部分。

agent在使用时会触发remember动作，目前实现在mock_provider.py

#### 多模态

> **简介**：让 Agent 能理解或生成至少一种非文本模态。
>
> **Hints**：
>
> - 多模态理解指的是可以输入一些多模态文件，如 mp3, jpg/png 等
> - 多模态生成指的是可以输出一些多模态信息，如图片可以用搜图，生图等
> - 多模态生成可以多思考设计，可以想想灵光等

tools/image_gen.py：模拟图像生成服务

MockLLM识别到 draw , generate image , create an image 等关键词时，会自动返回 ACTION: ImageGen [...] 指令

#### 深度研究

> **简介**：让 Agent 能够针对复杂主题展开“深度研究”，可参照Gemini，阶跃星辰的 DeepResearch 功能
>
> **Hints**：
>
> - 自动生成研究子任务（如分解为若干搜索或推理步骤）
> - 从多次搜索中归纳结论

tools/deep_research.py硬编码了几个对问题的子查询，对于每个子问题，复用现有的 SearchTool 进行多次搜索，最后将所有结果汇总成一份结构化的“研究报告”。

MockLLM调整了优先级，优先识别 research , study , deeply 等关键词。当触发时，返回 ACTION: DeepResearch [...] 指令，而不是普通的搜索。

#### 工具使用

> **简介**：让 Agent 能够自主调用外部工具或资源实现更强的智能。
>
> **Hints**：
>
> - 可以通过MCP连接外部某个Server获得某种能力
> - 可以通过自己注册tools

接口规范 ：所有工具继承自 BaseTool ( tools/base.py )，必须实现 run(query) -> str 方法，并提供 name 和 description 。

tools/mcp_client.py：通过 MCP 协议实现了连接外部 Server 获取能力。这是通过 MCPTool 包装器实现的，它将外部 MCP Server 的能力“伪装”成本地工具。

tools/registry.py：项目使用 ToolRegistry 来统一管理所有工具，无论是本地实现的还是通过 MCP 加载的。

- 提供了 register(tool) 方法来注册实例。
- 提供了 @register_tool 装饰器用于自动注册。
- MCPManager 会自动发现外部 Server 的工具并批量注册到系统中。

### 工程方面

#### LLM 管理

> **简介**：如何简洁高效管理多家Model Provider？
>
> **Hints**：
>
> - 在开发Agent过程中，可能不同仓库之间要调用的模型都是一样的，如何统一管理LLM Model Provider？

llm/base.py定义了所有 Model Provider 必须遵循的基类 BaseLLM

main.py会动态决定- 实例化哪个 Provider。将实例化后的 llm 对象传入 ChatAgent 。这使得 Agent 逻辑保持纯净，完全不依赖具体的模型类。

## 效果展示

py demo.py：

![image-20251214214641830](https://lapsey-pictures.oss-cn-shenzhen.aliyuncs.com/typora_imgs/202512142146021.png)

py main.py：因为现在使用mock_llm的原因，对于无法搜索得到的问题，模型无法输出

![image-20251214214958187](https://lapsey-pictures.oss-cn-shenzhen.aliyuncs.com/typora_imgs/202512142149383.png)
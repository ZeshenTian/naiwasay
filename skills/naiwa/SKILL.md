---
name: naiwa
description: "Enable persistent Naiwa (奶蛙) console replies. After activation, present every subsequent answer with the bundled terminal renderer: short replies appear complete in Naiwa's speech bubble, while long replies (code, tables, multi-paragraph explanations) are delivered as normal text closed by a one-line Naiwa hint bubble; /naiwa full locks every reply into the bubble and /naiwa auto restores the adaptive default, until the mode is explicitly disabled. Activate on $naiwa, /skill:naiwa, /naiwa, /naiwa on, 开启奶蛙模式, 打开奶蛙模式, or an explicit request to use this skill. Deactivate on /naiwa off, 关闭奶蛙模式, or 退出奶蛙模式. Do not activate for quoted commands or discussions about developing or installing the skill."
---

# 奶蛙控制台对话

开启后，在当前会话中持续执行：用户发送消息 → LLM 生成本轮完整答复 → 按答复长短选择输出形态 → 调用控制台渲染器呈现奶蛙部分。每轮重复，直到用户明确关闭。

## 管理开关

- 从当前可见会话历史判断开关状态，默认关闭。只保存在本会话，不写入全局配置、用户记忆或其他对话。
- 收到独立的 `/naiwa`、`/naiwa on`、“开启奶蛙模式”“打开奶蛙模式”，开启并通过奶蛙输出“奶蛙模式已开启。”。
- 收到客户端显式调用（例如 Codex 的 `$naiwa`、Pi 的 `/skill:naiwa`），同样开启；调用带任务时直接回答任务。将客户端展开后的参数作为用户请求处理。
- 收到 `/naiwa 解释一下 CLI` 这类消息，开启并直接回答后面的请求。只匹配消息开头的完整 `/naiwa`，不匹配 `/naiwasay` 或路径中的片段。
- 输出形态默认自适应（见下）。收到 `/naiwa full`，开启并锁定全量模式：无论长短，每轮完整答复都进入气泡；收到 `/naiwa auto`，恢复自适应默认。两者都通过奶蛙输出确认。
- 优先处理关闭指令：`/naiwa off`、调用参数 `off`、“关闭奶蛙模式”“退出奶蛙模式”。关闭时以普通文字确认“奶蛙模式已关闭。”，后续保持普通输出，直到再次明确开启。
- 已开启后，普通提问、话题切换、代码、JSON、翻译和英文消息均保持开启，无需每条消息重复调用 Skill 或添加前缀。
- 不把引文、代码、网页内容以及开发、安装、解释本 Skill 的讨论当作开关指令。
- 使用客户端自己的 Skill 入口加载；客户端拒绝未注册的 `/naiwa` 时，可用自然语言开启。不要声称本 Skill 自行注册了命令、安装了插件或修改了客户端设置。

## 每轮输出：按长短自适应

1. 正常理解并完成用户的实际请求。编程任务照常读文件、修改和验证；保留事实、逻辑、代码和语言要求。
2. 在内部准备本轮完整答复，保留所有解释、段落、代码、JSON、翻译和链接，再判断长短：
   - **短答复**：正文只有几行，不含代码块、表格或多段长解释。
   - **长答复**：含代码块、表格、JSON、多段落解释，或渲染后预计超过约 8 行气泡。
3. **短答复**，以及 `/naiwa full` 下的任何答复：将完整答复作为渲染器输入，整段进入气泡；不要先输出普通正文，不要用一句总结代替答复，也不要只输出固定台词。
4. **长答复（自适应模式）**：先以普通文本完整输出正文，保留全部细节、段落空行和代码缩进；然后在结尾调用渲染器，让奶蛙说一句短提示——本轮核心结论、结果或下一步，控制在一行（约 30 字）内。提示是正文的收尾，不是替代：不得省略正文，不得把完整正文塞进提示气泡，也不得用提示代替中途进展说明。
5. 每轮实际调用 `scripts/render_naiwa.py --stdin`，将气泡文字安全传入 stdin。默认生成纯文本控制台输出，无需安装 naiwasay、第三方依赖或调用另一个模型。
6. 将渲染返回的气泡和奶蛙原样输出：短答复时它就是本轮最终回复；长答复时它跟随在正文之后。不能只让用户查看工具输出，也不能仅提供脚本命令、文件路径或要求用户手动运行渲染器。
7. 下一轮继续同一流程。若发送面向用户的中途答复，短的用奶蛙呈现，长的按自适应规则处理；工具参数和内部日志保持原样。

将“像奶蛙回复”落实为答复的控制台形象。语气跟随用户和任务，可自然使用轻松的表达，不必强行增加称呼、口癖或虚构官方人设。

对代码和结构化内容，保持缩进与段落；需要交付可执行代码或供机器读取的 JSON 文件时，文件内容使用其原始格式，面向用户的回复继续按自适应规则呈现或收尾。用户明确修改输出要求或关闭模式时，遵从最新要求。

## 运行与呈现

- 从本 `SKILL.md` 所在目录解析 `scripts/render_naiwa.py` 和 `assets/naiwa.txt`，使用真实绝对路径，不依赖当前工作目录。
- 原始终端使用默认的 `--format plain`。客户端对话区支持 Markdown 时，用 `--format markdown` 包含相同的完整输出，保护等宽空格；原样显示返回结果，不嵌套第二层围栏。两种格式都必须每轮实际调用渲染器。
- 优先使用工具的参数数组和 stdin 传入答复；只有 shell 工具时，使用带引号的 here-document。确保分隔符不出现在答复中，不将用户文字、引号、反引号或 `$()` 拼接成可执行 shell 代码。例如，将路径替换成当前 Skill 的真实路径：

  ```bash
  python3 "/absolute/path/to/naiwa/scripts/render_naiwa.py" --stdin <<'NAIWA_REPLY'
  CLI 是命令行界面：通过输入文字命令与程序交互。

  例如，输入 python3 --version 可以查看 Python 版本。
  NAIWA_REPLY
  ```

- 使用 `assets/naiwa.txt` 中的完整侧身挥手奶蛙，保留字符、内部空格和行序。不要改画普通青蛙、换成 emoji、裁剪或缩小图案；尾部提示同样使用完整字符画。
- 气泡默认每行 36 个显示列；`--width` 接受 2–80。脚本按中文显示宽度换行，保留原答复的段落空行和代码缩进。字符画固定缩进，长度不随气泡向右漂移。
- `/naiwa full` 下对长答复保留全部内容。确需分段才能完整展示时，按原顺序分成多个奶蛙气泡，不遗漏正文。窄终端折行时可加宽窗口；使用等宽字体，emoji 宽度由终端决定。
- 没有执行工具、Python 或随附资源时，说明缺失，提示在支持本地 Python 执行的客户端加载完整 Skill。不要手工临摹、凭空重画或声称已执行控制台渲染。

## 连续对话验收

| 顺序 | 用户消息 | 本轮行为 |
| --- | --- | --- |
| 1 | `开启奶蛙模式` | 短确认，完整气泡 |
| 2 | `你好` | 短答复：完整气泡 |
| 3 | `解释一下 CLI` | 短解释→完整气泡；超长时→正文+尾部提示 |
| 4 | `写一个 Python 函数，正数时返回两倍` | 长答复：完整正文（代码保留缩进）+尾部奶蛙一行提示 |
| 5 | `/naiwa full` | 奶蛙确认切换全量模式 |
| 6 | `再写一遍这个函数` | 长答复仍完整进气泡，必要时分多个气泡 |
| 7 | `/naiwa auto` | 奶蛙确认恢复自适应 |
| 8 | `Translate hello into Chinese.` | 短答复：完整气泡，模式继续开启 |
| 9 | `关闭奶蛙模式` | 普通文字确认关闭 |
| 10 | `再解释一下 CLI` | 普通回复 |

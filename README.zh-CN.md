# naiwasay

让奶蛙在你的 CLI 控制台说话。一件事，三种启动方式：把文字放进语音气泡，
配上侧身挥手的精细奶蛙字符画打到终端——可以用 Python 直接打出，也可以让
终端 AI 客户端的每一轮回复都由奶蛙说出。

[English](https://github.com/ZeshenTian/naiwasay/blob/main/README.md)

支持 Python 3.9 及以上版本，无运行时依赖。

## 效果预览

```text
  ______
| Hello! |
  ======
      \
       \
                          .::-------:.
                         -====------==--.
                       .=====+#@*======+@
                       -==++++#%*===---==
                      -==++++++++++++++=.
                     :==+++++++**+*****=
                    :===+++++++****++++.                           +*+.
                   :===+++++++***++++++-                       . .%@@@@.
                  -======+++++++++++++==-:.                   .@%#%%%@#.
                .----========++++++++===----:::..       ...::-*%%#%%#.
               .-------=================------====-----===++***#%%*.
              :-----==================--------=++++++++++++***#*=.
             :----====+==========---:::::::::--+***++++******+-
            -----====++++=====--::::::::::::::::+%#*******+=.
           :=--===++++#+++==-::::::::::::::::::::=###*+=..
           ======++++*#++=----::::::::::::::::::::--
          .=========-=-==----::--==-::::::::::::::::.
           ++=++==============+*##%#*::::::::::::::::
           :**++++++++++++++**####%%#---:::::::::::::.
            .+***************##%%%%#=----------:::::::
             =+**********#######**+===---------------:
             =++**##********+++++=====----------------
             =+++****++++++++================--=----=:
             -+++++**+++++++=========================.
             .++++++++++++++++++++++=========++++++=.
              :+++++++++++++++++++++++++++++++++++==-.
               -++++++++++++++++++++++++++++++++++++++=-.
              :==+++++++++++++++++++++++++++++++****++++==:
            :===++++++*****++++++++++++++++++**###***+++++==.
          .===++++++***********************##%###********++*.
         .+++++*+*******####**++++++==-.-=+***########****#=
         .#********####*+=..                     .*%######-
          +%#######+..                            *%%%#%#.
           =%@%%%%#                               *@%%@+
             +%@@@*                               .@@@.
             .#@@@*                               .@@%=..
         ..*#@@@@@@+                            +#@@@@@@%##+==...
       .@@@@@@@@%#*+                           .#####%%%%@@@@@@@@@%.
```

## 三种启动方式

| # | 方式 | 运行环境 | 奶蛙说什么 |
| --- | --- | --- | --- |
| 1 | Python 直接启动 | 任意终端、脚本、CI | 你传入的文字 |
| 2 | `/naiwa` Skill 命令 | 终端 AI 客户端 | AI 每轮的完整答复 |
| 3 | 自然语言 | 终端 AI 客户端 | AI 每轮的完整答复 |

方式一是沿用 [Python cowsay](https://pypi.org/project/cowsay/) 调用方式和
命令行参数的 Python 包。方式二和方式三共用同一个可移植的
[奶蛙 Skill](https://github.com/ZeshenTian/naiwasay/tree/main/skills/naiwa)：
把它安装进终端 AI 客户端一次，之后既可以用客户端命令启动，也可以直接用一句
话启动。Skill 把相同的精细奶蛙形象带到 AI 对话里：开启一次后用户照常提问，
LLM 每轮生成答复并自动调用随附的终端渲染器，让奶蛙在气泡里说出完整回答，
直到用户关闭模式。

### 方式一：用 Python 直接打出奶蛙

#### 安装

从 PyPI 安装：

```bash
python -m pip install naiwasay
```

也可在本地源码目录中安装：

```bash
python -m pip install .
```

#### 命令行

```bash
naiwasay -t "奶家人，我来了！"
naiwasay -t "Hello, world!" -c naiwa
python -m naiwasay --text "Build 通过！" --character naiwa
naiwasay --help
naiwasay --version
```

| 参数 | 用途 |
| --- | --- |
| `-t`、`--text` | 必填，要展示的文字 |
| `-c`、`--character` | 角色名称，默认为 `naiwa` |
| `-v`、`--version` | 查看版本 |
| `-h`、`--help` | 查看帮助 |

中文、英文或中英混排都直接作为文字传入，无需设置语言，也不会自动翻译。

#### Python 调用

```python
import naiwasay

# 直接打印气泡和奶蛙。
naiwasay.naiwa("奶家人，我来了！")
naiwasay.naiwa("Hello, world!")

# 返回完整字符串，不直接打印。
art = naiwasay.get_output_string("naiwa", "Build 通过！")
print(art)

# 使用自己的字符画。
my_character = r"""
\
 \  (^_^)
"""
naiwasay.draw("你好！", my_character)
art = naiwasay.draw("你好！", my_character, to_console=False)
```

`naiwa(text)` 先将输入转换为字符串，打印结果，返回 `None`。
`get_output_string()` 返回的字符串末尾没有额外换行。
`draw()` 默认打印；传入 `to_console=False` 时返回字符串。

可通过 `naiwasay.char_names`、`naiwasay.char_funcs` 和 `naiwasay.CHARS`
查看角色名称、函数及字符画。内置角色为 `naiwa`。
空白文本和未知角色会抛出 `naiwasay.CowsayError`。

### 方式二：用 `/naiwa` 命令启动奶蛙模式

把完整的 `skills/naiwa/` 目录放进控制台 AI 客户端的 Skill 目录：

| 客户端 | 用户级安装目录 | 项目级安装目录 | 首次调用 |
| --- | --- | --- | --- |
| [Codex CLI](https://learn.chatgpt.com/docs/build-skills) | `~/.agents/skills/naiwa/` | `.agents/skills/naiwa/` | `$naiwa 开启奶蛙模式` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/naiwa/` | `.claude/skills/naiwa/` | `/naiwa` |
| [Pi](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md) | `~/.pi/agent/skills/naiwa/` | `.pi/skills/naiwa/` | `/skill:naiwa` |
| [OpenCode](https://opencode.ai/docs/skills/) | `~/.config/opencode/skills/naiwa/` | `.opencode/skills/naiwa/` | `使用 naiwa skill，开启奶蛙模式` |

例如，从本仓库根目录为 Codex CLI 安装（已有同名目录时，先备份再更新）：

```bash
mkdir -p "$HOME/.agents/skills"
cp -R skills/naiwa "$HOME/.agents/skills/"
```

在客户端加载或刷新 Skill 后，用命令入口开启，随后照常对话：

| 消息 | 效果 |
| --- | --- |
| `/naiwa` 或 `开启奶蛙模式` | 在当前对话开启奶蛙模式 |
| `/naiwa 今天代码终于跑通了！` | 开启模式，并直接回应后面的消息 |
| `/naiwa full` | 开启并锁定全量模式：长短答复都完整进气泡 |
| `/naiwa auto` | 恢复自适应默认：短答复进气泡，长答复正文+尾部提示 |
| `/naiwa off` 或 `关闭奶蛙模式` | 关闭奶蛙模式 |

### 方式三：用自然语言启动奶蛙模式

不用记命令。安装 Skill 后，直接用一句话开启——“开启奶蛙模式”“打开奶蛙模式”，
或任何明确要求使用 naiwa skill 的说法；客户端不接受裸 `/naiwa` 时，也走这个
入口。用“关闭奶蛙模式”“退出奶蛙模式”或 `/naiwa off` 关闭。

也可以在安装前先试用：让具有本地文件和执行工具的 AI 读取仓库内的
`skills/naiwa/SKILL.md` 后开启模式。每轮渲染由 AI 按 Skill 执行。

### 奶蛙模式做什么（方式二、三共用）

回复语言跟随用户，支持中文、英文和中英混排。输出按答复长短自适应：短答复
完整进入气泡；长答复（代码、表格、多段解释）以普通文本完整输出正文，结尾由
奶蛙用一行短提示气泡收尾，长会话工作不再被刷屏。`/naiwa full` 锁定每轮完整
进气泡，`/naiwa auto` 恢复自适应默认；两种形态都保留段落空行与代码缩进。
形象由控制台输出实现，无需强行增加口癖。Skill 内附完整字符画和零依赖渲染
脚本，无需安装 PyPI 包。

模式仅在当前会话内保持，关闭后恢复普通回复。编程任务照常执行；需要交付
代码或 JSON 文件时，文件保持原始格式，面向用户的回复继续用奶蛙呈现。
调用入口由客户端提供，Skill 不会自行注册命令或修改客户端设置。
只安装 Python 包不会自动安装 Skill。

在 AI 客户端连续输入以下消息，即可检查实际对话效果。只有第一条需要开启模式：

```text
开启奶蛙模式
你好
解释一下 CLI 是什么
写一个 Python 函数，正数时返回两倍，否则返回 0
/naiwa full
再写一遍这个函数
/naiwa auto
把 hello 翻译成中文
关闭奶蛙模式
再解释一下 CLI 是什么
```

关闭之前，短答复应完整出现在气泡里，长答复以普通正文输出并由奶蛙一行提示
收尾；在 `/naiwa full` 与 `/naiwa auto` 之间，长答复也完整进气泡。
关闭之后恢复普通输出。

### 单独使用 Skill 渲染器

以下 shell 命令用于单独检查渲染组件，默认输出纯文本：

```bash
python3 skills/naiwa/scripts/render_naiwa.py --text '奶家人，Build 通过了！'
python3 skills/naiwa/scripts/render_naiwa.py --format markdown --text 'Hello, Naiwa!'
python3 skills/naiwa/scripts/render_naiwa.py --stdin --width 24 <<'NAIWA_MESSAGE'
奶家人，中文和 English 都能说！
NAIWA_MESSAGE
```

`--format plain`（默认）用于终端 stdout、文本文件和管道；`--format markdown`
用于支持 Markdown 的 AI 对话区。气泡默认每行最多 36 个显示列，
`--width` 接受 2–80；完整字符画保持固定缩进。请使用等宽字体，
窄窗口自动折行时加宽窗口。脚本的 CLI 默认值从 Markdown 改为纯文本；
原有调用若需要代码围栏，请显式传入 `--format markdown`。

## 排版与兼容性

公开接口、命令参数、气泡样式和 ASCII 文本排版沿用 Python cowsay 6.1，
内置角色换为奶蛙。每行首尾空白会被去除，空行会被忽略，长文本每 49 个
终端显示列硬换行。汉字按两列计算，组合附加符号不额外占列，从而修复
中文气泡的宽度对齐。

字符画像 cowsay 一样按气泡文字宽度向右缩进。奶蛙图案较大，长文字会让
整体超出窄终端；出现自动折行时，可以加宽终端，或主动将文字分为较短的行。
请使用等宽字体。不同终端的 emoji 组合和部分 Unicode 字符宽度可能不同，
不保证所有这类字符都能准确对齐。

## 开发与发布

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m pip install build twine
python -m build
python -m twine check dist/*
```

显示宽度和换行逻辑只存在于 `src/naiwasay/_textlayout.py` 一处，并以原文
嵌入单文件 Skill 渲染器。修改该模块后，运行
`python3 scripts/sync_skill_layout.py` 并一起提交两个文件；两份拷贝不一致
时测试会失败。

正式版本通过 GitHub Actions 的 `publish.yml` 和 PyPI 可信发布上传，
无需在仓库保存 API Token。具体步骤见
[RELEASING.md](https://github.com/ZeshenTian/naiwasay/blob/main/RELEASING.md)。

## 来源与许可

渲染及命令接口改编自 Vaasudevan Srinivasan 及贡献者维护的
[cowsay-python](https://github.com/VaasuDevanS/cowsay-python)，使用 GPL-3.0
许可。完整许可见 [LICENSE](LICENSE)；修改说明和奶蛙参考图来源见
[NOTICE](NOTICE)。这是独立的同人项目。

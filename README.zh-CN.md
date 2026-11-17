# naiwasay

让奶蛙在终端里说话。采用侧身挥手的精细奶蛙字符画，沿用
[Python cowsay](https://pypi.org/project/cowsay/) 的调用方式和命令行参数。

[English](https://github.com/ZeshenTian/naiwasay/blob/main/README.md)

支持 Python 3.9 及以上版本，无运行时依赖。

## AI 对话 Skill

[奶蛙模式 Skill](https://github.com/ZeshenTian/naiwasay/tree/main/skills/naiwa) 把相同的精细奶蛙形象带到 AI 对话里。
在支持 Agent Skills 的客户端中加载完整的 `skills/naiwa/` 目录后，可以发送：

| 消息 | 效果 |
| --- | --- |
| `/naiwa` 或 `开启奶蛙模式` | 在当前对话开启奶蛙模式 |
| `/naiwa 今天代码终于跑通了！` | 开启模式，并直接回应后面的消息 |
| `/naiwa off` 或 `关闭奶蛙模式` | 关闭奶蛙模式 |

回复语言跟随用户，支持中文、英文和中英混排。短回答放进气泡，长回答
保留正常排版，最后附一句奶蛙总结。Skill 内附完整字符画和可选的独立
渲染脚本，无需安装 PyPI 包；没有执行工具时，也可以直接使用字符画。

这些开关是 Skill 加载后的对话约定，不会注册客户端原生斜杠命令，
也不会修改 ChatGPT Desktop 的全局聊天设置。只安装 Python 包不会自动安装 Skill。

## 安装

从 PyPI 安装：

```bash
python -m pip install naiwasay
```

也可在本地源码目录中安装：

```bash
python -m pip install .
```

## Python 调用

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

## 命令行

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

正式版本通过 GitHub Actions 的 `publish.yml` 和 PyPI 可信发布上传，
无需在仓库保存 API Token。具体步骤见
[RELEASING.md](https://github.com/ZeshenTian/naiwasay/blob/main/RELEASING.md)。

## 来源与许可

渲染及命令接口改编自 Vaasudevan Srinivasan 及贡献者维护的
[cowsay-python](https://github.com/VaasuDevanS/cowsay-python)，使用 GPL-3.0
许可。完整许可见 [LICENSE](LICENSE)；修改说明和奶蛙参考图来源见
[NOTICE](NOTICE)。这是独立的同人项目。

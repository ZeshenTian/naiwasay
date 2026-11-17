# naiwasay

Let Naiwa speak in your CLI console. One job, three ways to start it: put
text into a speech bubble next to a detailed, waving Naiwa character — from
plain Python, or from your terminal AI client, where every reply comes out
as Naiwa.

[中文说明](https://github.com/ZeshenTian/naiwasay/blob/main/README.zh-CN.md)

Python 3.9 or later. No runtime dependencies.

## Preview

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

## Three ways to start Naiwa

| # | Way | Runs in | Naiwa says |
| --- | --- | --- | --- |
| 1 | Python, directly | Any terminal, script, or CI job | The text you pass |
| 2 | The `/naiwa` skill command | Terminal AI clients | Every complete AI reply |
| 3 | Plain natural language | Terminal AI clients | Every complete AI reply |

Way 1 is the Python package, with the familiar
[Python cowsay](https://pypi.org/project/cowsay/) API and CLI. Ways 2 and 3
share the same portable
[Naiwa skill](https://github.com/ZeshenTian/naiwasay/tree/main/skills/naiwa):
install it once into your terminal AI client, then start it either with the
client's command entry or just by asking. The skill brings the same detailed
character to AI conversations: enable it once, keep chatting normally, and
on every turn the LLM generates its answer, calls the bundled terminal
renderer, and displays the complete answer in Naiwa's speech bubble until
you disable the mode.

### Way 1: Print Naiwa directly with Python

#### Install

From PyPI:

```bash
python -m pip install naiwasay
```

Or install a local source checkout:

```bash
python -m pip install .
```

#### Command line

```bash
naiwasay -t "Hello, world!"
naiwasay -t "奶家人，我来了！" -c naiwa
python -m naiwasay --text "Build 通过！" --character naiwa
naiwasay --help
naiwasay --version
```

| Option | Meaning |
| --- | --- |
| `-t`, `--text` | Required text to display |
| `-c`, `--character` | Character name; defaults to `naiwa` |
| `-v`, `--version` | Print the package version |
| `-h`, `--help` | Show command help |

English, Chinese, and mixed text are supplied directly as the message.
There is no translation or language-selection step.

#### Python API

```python
import naiwasay

# Print a speech bubble and the Naiwa character.
naiwasay.naiwa("Hello, world!")
naiwasay.naiwa("奶家人，我来了！")

# Return the complete drawing as a string, without printing it.
art = naiwasay.get_output_string("naiwa", "Build passed!")
print(art)

# Draw a custom character using cowsay's existing interface.
my_character = r"""
\
 \  (^_^)
"""
naiwasay.draw("Hello!", my_character)
art = naiwasay.draw("Hello!", my_character, to_console=False)
```

`naiwa(text)` converts its argument to a string, prints it, and returns
`None`. `get_output_string()` returns a string without a trailing newline.
`draw()` prints by default; `to_console=False` returns the string instead.

The character registry is available as `naiwasay.char_names`,
`naiwasay.char_funcs`, and `naiwasay.CHARS`. The bundled character is
`naiwa`. Empty or whitespace-only text and unknown character names raise
`naiwasay.CowsayError`.

### Way 2: Start Naiwa mode with the `/naiwa` command

Copy the complete `skills/naiwa/` folder into your terminal agent's skills
directory:

| Client | User installation | Project installation | First invocation |
| --- | --- | --- | --- |
| [Codex CLI](https://learn.chatgpt.com/docs/build-skills) | `~/.agents/skills/naiwa/` | `.agents/skills/naiwa/` | `$naiwa Enable Naiwa mode` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/naiwa/` | `.claude/skills/naiwa/` | `/naiwa` |
| [Pi](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md) | `~/.pi/agent/skills/naiwa/` | `.pi/skills/naiwa/` | `/skill:naiwa` |
| [OpenCode](https://opencode.ai/docs/skills/) | `~/.config/opencode/skills/naiwa/` | `.opencode/skills/naiwa/` | `Use the naiwa skill and enable Naiwa mode` |

For example, from this repository's root, install for Codex CLI (back up
any existing `naiwa` directory before updating):

```bash
mkdir -p "$HOME/.agents/skills"
cp -R skills/naiwa "$HOME/.agents/skills/"
```

Load or refresh skills in your client, start the mode with its command
entry, then continue the conversation:

| Message | Effect |
| --- | --- |
| `/naiwa` or `开启奶蛙模式` | Enable Naiwa mode in the current conversation |
| `/naiwa Hello, Naiwa!` | Enable the mode and answer the message |
| `/naiwa full` | Enable and lock every reply into the speech bubble |
| `/naiwa auto` | Adaptive default: short replies in the bubble, long replies closed by a hint |
| `/naiwa off` or `关闭奶蛙模式` | Disable the mode |

### Way 3: Start Naiwa mode with natural language

No command to remember. With the skill installed, just ask in any language:
"开启奶蛙模式", "打开奶蛙模式", or any explicit request to use the naiwa
skill. This is also the entry for clients that reject a bare `/naiwa`. End
the mode with "关闭奶蛙模式", "退出奶蛙模式", or `/naiwa off`.

You can also try the mode before installing anything: ask an AI that has
local file and execution tools to read `skills/naiwa/SKILL.md` in this
repository and enable the mode. The AI runs the bundled renderer each turn.

### What Naiwa mode does (ways 2 and 3)

Replies follow the user's language. Output adapts to reply length: short
answers appear complete in Naiwa's speech bubble, while long answers — code,
tables, multi-paragraph explanations — are delivered as normal text and
closed by a one-line Naiwa hint bubble, so long work sessions stay
readable. `/naiwa full` locks every reply into the bubble; `/naiwa auto`
restores the adaptive default. Paragraph breaks and code indentation are
preserved in both forms. Naiwa's identity comes from the terminal drawing;
forced catchphrases are unnecessary. The full character and
dependency-free renderer are bundled; installing the PyPI package is not
required.

The mode lasts only for the current conversation. Coding work still runs
normally. Code and JSON deliverable files retain their original formats,
while replies to the user continue to appear as Naiwa. Clients provide
their own skill entry points; the skill never registers commands or changes
client settings by itself. Installing the Python package alone does not
install the skill.

Try this continuous conversation in your AI client. Only the first message
enables the mode:

```text
Enable Naiwa mode
Hello
Explain what a CLI is
Write a Python function that doubles positive numbers and otherwise returns 0
/naiwa full
Write it again
/naiwa auto
Translate hello into Chinese
Disable Naiwa mode
Explain what a CLI is again
```

Before deactivation, short answers should appear complete in the bubble,
and long answers as plain text closed by a Naiwa hint; between `/naiwa
full` and `/naiwa auto`, even the long answer goes entirely into the
bubble. After deactivation, answers return to normal.

### The skill renderer on its own

The following shell commands check the rendering component separately:

```bash
python3 skills/naiwa/scripts/render_naiwa.py --text 'Build passed!'
python3 skills/naiwa/scripts/render_naiwa.py --format markdown --text 'Hello, Naiwa!'
python3 skills/naiwa/scripts/render_naiwa.py --stdin --width 24 <<'NAIWA_MESSAGE'
奶家人，Chinese and English both work!
NAIWA_MESSAGE
```

`--format plain` (the default) produces terminal stdout for display, files,
or pipes. Use `--format markdown` for AI conversation panes that render
Markdown. The bubble wraps at 36 display columns by default; `--width`
accepts 2–80. The complete character uses a fixed indent. Use a monospace
font and widen the window if it wraps the drawing. The renderer's CLI
previously defaulted to Markdown; existing callers that need fences must
now pass `--format markdown`.

## Layout and compatibility

The public call patterns, command flags, speech bubble, and ASCII text
layout follow Python cowsay 6.1. Naiwa replaces the bundled cow character.
Lines are stripped of surrounding whitespace, blank lines are omitted, and
long lines are hard-wrapped at 49 terminal columns. Chinese characters
occupy two columns; combining marks do not add a column. This fixes Chinese
bubble alignment while preserving the usual ASCII output layout.

Like cowsay, the character is indented by the bubble's text width. This
detailed character can therefore extend beyond a narrow terminal,
especially with a long message. Widen the terminal or supply shorter
explicit lines if your terminal wraps the drawing. Use a monospace font.
Emoji sequences and font-specific Unicode widths are not guaranteed to
align in every terminal.

## Development and release

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m pip install build twine
python -m build
python -m twine check dist/*
```

Display-width and wrapping logic lives once in
`src/naiwasay/_textlayout.py` and is embedded verbatim in the single-file
skill renderer. After editing the module, run
`python3 scripts/sync_skill_layout.py` and commit both files; the test
suite fails when the copies drift apart.

Releases are published through the `publish.yml` GitHub Actions workflow
and PyPI Trusted Publishing. No API token is stored in the repository. See
[RELEASING.md](https://github.com/ZeshenTian/naiwasay/blob/main/RELEASING.md).

## Credits and license

The rendering and command interfaces are adapted from
[cowsay-python](https://github.com/VaasuDevanS/cowsay-python), by Vaasudevan
Srinivasan and contributors. Distributed under GPL-3.0; see the bundled
`LICENSE` and `NOTICE` files for attribution, modifications, and the Naiwa
image reference. This is an independent fan project.

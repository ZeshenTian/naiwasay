# naiwasay

Let Naiwa say something in your terminal. A detailed, waving Naiwa character,
with the familiar [Python cowsay](https://pypi.org/project/cowsay/) API and CLI.

[中文说明](https://github.com/ZeshenTian/naiwasay/blob/main/README.zh-CN.md)

Python 3.9 or later. No runtime dependencies.

## Terminal AI skill

The portable [Naiwa skill](https://github.com/ZeshenTian/naiwasay/tree/main/skills/naiwa) adds the same detailed character to
AI conversations. Copy the complete `skills/naiwa/` folder into your terminal
agent's skills directory:

| Client | User installation | Project installation | First invocation |
| --- | --- | --- | --- |
| [Codex CLI](https://learn.chatgpt.com/docs/build-skills) | `~/.agents/skills/naiwa/` | `.agents/skills/naiwa/` | `$naiwa Enable Naiwa mode` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/naiwa/` | `.claude/skills/naiwa/` | `/naiwa` |
| [Pi](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md) | `~/.pi/agent/skills/naiwa/` | `.pi/skills/naiwa/` | `/skill:naiwa` |
| [OpenCode](https://opencode.ai/docs/skills/) | `~/.config/opencode/skills/naiwa/` | `.opencode/skills/naiwa/` | `Use the naiwa skill and enable Naiwa mode` |

For example, from this repository's root, install for Codex CLI (back up any
existing `naiwa` directory before updating):

```bash
mkdir -p "$HOME/.agents/skills"
cp -R skills/naiwa "$HOME/.agents/skills/"
```

Load or refresh skills in your client, invoke the skill using the appropriate
entry above, then continue the conversation:

| Message | Effect |
| --- | --- |
| `/naiwa` or `开启奶蛙模式` | Enable Naiwa mode in the current conversation |
| `/naiwa Hello, Naiwa!` | Enable the mode and answer the message |
| `/naiwa off` or `关闭奶蛙模式` | Disable the mode |

Replies follow the user's language. Short answers appear in a speech bubble;
long answers keep their normal formatting and end with a short Naiwa summary.
The full approved character is bundled, along with an optional, dependency-free
renderer. The skill does not require installing the PyPI package.

The mode lasts only for the current conversation. Strict JSON, code-only, and
translation-only replies omit the decoration for that turn. Coding work still
runs normally; progress messages do not repeat the whole character.
Clients provide their own skill entry points. If a client rejects `/naiwa`,
use its entry above or ask it to enable Naiwa mode in natural language.
Installing the Python package alone does not install the skill.

Test the bundled renderer directly in your shell; no package installation is needed:

```bash
python3 skills/naiwa/scripts/render_naiwa.py --text 'Build passed!'
python3 skills/naiwa/scripts/render_naiwa.py --format markdown --text 'Hello, Naiwa!'
python3 skills/naiwa/scripts/render_naiwa.py --stdin --width 24 <<'NAIWA_MESSAGE'
奶家人，Chinese and English both work!
NAIWA_MESSAGE
```

`--format plain` (the default) produces terminal stdout for display, files, or
pipes. Use `--format markdown` for AI conversation panes that render Markdown.
The bubble wraps at 36 display columns by default; `--width` accepts 2–80.
The complete character uses a fixed indent. Use a monospace font and widen the
window if it wraps the drawing. The renderer's CLI previously defaulted to
Markdown; existing callers that need fences must now pass `--format markdown`.

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

## Installation

Install from PyPI:

```bash
python -m pip install naiwasay
```

Or install a local source checkout:

```bash
python -m pip install .
```

## Python API

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

`naiwa(text)` converts its argument to a string, prints it, and returns `None`.
`get_output_string()` returns a string without a trailing newline. `draw()`
prints by default; `to_console=False` returns the string instead.

The character registry is available as `naiwasay.char_names`,
`naiwasay.char_funcs`, and `naiwasay.CHARS`. The bundled character is `naiwa`.
Empty or whitespace-only text and unknown character names raise
`naiwasay.CowsayError`.

## Command line

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

English, Chinese, and mixed text are supplied directly as the message. There
is no translation or language-selection step.

## Layout and compatibility

The public call patterns, command flags, speech bubble, and ASCII text layout
follow Python cowsay 6.1. Naiwa replaces the bundled cow character.
Lines are stripped of surrounding whitespace, blank lines are omitted, and
long lines are hard-wrapped at 49 terminal columns. Chinese characters occupy
two columns; combining marks do not add a column. This fixes Chinese bubble
alignment while preserving the usual ASCII output layout.

Like cowsay, the character is indented by the bubble's text width. This detailed
character can therefore extend beyond a narrow terminal, especially with a
long message. Widen the terminal or supply shorter explicit lines if your
terminal wraps the drawing. Use a monospace font. Emoji sequences and font-
specific Unicode widths are not guaranteed to align in every terminal.

## Development and release

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m pip install build twine
python -m build
python -m twine check dist/*
```

Releases are published through the `publish.yml` GitHub Actions workflow and
PyPI Trusted Publishing. No API token is stored in the repository. See
[RELEASING.md](https://github.com/ZeshenTian/naiwasay/blob/main/RELEASING.md).

## Credits and license

The rendering and command interfaces are adapted from
[cowsay-python](https://github.com/VaasuDevanS/cowsay-python), by Vaasudevan
Srinivasan and contributors. Distributed under GPL-3.0; see the bundled `LICENSE`
and `NOTICE` files for attribution, modifications, and the Naiwa image
reference. This is an independent fan project.

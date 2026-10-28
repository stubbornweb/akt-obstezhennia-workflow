# Commits

Commit messages follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
The commit type tells you how to bump the `Версія X.Y` line in `akt-obstezhennia/SKILL.md`.
The release workflow reads that line and publishes a new release only when it changes.
A version with a suffix, such as `1.2-alpha`, becomes a pre-release for testing.

A commit message has two readers: the person who decides the next version, and the person
running `git log` a year from now to find out why a line exists. Write for both.

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

The type, the colon, the space, and the description are required. Everything else is
optional.

```
feat(style): add conclusion wording for roof-only damage
```

## Types

`feat` and `fix` are the only two types the spec defines. The rest of this table is the
vocabulary this repo uses. Use only these types. Do not invent new ones.

| Type       | Use when                                                          | Bump in `SKILL.md` |
| ---------- | ----------------------------------------------------------------- | ------------------ |
| `feat`     | A new field, rule, conclusion wording, or step in the skill       | `Y`                |
| `fix`      | A wrong act, a wrong rule, or a script error she could have hit   | `Y`                |
| `docs`     | Documentation only: `README.md`, `docs/`, code comments           | none               |
| `refactor` | The behaviour is the same; the code is not                        | none               |
| `test`     | Changes to `example.json` or test runs only, nothing else         | none               |
| `build`    | `tools/make_template.py`, how `template.docx` is built            | none               |
| `ci`       | Workflows in `.github/`                                           | none               |
| `chore`    | Housekeeping that fits no other type: `.gitignore`, tidying       | none               |
| `revert`   | Undoing a previous commit (see below)                             | none               |

Bump the version only when the commit changes something inside `akt-obstezhennia/`. The
release workflow ignores changes outside that folder. `prompts/dictation-project-instructions.md` is not in
the zip: after a change there, paste the new text into her Project by hand.

Types are lowercase. `BREAKING CHANGE` is the one token that must be uppercase.

If a change fits more than one type, split it into more than one commit.

## Scope

Optional. A noun in parentheses that names the part of the repo that changed:

```
fix(script): keep line breaks inside table cells
```

Use one of these scopes:

| Scope         | Part of the repo                                   |
| ------------- | -------------------------------------------------- |
| `skill`       | `akt-obstezhennia/SKILL.md`                        |
| `style`       | `akt-obstezhennia/style.md`                        |
| `fields`      | `akt-obstezhennia/fields.json`                     |
| `template`    | `akt-obstezhennia/template.docx`                   |
| `script`      | `akt-obstezhennia/scripts/fill_act.py`             |
| `example`     | `akt-obstezhennia/example.json`                    |
| `prompts`     | `prompts/dictation-project-instructions.md`        |
| `guide`       | `docs/guide-uk.md`, `docs/img/`                    |
| `tools`       | `tools/`                                           |
| `release`     | `.github/workflows/release.yml`                    |

Leave out the scope if none of these fits. Do not invent a vague one: `feat(core):` says
nothing.

## Description

The text after the colon, on the subject line.

- **Use the imperative mood.** Write "add", not "added" or "adds". Test: the subject should
  complete the sentence _"Applying this commit will…"_.
- **Start lowercase. Do not end with a period.**
- **Keep it to 72 characters or fewer**, including the type and scope, so
  `git log --oneline` stays readable.
- **Say the effect, not the method.** Write `fix(script): stop dropping the last room from
  the act`, not `fix(script): change loop handling`.

## Body

Optional. Leave one blank line after the description. Write as many paragraphs as you need.

Use the body for the **why**, not the what. The diff already shows the what. Write a body
when the change reverses an earlier decision, folds in one of her "МОЇ ПРАВКИ" lines, or
looks wrong without context. Wrap lines at 72 columns.

## Footers

Leave one blank line after the body. Each footer is `Token: value`. The token uses `-`
instead of spaces, as in git trailers.

| Footer                | Use                                                     |
| --------------------- | ------------------------------------------------------- |
| `Closes #42`          | This commit fully resolves the issue                    |
| `Refs #42`            | Related to the issue, does not close it                 |
| `BREAKING CHANGE: …`  | Describes an incompatible change (uppercase, spaces OK) |
| `Co-authored-by: …`   | A second author                                         |

`BREAKING CHANGE` is the one exception to the `-` rule. `BREAKING-CHANGE` means the same
thing. A footer value can run across several lines. It ends at the next token.

## Breaking changes

A change is breaking when she has to work differently, or when the setup must be redone,
for example when a dictation command is renamed or `prompts/dictation-project-instructions.md` must be pasted
again. A breaking change bumps `X` and resets `Y` to 0, whatever its type.

Mark it with `!` before the colon, with a footer, or with both:

```
feat(prompts)!: rename the "Сформуй акт" command to "Акт готовий"
```

```
feat(prompts): rename the "Сформуй акт" command to "Акт готовий"

BREAKING CHANGE: she now says "Акт готовий" to get the act. Paste the
new prompts/dictation-project-instructions.md into the Project and
update the guide.
```

If you use `!` alone, the description alone must explain the breaking change. A
`BREAKING CHANGE:` footer must say **what to do**, not only what broke.

## Reverting

```
revert: feat(style): add conclusion wording for roof-only damage

Refs: a1b2c3d
```

## Writing the message

Use a heredoc so that quotes in the body and footers stay as they are:

```sh
git commit -F - <<'EOF'
fix(fields): default the commission date to the inspection date

She left the commission date empty in three acts in a row. The
inspection date is the right value in every case she has sent.

Closes #10
EOF
```

## Fixing a bad message

Before you push, fix it with `git commit --amend` or `git rebase -i`. After you push, leave
it. Rewriting history on `main` costs more than a bad subject line. A commit that breaks
the convention only confuses the version decision. It does no other harm.

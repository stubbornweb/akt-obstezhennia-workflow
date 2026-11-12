# Commits

The shared rules are in `~/www/home/docs/agents/commits.md`. This file adds what is different in this repo.

The commit type tells you how to bump the `Версія X.Y` line in `akt-obstezhennia/SKILL.md`. The release workflow reads that line and publishes a new release only when it changes. A version with a suffix, such as `1.2-alpha`, becomes a pre-release for testing.

## Types

| Type       | Use when                                                        | Bump in `SKILL.md` |
| ---------- | --------------------------------------------------------------- | ------------------ |
| `feat`     | A new field, rule, conclusion wording, or step in the skill     | `Y`                |
| `fix`      | A wrong act, a wrong rule, or a script error she could have hit | `Y`                |
| `docs`     | Documentation only: `README.md`, `docs/`, code comments         | none               |
| `refactor` | The behaviour is the same; the code is not                      | none               |
| `test`     | Changes to `example.json` or test runs only, nothing else       | none               |
| `build`    | `tools/make_template.py`, how `template.docx` is built          | none               |
| `ci`       | Workflows in `.github/`                                         | none               |
| `chore`    | Housekeeping that fits no other type: `.gitignore`, tidying     | none               |
| `revert`   | Undoing a previous commit                                       | none               |

Bump the version only when the commit changes something inside `akt-obstezhennia/`. The release workflow ignores changes outside that folder. `prompts/dictation-project-instructions.md` is not in the zip: after a change there, paste the new text into her Project by hand.

## Scope

| Scope      | Part of the repo                            |
| ---------- | ------------------------------------------- |
| `skill`    | `akt-obstezhennia/SKILL.md`                 |
| `style`    | `akt-obstezhennia/style.md`                 |
| `fields`   | `akt-obstezhennia/fields.json`              |
| `template` | `akt-obstezhennia/template.docx`            |
| `script`   | `akt-obstezhennia/scripts/fill_act.py`      |
| `example`  | `akt-obstezhennia/example.json`             |
| `prompts`  | `prompts/dictation-project-instructions.md` |
| `guide`    | `docs/guide-uk.md`, `docs/img/`             |
| `tools`    | `tools/`                                    |
| `release`  | `.github/workflows/release.yml`             |

## Body

Write a body also when the change folds in one of her "МОЇ ПРАВКИ" lines.

## Breaking changes

A change is breaking when she has to work differently, or when the setup must be redone, for example when a dictation command is renamed or `prompts/dictation-project-instructions.md` must be pasted again. A breaking change bumps `X` and resets `Y` to 0, whatever its type.

```
feat(prompts)!: rename the "Сформуй акт" command to "Акт готовий"

BREAKING CHANGE: she now says "Акт готовий" to get the act. Paste the
new prompts/dictation-project-instructions.md into the Project and
update the guide.
```

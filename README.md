# Damage inspection acts from dictation

Turns a field worker's spoken description of a damaged object into a commission inspection act (`.docx`), using only the free Claude plan (web and mobile app).

## How it works

1. **On site (phone):** in the Claude Project "Акти пошкоджень" she opens a new chat and says "Об'єкт" with the object code, a short label only she can read, such as "Об'єкт Г 1/1". The chat carries the same name; she renames it by hand if claude.ai picked another one. Claude asks the object form: 6 short groups of questions about the building, its structures and engineering systems, and the damage date and cause. She answers by voice or taps an option. Then she dictates the damage room by room with the microphone button. Claude replies only "Записано". With no internet she dictates into the phone's notes app and pastes the text into the chat later.
2. **In the office (computer):** she opens the same chat and writes "Сформуй акт". The skill reads the dictation, asks once about anything missing, writes the act text, and fills the council's blank with a script. She gets a `.docx` and a checklist.
3. **Finishing:** she types personal data and document numbers into the turquoise `[[...]]` fields in Word, resolves the red `[УТОЧНИТИ: ...]` notes, checks the conclusion, and sends the act.

Personal data (owner, passport, tax number, address, cadastral number, document numbers) never goes into Claude; the act carries placeholders instead.

## What's in the repo

| Path | What it is |
|---|---|
| `akt-obstezhennia/` | The skill. The release workflow zips this folder. |
| `akt-obstezhennia/SKILL.md` | Instructions Claude follows (Ukrainian). Holds the version line. |
| `akt-obstezhennia/template.docx` | The council's blank with `{{field}}` markers. Everything outside the markers is the original form. |
| `akt-obstezhennia/fields.json` | Every field: label, type, default. Single source of truth for the script and for Claude. |
| `akt-obstezhennia/style.md` | Writing rules, where dictated facts go, building codes (ДК 018-2000), conclusion wordings. |
| `akt-obstezhennia/example.json` | One real act, anonymised, as Claude's worked example. Also the CI smoke test. |
| `akt-obstezhennia/scripts/fill_act.py` | Fills the template from JSON. Python standard library only. |
| `prompts/dictation-project-instructions.md` | Text for the Project's Instructions field: protected core, current event, her rules. |
| `docs/guide-uk.md` | Her guide (Ukrainian): install, update, Project instructions, daily work. Screenshots in `docs/img/`. |
| `tools/` | Maintainer-only: the original blank and the script that turned it into `template.docx`. |

Only anonymised material belongs here. Real acts never get committed.

## One-time setup (about 20 minutes, on her account)

1. Create her free account at claude.ai and log in on her office computer and in the Claude app on her phone.
2. Settings → Privacy: turn off using chats to improve the models.
3. Install the skill with her, following part 1 of [`docs/guide-uk.md`](docs/guide-uk.md), so she sees each step once. Take the `.zip` from the newest release on the [Releases page](https://github.com/stubbornweb/akt-obstezhennia-workflow/releases), whether it is alpha, beta, or a full release.
4. On the computer: Projects → New project → name it "Акти пошкоджень". Paste `prompts/dictation-project-instructions.md` into the Project's Instructions field.
5. On her phone: check the Project appears and she can start a chat inside it. If the app doesn't show Projects, she uses ordinary chats named "Об'єкт <code>" and pastes the Project instructions' first block as her first message. Nothing else changes.
6. Do one complete test object together: dictate a few lines on the phone, then "Сформуй акт" on the computer, open the Word file, fill one turquoise field.

## The 2-week routine

1. Copy her lines from the "МОЇ ПРАВКИ" section of the Project instructions.
2. Fold each rule into `style.md` (or `fields.json` for a default, or `SKILL.md` for a process change). Keep one place per rule.
3. Bump `Версія X.Y (date)` in `SKILL.md`, commit, merge to `main`.
   A suffix such as `Версія 1.2-alpha` or `Версія 1.2-beta` makes the workflow publish a pre-release. She installs and tests the newest release of any kind.
4. The workflow smoke-tests and publishes a Release with `akt-obstezhennia.zip`.
5. Clear the merged lines from "МОЇ ПРАВКИ" in her Project instructions.
6. Message her: the new version number, one line on what changed, and a link to part 2 of [`docs/guide-uk.md`](docs/guide-uk.md). She updates the skill herself.
   If `prompts/dictation-project-instructions.md` changed, first set its "ПОТОЧНА ПОДІЯ" to her current event, then add "оновіть інструкції проєкту" to the message. She replaces the whole Instructions text (part 3 of the guide).

## Changing the blank

- **Commission member or order changes:** open `akt-obstezhennia/template.docx` in Word, edit the text, keep every `{{...}}` marker as is, save, then test:
  `python3 akt-obstezhennia/scripts/fill_act.py --data akt-obstezhennia/example.json --out test.docx`
- **A completely new blank:** put it at `tools/blank-original.docx`, adjust the paragraph numbers in `tools/make_template.py`, run it (`pip install python-docx` first).

## Known limits

- Free plan usage limits: if Claude says the limit is reached, dictation continues in the notes app and acts get generated after the reset.
- The conclusion for "only finishing/windows damaged" in `style.md` is a working draft, not yet confirmed by real acts. Replace it once more examples arrive.

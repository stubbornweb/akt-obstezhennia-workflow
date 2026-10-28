# Damage inspection acts from dictation

Turns a field worker's spoken description of a damaged object into the Dubno city council's commission inspection act (`.docx`), using only the free Claude plan (web and mobile app).

## How it works

1. **On site (phone):** in the Claude Project "Акти пошкоджень" she opens a new chat, says "Об'єкт N, дата", then dictates room by room with the microphone button. Claude replies only "Записано". With no internet she dictates into the phone's notes app and pastes the text into the chat later.
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
| `project/instructions.md` | Text for the Project's Instructions field: protected core, current event, her rules. |
| `docs/cheat-sheet-uk.md` | Her one-page reminder (Ukrainian). |
| `tools/` | Maintainer-only: the original blank and the script that turned it into `template.docx`. |

Only anonymised material belongs here. Real acts never get committed.

## One-time setup (about 20 minutes, on her account)

1. Create her free account at claude.ai and log in on her office computer and in the Claude app on her phone.
2. Settings → Privacy: turn off using chats to improve the models.
3. Settings → Capabilities: turn on code execution and file creation; under Skills, upload `akt-obstezhennia.zip` from the latest GitHub Release. (Menu names can shift slightly between app versions.)
4. On the computer: Projects → New project → name it "Акти пошкоджень". Paste `project/instructions.md` into the Project's Instructions field.
5. On her phone: check the Project appears and she can start a chat inside it. If the app doesn't show Projects, she uses ordinary chats named "Об'єкт N" and pastes the Project instructions' first block as her first message. Nothing else changes.
6. Do one complete test object together: dictate a few lines on the phone, then "Сформуй акт" on the computer, open the Word file, fill one turquoise field.

## The 2-week routine

1. Copy her lines from the "МОЇ ПРАВКИ" section of the Project instructions.
2. Fold each rule into `style.md` (or `fields.json` for a default, or `SKILL.md` for a process change). Keep one place per rule.
3. Bump `Версія X.Y (date)` in `SKILL.md`, commit, merge to `main`.
   To test a version before she gets it, add a suffix such as `Версія 1.2-alpha`. The workflow publishes it as a pre-release, which the latest-release link skips.
4. The workflow smoke-tests and publishes a Release with `akt-obstezhennia.zip`.
5. Replace the skill in her Claude settings with the new zip and clear the merged lines from "МОЇ ПРАВКИ".

## Changing the blank

- **Commission member or order changes:** open `akt-obstezhennia/template.docx` in Word, edit the text, keep every `{{...}}` marker as is, save, then test:
  `python3 akt-obstezhennia/scripts/fill_act.py --data akt-obstezhennia/example.json --out test.docx`
- **A completely new blank:** put it at `tools/blank-original.docx`, adjust the paragraph numbers in `tools/make_template.py`, run it (`pip install python-docx` first).

## Known limits

- Free plan usage limits: if Claude says the limit is reached, dictation continues in the notes app and acts get generated after the reset.
- The conclusion for "only finishing/windows damaged" in `style.md` is a working draft, not yet confirmed by real acts. Replace it once more examples arrive.

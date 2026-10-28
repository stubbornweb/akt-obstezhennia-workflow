"""Перевіряє, що анкета об'єкта питає про кожне поле розділу 1 бланка.

Поля розділу 1 — усі поля з fields.json, крім персональних, пошкоджень (d_*)
і полів, які Claude заповнює після вільної диктовки.
"""

import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "akt-obstezhennia"
AFTER_DICTATION = {"repairs", "additional_info", "conclusions", "attachments"}

fields = json.loads((SKILL / "fields.json").read_text(encoding="utf-8"))["fields"]
asked = set(re.findall(r"`([a-z_]+)`", (SKILL / "anketa.md").read_text(encoding="utf-8")))

required = {
    key for key, field in fields.items()
    if field["type"] != "personal" and not key.startswith("d_") and key not in AFTER_DICTATION
}
missing = sorted(required - asked)
unknown = sorted(asked - fields.keys())

for key in missing:
    print(f"anketa.md не питає про поле {key}")
for key in unknown:
    print(f"anketa.md посилається на поле {key}, якого немає в fields.json")
if missing or unknown:
    sys.exit(1)
print(f"Анкета охоплює всі поля розділу 1: {len(required)}.")

#!/usr/bin/env python3
"""Fill the commission act template with values from a JSON file.

    python3 fill_act.py --data act.json --out "/mnt/user-data/outputs/Акт_об'єкт-14_28.10.2026.docx"

act.json: {"field_key": "value", ...}, keys from fields.json. A value may be a
string (use "\\n" for a new paragraph) or a list of strings (one paragraph each).
Missing or empty fields get their default from fields.json.

Formatting applied to every filled value: the template's font, underlined.
[[...]]          -> turquoise highlight (personal data the worker types in Word)
[УТОЧНИТИ: ...]  -> red bold (information still missing)

Prints a checklist of everything the worker still has to fill or confirm.
Standard library only, so it runs anywhere Python 3 runs.
"""
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.dom import minidom

HERE = Path(__file__).resolve().parent.parent
MARKER = re.compile(r"\{\{([a-z_]+)\}\}")
SPECIAL = re.compile(r"(\[\[.*?\]\]|\[УТОЧНИТИ:.*?\])")

RPR_ORDER = [
    "rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike",
    "dstrike", "outline", "shadow", "emboss", "imprint", "noProof", "snapToGrid",
    "vanish", "webHidden", "color", "spacing", "w", "kern", "position", "sz",
    "szCs", "highlight", "u", "effect", "bdr", "shd", "fitText", "vertAlign",
    "rtl", "cs", "em", "lang", "eastAsianLayout", "specVanish", "oMath",
]


def children(node, tag):
    return [c for c in node.childNodes if c.nodeType == c.ELEMENT_NODE and c.tagName == tag]


def run_text(r):
    return "".join(t.firstChild.data if t.firstChild else "" for t in children(r, "w:t"))


def set_run_text(doc, r, text):
    for c in list(r.childNodes):
        if c.nodeType == c.ELEMENT_NODE and c.tagName in ("w:t", "w:tab", "w:br"):
            r.removeChild(c)
    t = doc.createElement("w:t")
    t.setAttribute("xml:space", "preserve")
    t.appendChild(doc.createTextNode(text))
    r.appendChild(t)


def set_rpr(doc, rpr, name, attrs):
    """Insert or replace one rPr child, keeping the schema order Word expects."""
    for c in children(rpr, "w:" + name):
        rpr.removeChild(c)
    el = doc.createElement("w:" + name)
    for k, v in attrs.items():
        el.setAttribute(k, v)
    pos = RPR_ORDER.index(name)
    for c in rpr.childNodes:
        if c.nodeType == c.ELEMENT_NODE:
            cname = c.tagName.split(":")[1]
            if cname in RPR_ORDER and RPR_ORDER.index(cname) > pos:
                rpr.insertBefore(el, c)
                return
    rpr.appendChild(el)


def merge_split_markers(p):
    """Word sometimes splits {{marker}} over several runs after manual edits.
    Move every marker's characters into the run where it starts."""
    runs = children(p, "w:r")
    texts = [run_text(r) for r in runs]
    joined = "".join(texts)
    if "{{" not in joined:
        return
    owner = [i for i, t in enumerate(texts) for _ in t]
    for m in MARKER.finditer(joined):
        for k in range(m.start(), m.end()):
            owner[k] = owner[m.start()]
    new = [""] * len(runs)
    for ch, i in zip(joined, owner):
        new[i] += ch
    doc = p.ownerDocument
    for r, old, txt in zip(runs, texts, new):
        if old != txt:
            set_run_text(doc, r, txt)


def make_runs(doc, base_rpr, text):
    out = []
    for part in SPECIAL.split(text):
        if not part:
            continue
        r = doc.createElement("w:r")
        rpr = base_rpr.cloneNode(True) if base_rpr is not None else doc.createElement("w:rPr")
        if part.startswith("[["):
            set_rpr(doc, rpr, "highlight", {"w:val": "cyan"})
        elif part.startswith("[УТОЧНИТИ:"):
            set_rpr(doc, rpr, "b", {})
            set_rpr(doc, rpr, "color", {"w:val": "FF0000"})
        r.appendChild(rpr)
        set_run_text(doc, r, part)
        out.append(r)
    return out


def fill_paragraph(p, values, used):
    doc = p.ownerDocument
    merge_split_markers(p)
    for r in children(p, "w:r"):
        text = run_text(r)
        m = MARKER.search(text)
        if not m:
            continue
        key = m.group(1)
        if key not in values:
            raise SystemExit(f"У шаблоні є маркер {{{{{key}}}}}, якого немає в fields.json")
        used.add(key)
        rpr_list = children(r, "w:rPr")
        rpr = rpr_list[0] if rpr_list else None
        lines = values[key].split("\n")
        before, after = text[: m.start()], text[m.end():]
        first = make_runs(doc, rpr, before + lines[0] + after)
        for nr in first:
            p.insertBefore(nr, r)
        p.removeChild(r)
        # extra lines become new paragraphs with the same paragraph formatting
        anchor = p
        ppr = children(p, "w:pPr")
        for line in lines[1:]:
            np_ = doc.createElement("w:p")
            if ppr:
                np_.appendChild(ppr[0].cloneNode(True))
            for nr in make_runs(doc, rpr, line):
                np_.appendChild(nr)
            anchor.parentNode.insertBefore(np_, anchor.nextSibling)
            anchor = np_
        return fill_paragraph(p, values, used)  # a paragraph may hold several markers


def normalise(value):
    if value is None:
        return ""
    if isinstance(value, list):
        value = "\n".join(str(v).strip() for v in value if str(v).strip())
    return str(value).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="act.json")
    ap.add_argument("--out", required=True, help="шлях до готового .docx")
    ap.add_argument("--template", default=str(HERE / "template.docx"))
    ap.add_argument("--fields", default=str(HERE / "fields.json"))
    a = ap.parse_args()

    fields = json.loads(Path(a.fields).read_text(encoding="utf-8"))["fields"]
    data = json.loads(Path(a.data).read_text(encoding="utf-8"))
    unknown = sorted(set(data) - set(fields))
    if unknown:
        raise SystemExit("Невідомі поля в act.json: " + ", ".join(unknown)
                         + "\nДопустимі: " + ", ".join(fields))
    values = {k: normalise(data.get(k)) or f["default"] for k, f in fields.items()}

    with zipfile.ZipFile(a.template) as zin:
        doc = minidom.parseString(zin.read("word/document.xml"))
        used = set()
        for p in list(doc.getElementsByTagName("w:p")):
            fill_paragraph(p, values, used)
        missing = sorted(set(fields) - used)
        if missing:
            raise SystemExit("У шаблоні немає маркерів для полів: " + ", ".join(missing))
        xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + doc.documentElement.toxml()
        if "{{" in xml:
            raise SystemExit("Після заповнення лишилися маркери {{...}} — перевір шаблон.")
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                payload = xml.encode("utf-8") if item.filename == "word/document.xml" else zin.read(item.filename)
                zout.writestr(item, payload)

    # checklist, in document order, without repeats
    placeholders, unclear = [], []
    for key in fields:
        for s in SPECIAL.findall(values[key]):
            target = placeholders if s.startswith("[[") else unclear
            if s not in target:
                target.append(s)
    print(f"ГОТОВО: {out}")
    print("\nЗАПОВНИТИ ВРУЧНУ (бірюзові поля):")
    print("\n".join(f"- {s[2:-2]}" for s in placeholders) or "- немає")
    print("\nУТОЧНИТИ (червоне в тексті):")
    print("\n".join(f"- {s[11:-1].strip()}" for s in unclear) or "- немає")


if __name__ == "__main__":
    sys.exit(main())

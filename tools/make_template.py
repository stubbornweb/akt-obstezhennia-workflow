"""One-off maintainer tool: turn the council's blank act into the skill's template.

Puts a {{field}} marker at every fillable spot of tools/blank-original.docx and
writes akt-obstezhennia/template.docx. Everything else in the blank is untouched.

You only need this if you get a completely new blank. For small changes (a new
commission member, a new order number) edit akt-obstezhennia/template.docx in
Word directly and keep the {{...}} markers intact.

Usage: pip install python-docx && python tools/make_template.py
"""
import copy
from pathlib import Path

import docx
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "blank-original.docx"
DST = ROOT / "akt-obstezhennia" / "template.docx"

RPR_ORDER = [
    "rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike",
    "dstrike", "outline", "shadow", "emboss", "imprint", "noProof", "snapToGrid",
    "vanish", "webHidden", "color", "spacing", "w", "kern", "position", "sz",
    "szCs", "highlight", "u", "effect", "bdr", "shd", "fitText", "vertAlign",
    "rtl", "cs", "em", "lang", "eastAsianLayout", "specVanish", "oMath",
]


def runs(p):
    return p.findall(qn("w:r"))


def run_text(r):
    return "".join(t.text or "" for t in r.iter(qn("w:t")))


def set_text(r, text):
    for t in list(r.iter(qn("w:t"))):
        t.getparent().remove(t)
    for tab in list(r.findall(qn("w:tab"))):
        r.remove(tab)
    t = r.makeelement(qn("w:t"), {})
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text
    r.append(t)


def value_rpr(rpr):
    """Formatting for filled values: same font, underlined, no highlight."""
    rpr = copy.deepcopy(rpr) if rpr is not None else docx.oxml.parse_xml(
        '<w:rPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
    for tag in ("b", "bCs", "i", "iCs", "highlight", "u", "shd"):
        for el in rpr.findall(qn("w:" + tag)):
            rpr.remove(el)
    u = rpr.makeelement(qn("w:u"), {qn("w:val"): "single"})
    pos = RPR_ORDER.index("u")
    for i, child in enumerate(rpr):
        name = child.tag.split("}")[1]
        if name in RPR_ORDER and RPR_ORDER.index(name) > pos:
            rpr.insert(i, u)
            break
    else:
        rpr.append(u)
    return rpr


def marker_run(template_run, key):
    r = template_run.makeelement(qn("w:r"), {})
    r.append(value_rpr(template_run.find(qn("w:rPr"))))
    set_text(r, "{{%s}}" % key)
    return r


def replace_run(p, idx, key):
    """The whole run (underscores, '-' or a sample value) becomes the marker."""
    old = runs(p)[idx]
    old.addnext(marker_run(old, key))
    p.remove(old)


def append_after(p, idx, key, strip=""):
    """Keep the label run, minus trailing characters in `strip` ('-' or '_'),
    and put the marker right after it, separated by one space."""
    r = runs(p)[idx]
    text = run_text(r)
    if strip:
        stripped = text.rstrip().rstrip(strip)
        assert stripped != text.rstrip(), (text, strip)
        text = stripped
    set_text(r, text.rstrip() + " ")
    r.addnext(marker_run(r, key))


def cell_marker(tbl, row, key):
    tr = tbl.findall(qn("w:tr"))[row]
    label_cell, value_cell = tr.findall(qn("w:tc"))[:2]
    label_run = label_cell.find(qn("w:p")).find(qn("w:r"))
    p = value_cell.find(qn("w:p"))
    for r in runs(p):
        p.remove(r)
    p.append(marker_run(label_run, key))


def main():
    d = docx.Document(str(SRC))
    body = [el for el in d.element.body.iterchildren() if el.tag in (qn("w:p"), qn("w:tbl"))]
    P = lambda i: body[i]

    # sanity check: we are editing the blank we analysed
    assert run_text(runs(P(6))[0]).startswith("Назва об’єкта")
    assert run_text(runs(P(79))[0]).startswith("Примітка")

    replace_run(P(6), 1, "object_name")
    append_after(P(7), 0, "address", strip="_")
    append_after(P(8), 0, "cadastral")
    p8 = P(8)
    p8.remove(runs(p8)[2])  # old underscores
    replace_run(P(9), 1, "ownership")
    replace_run(P(10), 1, "owner")
    append_after(P(27), 1, "presence", strip="_")  # keeps the ')' of the label
    set_text(runs(P(29))[0], "на підставі заяви (за наявності) ")  # drop the tab
    replace_run(P(29), 1, "application")
    P(30).getparent().remove(P(30))  # spare underscore line under the application

    append_after(P(34), 0, "heritage", strip="-")
    for i, key in [(35, "year_built"), (36, "total_area"), (37, "floors_total"),
                   (38, "floors_underground"), (39, "floors_above")]:
        append_after(P(i), len(runs(P(i))) - 1, key)
    for i, key in [(40, "floors_mansard"), (41, "sections"), (42, "apartments"),
                   (43, "nonresidential_area")]:
        append_after(P(i), 0, key, strip="-")
    replace_run(P(45), 0, "documents")

    tbl = P(48)
    for row, key in [(1, "c_foundations"), (2, "c_walls"), (4, "c_slab_first_floor"),
                     (5, "c_slab_interfloor"), (6, "c_slab_attic"), (7, "c_roof_structure"),
                     (8, "c_roofing"), (9, "c_windows"), (10, "c_doors"), (12, "c_facade"),
                     (13, "c_floors"), (14, "c_ceiling"), (15, "c_inner_walls"),
                     (17, "c_electricity"), (18, "c_water"), (19, "c_gas"),
                     (20, "c_sewage"), (21, "c_heating")]:
        cell_marker(tbl, row, key)

    replace_run(P(52), 1, "damage_date")
    replace_run(P(53), 1, "damage_cause")
    replace_run(P(55), 1, "d_foundation")
    replace_run(P(56), 1, "d_walls_facade")
    set_text(runs(P(56))[0], run_text(runs(P(56))[0]).rstrip() + " ")
    append_after(P(57), 0, "d_roof")
    replace_run(P(58), 1, "d_inner")
    append_after(P(59), 1, "d_floors")
    append_after(P(60), 1, "d_openings")
    append_after(P(61), 1, "d_utilities")
    append_after(P(62), 1, "d_other", strip="_")
    append_after(P(64), len(runs(P(64))) - 1, "repairs")
    append_after(P(65), 0, "additional_info", strip="_")
    replace_run(P(68), 0, "conclusions")

    replace_run(P(70), 0, "attachments")
    for i in (71, 72, 73):
        P(i).getparent().remove(P(i))

    owner_tbl = P(77)
    cell = owner_tbl.find(qn("w:tr")).findall(qn("w:tc"))[2]
    replace_run(cell.find(qn("w:p")), 0, "owner_sign")

    d.save(str(DST))
    print("written", DST)


if __name__ == "__main__":
    main()

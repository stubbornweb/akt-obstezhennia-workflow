# Damage inspection acts from dictation

A field worker inspects a damaged building and dictates what she sees to Claude. Claude turns the dictation into a commission inspection act in Word.

## Language

### The work

**Об'єкт** (object):
One damaged building or apartment that the commission inspects. One object has one chat and one act.
_Avoid_: site, address, case

**Код об'єкта** (object code):
A short label the worker gives an object, such as «Г 1/1». She understands it; a stranger cannot find the address or the owner from it.
_Avoid_: object number, address, street name

**Обстеження** (survey):
The visit to an object, on one date, when the worker looks at the damage.
_Avoid_: inspection visit, check

**Акт** (act):
The Word document that records one survey of one object, made from the council blank.
_Avoid_: report, protocol, blank (the blank is the empty template)

**Поточна подія** (current event):
The damage date and cause that apply to most objects right now, for example one attack. It is the default answer for the damage date and cause.
_Avoid_: incident, default damage

### Chat flow

**Анкета об'єкта** (object form):
The fixed questions Claude asks at the start of a chat. They cover section 1 of the act and the damage date and cause in section 2.
_Avoid_: start questions, intake, passport of the object (collides with «технічний паспорт»)

**Група анкети** (form group):
One message of the анкета об'єкта with 3–5 questions about one area: act, building, structures, openings and finishes, engineering systems, damage.
_Avoid_: step, page, block

**Вільна диктовка** (free dictation):
The part of the chat after the анкета об'єкта, where the worker describes the damage room by room in her own words.
_Avoid_: description mode, damage dictation

### Answers and marks

**«Немає»** (not present):
The answer for a thing that does not exist at the object. The act shows "-".
_Avoid_: skip, n/a

**«Пропустити»** (skip):
The answer for a thing the worker does not know or does not answer now. The act shows a прогалина.
_Avoid_: no, empty

**Прогалина** (gap):
Red text `[УТОЧНИТИ: …]` in the act for a required fact that is still missing. The act is not ready to send while one remains.
_Avoid_: check mark, TODO

**Заглушка** (placeholder):
Turquoise text `[[…]]` in the act for personal data or a document number that the worker types in Word herself. Claude never asks for these.
_Avoid_: manual field, blank field

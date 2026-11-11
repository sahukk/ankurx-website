# AnkurX editorial rules and bulletin workflow

AnkurX ("खबर भी, समझ भी") is a Hindi news platform for the youth of North Bihar, published at https://ankurx.in.
Editor and grievance officer: K. K. Sahu (sahukk@gmail.com).
Philosophy: a news channel for North Bihar's youth that helps them think in a wise and intelligent way; it brings out hidden talent and grows understanding.

## Coverage
- Region first: Tirhut and Darbhanga divisions — Muzaffarpur, Darbhanga, Madhubani, Samastipur, Vaishali, Sitamarhi, Sheohar, East Champaran, West Champaran. Bihar-wide items only when they matter to youth here.
- Topics (`cat`): `job` = नौकरी-शिक्षा (recruitment, exams, results, admissions, scholarships, universities LNMU/BRABU), `gen` = आम खबर (civic, health, transport, weather, administration), `new` = नई पहल (innovation, science, technology, startups, infrastructure for the future), `talent` = प्रतिभा (achievements of young people of the region).
- 5–8 items per bulletin. At least 2 `job` items when real ones exist. Mix districts.

## Hard rules
1. Every item must come from a page you actually opened and read, with a clear date within the last 48 hours (for jobs/exams: a notice that is currently relevant). No date or cannot open it → drop it.
2. Sources: official sites (bpsc.bihar.gov.in, bssc.bihar.gov.in, lnmu.ac.in, brabu.ac.in, district *.nic.in, IMD, railways, PIB, state government) and established newspapers (Prabhat Khabar, Dainik Jagran, Hindustan, Dainik Bhaskar, Times of India, The Hindu, Indian Express, ETV Bharat, News18 Bihar). Coaching / "sarkari result" sites are hints only — confirm on the official site or leave the item out.
3. When sources conflict (dates, numbers), do not choose: say so and point to the official site.
4. Write fresh, simple Hindi in your own words, 1–3 sentences per item. Never copy sentences, headlines or photos. Always give `source` (outlet name, date) and the `url` you read (https only).
5. EXCLUDE entirely: crime and violence, communal or caste conflict, deaths/accidents/suicides, anything involving minors as victims, political allegations and party statements, rumours, health claims without an official source. When in doubt, leave it out.
6. Tone: calm, useful, hopeful, no sensational words, no exclamation marks.

## Bulletin file
`data/bulletins/<YYYY-MM-DD>-<am|pm>.json`:
```json
{"id":"2026-11-12-am","date":"2026-11-12","slot":"am","unreviewed":true,
 "items":[{"cat":"job","head":"…","body":"…","source":"प्रभात खबर, 12 नवंबर","url":"https://…","district":"दरभंगा"}]}
```
`am` = morning (published 08:00 IST), `pm` = evening (published 18:00 IST). `unreviewed: true` means the editor has not approved it; the site then shows "संपादक की जाँच बाकी". Remove the key (or set false) once approved.

Validate and publish with `python3 tools/publish.py push "Bulletin <id>"` (rebuilds data/index.json, commits, pushes to main; live in about a minute).

## Workflow (cloud routines, times IST)
- **Draft run (06:30 and 16:30):** research, write the draft JSON, save it on branch `drafts` as `drafts/<id>.json`, then email the editor (to sahukk@gmail.com, subject `AnkurX ड्राफ़्ट: <सुबह|शाम> <date> [<id>]`) with every item numbered (headline, text, source) and these reply instructions:
  - `OK` → publish as is
  - `3 हटाओ` → remove item 3
  - `2 शीर्षक: …` / `2 खबर: …` → replace headline / text of item 2
  - `नई खबर: …` → add the editor's own item (category inferred; mark source "AnkurX संवाददाता")
  - `रोको` → do not publish this bulletin
  If nothing is heard by publish time, it is published as is with the "संपादक की जाँच बाकी" label.
- **Publish run (08:00 and 18:00):** read the draft from branch `drafts`, look in Gmail for the editor's reply in that thread (from sahukk@gmail.com), apply the instructions, set `unreviewed` false if the editor replied (OK or edits), true otherwise, skip if `रोको`, copy to `data/bulletins/`, publish with tools/publish.py. Also: if the editor has since replied OK to an earlier already-published unreviewed bulletin, remove its `unreviewed` flag. Then send a one-line confirmation email: "प्रकाशित: https://ankurx.in/#b-<id>".

# "Anokhi Duniya, Is Hafte" — weekly section rules

Section page: https://ankurx.in/anokhi/ . Tagline: "क्या यह कल बदलेगा?" (will this change tomorrow?).
**ONE in-depth article per week**, published **Sunday 10:00 IST**. Editor: see EDITORIAL.md (same editor, same email).
The editor approves twice before writing starts (pick 2 of 10, then 1 of 2) and once more before publishing.

## Weekly flow (times IST; edition date = the coming Sunday)
1. **Thursday 18:00 — SCOUT (cloud routine "AnkurX Anokhi scout").** Screen Monday–Thursday of this week for the most
   talked-about *unusual, surprising, funny, scientific, space, technology, nature, art or culture* happenings worldwide and
   in India. Shortlist the **10 best** candidates. Write `drafts/anokhi-<sunday>-shortlist.md` on branch `drafts` and email
   the editor (subject `AnkurX अनोखी दुनिया: शॉर्टलिस्ट <sunday date in Hindi>`), numbered 1–10, each: one-line Hindi
   summary, category, why it is anokha, could it change the future (one phrase), 2 sources (outlet, date, link).
   Reply instruction in the email: **`चुनें: 3, 8`** (pick exactly 2), optional `सवाल 3: …`, `अपनी खबर: …`.
2. **Friday 09:00 — BRIEFS (cloud routine "AnkurX Anokhi briefs").** Read the editor's reply in that shortlist thread.
   For the 2 picked items, verify deeply (2+ independent reliable sources, primary source such as the paper/official
   release, fact-checkers if viral) and write a **brief** of each (Hindi, ~250–400 words): what exactly happened (date, who,
   where), is it confirmed (and any doubts), background/origin, why it matters, known controversies or criticism, possible
   future impact, free pictures available, and full source links. Save `drafts/anokhi-<sunday>-briefs.md` on branch
   `drafts` and email both briefs in the same thread. Reply instruction: **`अंतिम: 3`** (choose 1).
   If the editor has not replied with 2 picks, send a one-line reminder in the thread and stop.
3. **Saturday — ARTICLE (in a Claude session with the editor).** Write ONE full article on the chosen topic:
   `lekh/anokhi-<sunday>-<topic-slug>/article_body.html`, sections: the story (what happened), origin/history,
   how it works / the science, impact, controversies and other views, **क्या यह कल बदलेगा?** (AnkurX's balanced view),
   sources. Lively, simple Hindi; photos per the picture rules. Export to Word for the editor (tools/lekh_to_docx.py).
4. **Editor's final approval → publish Sunday 10:00**, then post on WhatsApp channel, Facebook (page + editor's profile),
   X, Instagram, LinkedIn. Add the slug to ARTICLES and ANOKHI in tools/build_lekh.py.

## What counts as a good candidate
- Surprising, delightful or mind-opening: science discoveries, space, animals and nature, inventions, health research
  (peer-reviewed or official only), records, art and culture, funny-but-true happenings, viral things that turn out true.
- The 10 should be a mix: science/space/tech, nature/animal, art/culture, funny/viral, and at least 1 India story.
- Must have depth for a full article (origin, impact, debate, future) — not just a one-day curiosity.
- Prefer topics a young reader in North Bihar would share with a friend: "अरे, ऐसा भी होता है!"
- The event (or the news of it) must fall in this week's Monday–Thursday window. An older discovery is allowed only if
  this week brought something new about it, and the text must say clearly what is old and what is new.

## Hard rules
- **Truth first.** A viral item is used only if verified; a fake one can appear only as "वायरल का सच" (explaining that it is
  false, with a fact-checker source). Never present an unverified claim as fact.
- Sources: major news agencies and newspapers, science journals and their press releases, NASA/ISRO/ESA, universities,
  museums, WHO/ICMR, recognised fact-checkers (Alt News, BOOM, PIB Fact Check, AFP Fact Check). Prefer direct links over
  Google News redirect links. Never bypass bot-blocking (see EDITORIAL.md "How to collect").
- Same exclusions as EDITORIAL.md rule 5 (no crime, violence, deaths, communal/caste conflict, party politics, minors as
  victims, health claims without official/peer-reviewed source). Humour never mocks a person or community.
- Write fresh, simple, lively Hindi in our own words. Never copy sentences or photos.
- **Pictures:** only NASA/ESA/ISRO public images, Wikimedia Commons with licence + credit, official press images where reuse is
  allowed (with credit), embedded original posts (YouTube/X/Instagram), or AnkurX-made cards. Never download news-site photos.

## Article markup (inside article_body.html)
Standard lekh article (`<article class="lekh">`, kicker linking /anokhi/, h1, byline, lede, h2 sections, figures).
End with `<div class="kal"><b>क्या यह कल बदलेगा?</b> …</div>` and an `<h2>स्रोत</h2>` list.

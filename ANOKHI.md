# "Anokhi Duniya, Is Hafte" — weekly section rules

Section page: https://ankurx.in/anokhi/ . Tagline: "क्या यह कल बदलेगा?" (will this change tomorrow?).
One edition per week, **7 stories**, published **Friday 19:00 IST**, reminder posts Sunday morning.
Editor: see EDITORIAL.md (same editor, same email address).

## Weekly flow
1. **Wednesday 08:00 IST — scout (cloud routine).** Find the week's most talked-about *unusual, surprising, funny,
   scientific, space, technology, nature, art or culture* happenings worldwide (and India) from the last 7 days.
   Shortlist **10 candidates**, write the shortlist to branch `drafts` as `drafts/anokhi-<friday-date>-shortlist.md`,
   and email the editor (subject: `AnkurX अनोखी दुनिया: शॉर्टलिस्ट <friday date>`), numbered 1–10, each with:
   a one-line Hindi summary, category, why it is "anokha", whether it could change the future (one phrase),
   2 sources (outlet + date + link). Reply instructions in the email: `चुनें: 2, 5, 7, …` (pick 7),
   `सवाल 3: …` (question about an item), `अपनी खबर: …` (editor adds own item).
2. **Wednesday–Thursday — research and writing (in a Claude session with the editor, not automated).**
   For each picked story: confirm it is real (2+ independent reliable sources; check fact-checkers if viral),
   background/history, what experts say, and "क्या यह कल बदलेगा?" (AnkurX's balanced view, no hype).
   Write the edition as a lekh article: `lekh/anokhi-<YYYY-MM-DD>/article_body.html` (date = Friday),
   add to ARTICLES and ANOKHI in tools/build_lekh.py. Export to Word for the editor (tools/lekh_to_docx.py).
3. **Friday — editor approves**, then publish at 19:00 IST and post on WhatsApp channel, Facebook (page + editor's
   profile), X, Instagram, LinkedIn. Sunday morning: one reminder post (best story as a teaser).

## What counts as a good candidate
- Surprising, delightful, or mind-opening: science discoveries, space, animals and nature, inventions, health research
  (peer-reviewed or official only), records, art and culture, funny-but-true happenings, viral things that turn out true.
- Mix every week: at least 2 science/space/tech, 1 nature/animal, 1 art/culture, 1 funny/viral; at least 1 India story.
- Prefer things a young reader in North Bihar would share with a friend: "अरे, ऐसा भी होता है!"

## Hard rules
- **Truth first.** A viral item is used only if verified; if it turned out fake, it can be a story *only* as
  "वायरल का सच" (explaining that it is false, with a fact-checker source). Never present an unverified claim as fact.
- Sources: major news agencies and newspapers, science journals and their press releases (Nature, Science, etc.),
  NASA/ISRO/ESA, universities, museums, WHO/ICMR, recognised fact-checkers (Alt News, BOOM, PIB Fact Check, AFP Fact Check).
  Use RSS/feeds and official pages; never bypass bot-blocking (see EDITORIAL.md "How to collect").
- Same exclusions as EDITORIAL.md rule 5 (no crime, violence, deaths, communal/caste conflict, party politics, minors as
  victims, health claims without official/peer-reviewed source). Nothing cruel to animals or people; humour never mocks
  a person or community.
- Write fresh, simple, lively Hindi in our own words. Never copy sentences or photos.
- **Pictures:** only (a) NASA/ESA/ISRO public images, (b) Wikimedia Commons with licence + credit, (c) official press
  images where reuse is allowed, with credit, (d) the original post embedded (YouTube/X/Instagram embed code),
  (e) AnkurX-made illustration cards. Never download photos from news sites.
- Every story ends with a `क्या यह कल बदलेगा?` box and lists its sources.

## Article markup (inside article_body.html)
```html
<div class="story">
  <span class="tag">विज्ञान</span>
  <h2>1. …headline…</h2>
  <p>…story…</p>
  <figure>…</figure>  or  <div class="embed">…embed code…</div>
  <div class="kal"><b>क्या यह कल बदलेगा?</b> …</div>
  <p class="sach">स्रोत: …</p>
</div>
```

# Tauranga Golf Club — Heritage & Club Life

Member review website extending Dave Mowat’s *Pars from the Past* (2014), with six historical chapters covering **1903–2014**, plus the complete original book collection. The existing club website is untouched.

## Run locally

Python 3 is the only build requirement. No packages or JavaScript installation needed.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8033 --bind 127.0.0.1
```

Open http://127.0.0.1:8033. Stop with Ctrl-C.

## Structure and editing

- `content/collection.json`: 41 story introductions, 53 milestones, 15 selected archive records, five club groups and chapter metadata.
- `content/book.json`: all 305 source pages organised into 25 chapters, front matter and appendices; 87 substantial embedded images are indexed by source page.
- `scripts/build.py`: generates static HTML pages from content and shared templates.
- `scripts/book_views.py`: original book chapters, page reader, complete image gallery and search interface.
- `scripts/import_book.py`: reproducible PDF text/image import; requires PyMuPDF only when reimporting the supplied source. The normal build needs only Python’s standard library.
- `assets/style.css`: responsive presentation, aligned with the club’s logo, white header and green accents.
- `assets/*.jpg`: web-sized images extracted from the supplied book, plus the existing club logo.
- `.github/ISSUE_TEMPLATE/member-feedback.yml`: a form for member corrections, contributions and website feedback.

Edit content, rebuild, then run the checks. Generated HTML is tracked so GitHub Pages can serve it directly. Internal paths are relative and work beneath the repository’s Pages path.

Stories have `era`, `groups`, `record_type`, `source_kind`, `review_status`, book page references and optional `external_sources`. Shared stories can appear in more than one club group without duplication. `review_status: draft` marks material open for historical review; this edition deliberately displays draft historical stories for member feedback.

The `records` array supports new dated club contributions separately from book adaptations. Fields: `title`, `date` (ISO `YYYY-MM-DD`), `groups` (group IDs), `summary`, `body`, `contributor`, `source`, `review_status`. Only `approved` records render; they sort newest first within each club group. All content is HTML escaped.

Chapter IDs: `beginnings` (1903–1923), `interwar` (1924–1945), `postwar` (1946–1959), `sixties` (1960–1979), `eighties` (1980–1999), `modern` (2000–2014). Add a chapter object with `id`, `title`, `years`, `status`, and `link` to generate a populated chapter page. Timeline entries are assigned by their event date, independently of introductions that span several eras.

## Historical sources and permissions

Book: *Pars from the Past*, edited by David G. S. Mowat, 2014. Printed page numbers match PDF page numbers. The original PDF stays **outside this repository** and is ignored by Git. Do not upload it or place it in website output.

Supporting sources:
- https://www.taurangagolf.co.nz/history?ComeFromCat=1338
- Luke Balvert, “A hole in 100”, SunLive, 15 November 2014: https://www.sunlive.co.nz/news/87217-a-hole-100.html

The project owner authorised all photographs and images for publication on 9 November 2026. Each extracted image retains a page reference, credit where available, date uncertainty and permission record. Images were resized/compressed without generating new historical detail. The club logo is unchanged, sourced from https://www.taurangagolf.co.nz/clubs/400-2/images/club-logo.jpg.

Historical material remains open to correction. Known conflicting details in the source book are explicitly identified in the relevant stories. Newspaper originals have not yet been independently checked. Nine-hole golf’s national initiative, local 1977 provision and 1998 launch are distinguished rather than conflated.

## Share and publish the review edition

The owner requested a GitHub-hosted edition for member feedback on 9 November 2026. This supersedes the earlier local-only prototype stage. Publication is a **review edition**, not a statement of final historical approval.

Target repository: https://github.com/bwucee/Tauranga-Golf-Club-Heritage

GitHub Pages should serve `main`, root folder, using the generated HTML and `.nojekyll`. To configure manually: Settings → Pages → Deploy from a branch → main → /(root). The standard URL is https://bwucee.github.io/Tauranga-Golf-Club-Heritage/; verify deployment before sharing it.

This repository and its Pages site are public. Sharing the link with a few members does not limit who can access it. `noindex` metadata and `robots.txt` discourage search indexing but do not restrict access.

Feedback links open the repository’s issue form. A GitHub account is needed to submit an issue; feedback is public. Members without an account can reply directly to whoever shared the site, using the page link and suggested change. No messages are submitted or stored by the static website itself.

For updates, rebuild and check, commit the approved changes and push to `main`; GitHub Pages republishes that branch. There is no separate framework build or automatic deployment to the operational club website.

## Repository authorship

Project updates use Bruce Partridge (`bwucee@gmail.com`) as the repository-local Git author. This keeps the project separate from other club identities configured on the same computer.

## Full-book edition

All 25 chapters are available as original, attributed review transcriptions, with separate short story introductions. Front matter, captions, source page numbering and appendices are retained. The PDF itself is not served. Some extraction corrections and proofreading remain; this is explicit in the reader. Running headers and narrow bleed/layout fragments are removed. Three chapter-title fonts that did not extract correctly were transcribed after visual inspection.

The 19 original-layout appendix pages preserve table columns. Their searchable extraction is explicitly not a substitute for the original layout. The final chapter’s imagined future is labelled on every source page and excluded from the factual timeline. References to present-day rules, personnel or programmes within source text refer to 2014, not the present.

Search loads `assets/search-index.json` only when needed and runs in the browser. It covers 305 source pages and all 41 introductions, with links to permanent page URLs. No query goes to an external search service. Book images load lazily within chapter groups, keeping the home page light.

To reimport from the separately retained PDF, use an environment with PyMuPDF: `python scripts/import_book.py /absolute/path/to/source.pdf`, then run the standard build and checks. Keep the source PDF outside the checkout. Reimporting is unnecessary for normal editorial changes to the JSON.

Checks verify links, script/image paths, source exclusion, all 305 page routes, the 25-chapter sequence, appendix facsimiles, speculation notices and search targets. Browser QA covers search, topic expansion, source reading, a reference page and mobile widths.

The incorrect motorcycle-club author on the early website commit was corrected on 9 November 2026. The original history is recoverable in a local Git backup ref; the public main branch uses Bruce Partridge’s identity.

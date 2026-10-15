# tools/checks

Scripts the website maintainer used for the September 2026 verification-stack batch and PG-016. Each file's first line says what it does and how to run it. Most carry hard-coded paths from the session that wrote them (scratchpad, upload directory, repo path): check and adjust before running. Requirements: python-docx, pypdf, pymupdf (optional), Node with Playwright; Chromium at /opt/pw-browsers/chromium; serve the repo with `python3 -m http.server 8766` for the *.js checks.

- Page rebuilds from Word: vbuild.py (CVP/IVP/CRD), sf40.py + sf40b.py (TCAP), splice.py (older, generic); libraries conv.py and dx.py; vpost.py for citations and head descriptions.
- Practitioner Guide page from markdown: pg_build.py.
- Checks: linecheck.py (page vs PDF, all papers), duo.py (Word vs PDF), trio.py (Word vs PDF vs markdown), sdiff.py (sentence diff between versions), md5check.sh (site PDFs vs Zenodo MD5s), opscheck.py (ops-file edit check).
- Claim language: claimcheck.py lists empirical-sounding words in the site pages that summarize the papers (About, FAQ, Glossary, Founder, research.html, updates.html, the homepage), for review, never auto-fix (09_instance_briefing Section 2.3, "Say whose claim it is"). Run it after editing any of those pages. On 2026-10-15, after PRs #62 to #66, its 55 remaining hits were all correct uses (cited outside work, definitions in observable terms, explicit disclaimers).
- Rendering: cshot.js, pgshot.js, vshot.js, tshot.js.
- companion.py is a record of edits already applied (PR #39), not a tool to re-run.

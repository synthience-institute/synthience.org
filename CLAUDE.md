# Working on this repository

This repository is the Synthience Institute website (synthience.org), served by GitHub Pages from `main`. Anything merged to `main` goes live within minutes.

## Where the rules live

The Institute's operations files are the authority. This file only points to them. Ask the PCP (Thomas W. Gantz) to upload the current versions before any website work:

- **08_site_ops**: site architecture, the publication checklist, index-page sorting.
- **15_word_production_spec**: paper pages, the Google Scholar tags, and the Website Publication Workflow for new papers and new versions.
- **01_canon_published** and **17_Paper_DOIs**: each paper's current version, title and concept DOI.
- **10_social_pipeline**: Field Notes and Practitioner Guides, with titles and publication dates.

If those files and this one disagree, the operations files win.

## Standing conventions (reminders; details are in the files above)

- **Change only what was asked.** Don't touch article text in `research/`, `field-notes/` or `practitioner-guides/` unless the request names it.
- **Concept DOIs** for Institute papers. Outside works keep the DOI of the version cited.
- **Version numbers** appear only on a paper's own page (meta block and footer). Nothing else refers to a specific version.
- **`research/pdf/<ID>.pdf`** is the exact PDF on Zenodo, byte for byte, named by document ID only. A new Zenodo version replaces the file under the same name and updates the paper's page to match.
- **`updates.html`** announces new pieces only, never new versions or corrections. After adding an entry, rebuild the RSS feed with `node tools/build-feed.js`, which regenerates `feed.xml` from updates.html. **`sitemap.xml`** changes only when a page is added.
- **Images:** export as JPEG (quality about 85 to 88) before upload, keeping the original pixel size.

## How changes are made

1. Work on a branch and open one pull request per request.
2. List every change in the PR as before/after.
3. Merge when the PCP says to publish.
4. Check pages in a headless browser before merging. Chromium is at `/opt/pw-browsers/chromium`.

## Environment notes (Claude Code on the web)

- **Blocked:** zenodo.org, doi.org, api.datacite.org and synthience.org are unreachable from the cloud container. New PDFs have to be uploaded by the PCP.
- **Google Drive connector:** it can find and read files, but it can't copy them into the repository.

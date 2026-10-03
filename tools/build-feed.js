// Builds feed.xml (RSS 2.0) from the allUpdates array in updates.html.
// Run from the repository root after adding a new entry to updates.html:
//   node tools/build-feed.js
// The feed lists new pieces only, exactly as updates.html does.

const fs = require('fs');
const vm = require('vm');

const SITE = 'https://synthience.org/';
const html = fs.readFileSync('updates.html', 'utf8');

// Extract and evaluate the allUpdates array literal.
const start = html.indexOf('var allUpdates = [');
if (start < 0) throw new Error('allUpdates not found in updates.html');
let depth = 0, end = -1;
for (let i = html.indexOf('[', start); i < html.length; i++) {
  if (html[i] === '[') depth++;
  else if (html[i] === ']') { depth--; if (depth === 0) { end = i + 1; break; } }
}
const updates = vm.runInNewContext('(' + html.slice(html.indexOf('[', start), end) + ')');

// Newest first: date descending, then dateOrder descending (08_site_ops Section 3.1).
updates.sort((a, b) => (b.date || '').localeCompare(a.date || '') || (b.dateOrder || 0) - (a.dateOrder || 0));

const entities = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', mdash: '—', ndash: '–',
  rsquo: '’', lsquo: '‘', rdquo: '”', ldquo: '“', hellip: '…', middot: '·', rarr: '→', larr: '←' };
const decode = s => String(s || '')
  .replace(/<[^>]+>/g, '')
  .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
  .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(+d))
  .replace(/&([a-z]+);/gi, (m, n) => entities[n] !== undefined ? entities[n] : m);
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const rfc822 = d => new Date(d + 'T00:00:00Z').toUTCString().replace('GMT', '+0000');

const items = updates.map(u => {
  // Entries without a single page (e.g. several papers announced together) link to the Research page.
  const url = /^https?:\/\//.test(u.link || '') ? u.link : SITE + (u.link || 'research.html');
  return [
    '    <item>',
    `      <title>${esc(decode(u.title))}</title>`,
    `      <link>${esc(url)}</link>`,
    `      <guid isPermaLink="false">${esc(u.date + ' ' + url)}</guid>`,
    `      <pubDate>${rfc822(u.date)}</pubDate>`,
    u.tag ? `      <category>${esc(decode(u.tag))}</category>` : null,
    `      <description>${esc(decode(u.body))}</description>`,
    '    </item>'
  ].filter(Boolean).join('\n');
});

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Synthience Institute</title>
    <link>${SITE}</link>
    <atom:link href="${SITE}feed.xml" rel="self" type="application/rss+xml"/>
    <description>New papers, Field Notes and Practitioner Guides from the Synthience Institute.</description>
    <language>en</language>
    <lastBuildDate>${rfc822(updates[0].date)}</lastBuildDate>
${items.join('\n')}
  </channel>
</rss>
`;
fs.writeFileSync('feed.xml', xml);
console.log(`feed.xml written: ${updates.length} items, newest ${updates[0].date} (${decode(updates[0].title)})`);

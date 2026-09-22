# Pasting the fifteen pages into Webflow

Each `.json` file is one page, transpiled straight from the artboards you approved, so the copy and the
styling cannot have drifted from what you signed off.

## Order

Paste in numbered order. Home first, because it defines most of the shared classes and every later page
reuses them.

| File | Webflow page |
|---|---|
| `01-home.json` | `/` |
| `02-waypoint.json` | `/waypoint` |
| `03-salesforce.json` | `/salesforce` |
| `04-about.json` | `/about` |
| `05-contact.json` | `/contact` |
| `06-storeconnect.json` | `/storeconnect` |
| `07-lumin.json` | `/lumin` |
| `08-gridmate.json` | `/gridmate` |
| `09-nonprofit.json` | `/nonprofit` |
| `10-npsp-migration.json` | `/nonprofit/npsp-migration` |
| `11-marketing-cloud-next.json` | `/marketing-cloud-next` |
| `12-work.json` | `/work` |
| `13-work-heritage.json` | `/work/heritage-unified-profile` |
| `14-work-retirement-living.json` | `/work/retirement-living-routing` |
| `15-work-marketing-cloud-next.json` | `/work/first-marketing-cloud-next-apac` |

Titles, meta descriptions and redirects for all fifteen are in `../SEO.md`.

**Test `01-home.json` on a blank page before doing the other fourteen.** The clipboard format is
undocumented. If it has moved, one fix to `wf_transpile.py` regenerates all fifteen, but there is no point
discovering that on page nine.

To paste: open the file, select all, copy, click the Webflow canvas so it has focus, paste.

## Three things that will not come across

**1. The logo** is a grey placeholder block, 130×28. Your logo already lives in your Webflow assets, so
replace the block with an Image element pointing at it. Fifteen times, or once if you make the nav a
Component first, which you should.

**2. The Salesforce Partner badge** is the dashed slot, 168×97. Drop the real asset in.

**3. Fonts** resolve only if railroad-gothic-atf is in the site's font list. It is already loaded via
Typekit on the current site, so it should be there, but check before deciding the headings look wrong.

## Do this after the first paste, before the other fourteen

Convert the **nav**, the **footer** and the **CTA band** into Components. All three are identical on every
page, and pasting fifteen unlinked copies is how you end up maintaining fifteen navs. Once they are
Components, delete the pasted copies on pages 2 to 15 and drop the instances in.

## About the classes

Be straight about what this is. The transpiler produced **266 classes**. The hand-build described in
`BUILD-GUIDE.md` would produce roughly 40.

It is not as bad as that number reads: about 150 of them cover ~94% of all class applications, and the names are
sensible at the top of the system — `tag`, `body`, `h-card`, `h-section`, `btn-primary`, `card-gradient-teal`,
`section-wash`. The long tail is genuinely one-off layout boxes, named `wrap`, `row`, `col`, `stack` with
numeric suffixes.

**So choose deliberately:**

- **Paste, then tidy.** Fastest to a site that looks right. You get every page's structure and copy without
  retyping forty thousand words. Budget a day afterwards to merge the one-off classes and rename the
  `wrap-n` boxes. Best if you want this live soon.
- **Build by hand from `BUILD-GUIDE.md`.** Slower to first pixel, cleaner forever, roughly seven to nine
  days. Best if this site is going to be edited weekly by someone who is not a developer.
- **Hybrid, which is what I would do.** Build the nav, footer, CTA and the card components by hand from the
  guide so the reusable parts are clean. Paste the long content pages and restyle their boxes onto your own
  classes. The copy is the part you do not want to retype; the chrome is the part you want to own.

## The diagrams

Nine heroes came across as HTML Embeds carrying their SVG, so they should just work. The icons inside cards
also became embeds — that is why StoreConnect has eleven and Waypoint has seven. They render fine but show
as grey boxes on the Designer canvas, which makes building around them awkward. If that bothers you, the
standalone SVGs are in `../embeds/` and can be uploaded as assets and used as Images instead.

## Regenerating

Run `python3 generate.py`. It rebuilds all fifteen files from the artboards in one pass, with the shared
class registry, and prints the node and class counts. If a page needs changing, change the artboard and
regenerate. Do not hand-edit the JSON.

Two placeholders on About worth knowing about: the hero and the founder portrait are dashed photo slots,
because About is the one page in the system that carries photography.

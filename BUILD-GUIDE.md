# Building this in Webflow

Your site is already Webflow (site `640fd7a17975fd87bdec31ea`), railroad-gothic-atf is already loaded via
Typekit and Inter is already loaded via Google Fonts. Nothing needs replatforming. This is a rebuild
inside the site you have.

**The design is done, so this is a Webflow build, not a design job.** Estimate for someone fluent in
Webflow: roughly a day to set up variables and components, then two to four hours per page once those
exist. Twelve pages plus CMS, responsive and QA lands around seven to nine working days. It is faster than
that if you accept the first three pages will be slow while the component set settles.

**Build order matters.** Variables, then base classes, then components, then pages. Building pages first
and extracting components later is how Webflow projects end up with two hundred classes and a style panel
nobody will touch.

---

## Step 1: Variables

Style panel → Variables. Create four collections and add these. Every colour in the build references a
variable, never a hex typed into a style.

**Collection: Ground**

| Variable | Value |
|---|---|
| `white` | `#FFFFFF` |
| `mist` | `#F4F8FC` |
| `wash-top` | `#FFFFFF` |
| `wash-bottom` | `#E6F1FB` |
| `tint-green` | `#E8FCF2` |

**Collection: Ink**

| Variable | Value |
|---|---|
| `ink` | `#0C2B4B` |
| `slate` | `#47566B` |
| `muted` | `#5D7290` |
| `hairline` | `#DCE6F0` |
| `border-strong` | `#C5D6E8` |

**Collection: Accent**

| Variable | Value |
|---|---|
| `green` | `#1EE885` |
| `green-ink` | `#0A6B44` |
| `green-hover` | `#085434` |
| `deep-blue` | `#175C93` |
| `deep-teal` | `#12795A` |
| `cyan` | `#17739A` |
| `violet` | `#7A5AF8` |

**Collection: Shape** (Size variables)

| Variable | Value |
|---|---|
| `radius-card` | `24px` |
| `radius-card-sm` | `20px` |
| `radius-inner` | `16px` |
| `radius-tag` | `3px` |
| `radius-pill` | `999px` |
| `gutter` | `80px` |
| `section-y` | `96px` |

Webflow cannot store a gradient in a variable. The four gradients get their own combo classes instead, in
step 2.

---

## Step 2: Base styles

### Container and sections

| Class | Styles |
|---|---|
| `.container` | width 100%, max-width 1280px, margin 0 auto |
| `.section` | padding `section-y` top and bottom |
| `.section.is-mist` | background `mist` |
| `.section.is-wash` | background `linear-gradient(180deg, #FFFFFF 0%, #E6F1FB 100%)` |
| `.section.is-hairline` | border-top and border-bottom 1px `hairline` |

At 1440 the 1280 container leaves 80px gutters, which is what the design assumes.

### Type

| Class | Font | Size | Weight | Colour | Notes |
|---|---|---|---|---|---|
| `.h-display` | railroad-gothic-atf | 58px | 600 | `ink` | Page H1. Letter-spacing -0.02em |
| `.h-section` | railroad-gothic-atf | 44px | 600 | `ink` | Section H2 |
| `.h-card` | railroad-gothic-atf | 24px | 600 | `ink` | Card H3 |
| `.h-card.is-on-gradient` | | | | `white` | |
| `.body-lg` | Inter | 19px | 400 | `slate` | Hero sub, section lead at 18px |
| `.body` | Inter | 16px | 400 | `slate` | |
| `.body-sm` | Inter | 15px | 400 | `slate` | Card body |
| `.caption` | Inter | 14px | 400 | `muted` | Fine print |

Line height: 1.07 on display, 1.12 on section headings, 1.65 to 1.7 on body.

### The four gradients

Combo classes on `.card-gradient`:

| Class | Value |
|---|---|
| `.is-teal` | `linear-gradient(150deg, #0B5C45 0%, #12795A 100%)` |
| `.is-cyan` | `linear-gradient(150deg, #0E5470 0%, #17739A 100%)` |
| `.is-blue` | `linear-gradient(150deg, #143F6B 0%, #1E5E93 100%)` |
| `.is-navy` | `linear-gradient(150deg, #0C2B4B 0%, #16436B 100%)` |

Body text inside them: `#D3E9DF`, `#D0E6F0`, `#CEDFEC`, `#C9D8E6` respectively. Those four are the only
places a colour is typed rather than referenced, and it is not worth five more variables.

---

## Step 3: Components

Build these before any page. Component properties need a paid Workspace plan; check yours before relying
on them, and use symbols with manual overrides if not.

| Component | Properties | Used on |
|---|---|---|
| `Nav` | active link (visibility) | Every page |
| `CTA band` | heading, body, fine print, button label | Every page |
| `Card / white` | heading, body, optional green rule | Most pages |
| `Card / gradient` | heading, body, gradient variant | Stack, products, capabilities |
| `Card / float` | heading, body | Cards sitting on mist or wash |
| `Row / numbered` | number, heading, body | How-we-work sections |
| `Tag` | label | Chip rows |
| `Diagram shell` | title, status, caption, embed slot | Every hero |
| `Strip / tags` | left label, tags | Sector and compliance strips |

### Buttons

| Class | Background | Text | Padding | Radius |
|---|---|---|---|---|
| `.btn` | `green` | `ink` | 17px 32px | `radius-pill` |
| `.btn.is-ink` | `ink` | white | 17px 32px | `radius-pill` |
| `.btn.is-outline` | white, 1px `border-strong` | `ink` | 16px 32px | `radius-pill` |
| `.btn.is-nav` | `green` | `ink` | 12px 26px | `radius-pill` |

**Ink on green, never white.** White on `#1EE885` measures 1.6:1 and fails at every size. This is the one
rule in the build that is not a preference.

### Tags

`.tag`: no fill, 1px `hairline`, `radius-tag`, `slate`, 13px, 400 weight, padding 6px 11px, sentence case.

**Not pills, not uppercase, not letterspaced.** That combination is what made the earlier version read as
machine-made. Fully rounded is reserved for buttons and for the 52×4 green rule that opens a card.

---

## Step 4: Pages, in build order

Build Home first because it exercises almost every component. Build Waypoint second because it is the
product you most need live.

| # | Page | URL | Notes |
|---|---|---|---|
| 1 | Home | `/` | Stack graphic is HTML, not an embed. See step 5 |
| 2 | Waypoint | `/waypoint` | New flagship. `/quick-starts` redirects here |
| 3 | Salesforce | `/salesforce` | Replaces the practice-area tiles on the old home |
| 4 | Contact | `/contact` | Form: see step 7 |
| 5 | StoreConnect | `/storeconnect` | Do not publish until the partner listing is live |
| 6 | Lumin Sign | `/lumin` | |
| 7 | GridMate | `/gridmate` | Includes the RevenueMate section |
| 8 | Nonprofit Cloud | `/nonprofit` | |
| 9 | NPSP migration | `/nonprofit/npsp-migration` | Keep the honesty block |
| 10 | Marketing Cloud Next | `/marketing-cloud-next` | |
| 11 | Case studies index | `/work` | |
| 12 | Case study template | `/work/:slug` | CMS, see step 6 |

Nav: The stack · Salesforce · Products · Waypoint · Nonprofit · Marketing · Work, plus Contact us as the
green button. Products is a dropdown to StoreConnect, Lumin and GridMate.

---

## Step 5: The diagrams

Nine of the ten heroes are a single inline SVG, sitting inside the diagram shell component. They are in
`embeds/` beside this file, one per page.

**How:** drop an HTML Embed element into the shell's diagram slot, paste the file contents, set the embed
wrapper to width 100%. The SVG carries `width="100%"` and a viewBox, so it scales to whatever column it
sits in and stays sharp at any size.

| File | Page |
|---|---|
| `waypoint-loop.html` | Waypoint |
| `storeconnect-convergence.html` | StoreConnect |
| `lumin-pipeline.html` | Lumin |
| `gridmate-grid.html` | GridMate |
| `nonprofit-hub.html` | Nonprofit Cloud |
| `npsp-model-map.html` | NPSP migration |
| `mcnext-journey.html` | Marketing Cloud Next |
| `case-heritage-resolution.html` | Case: heritage |
| `case-routing-fan.html` | Case: retirement living |

**Two things to know.** Embeds do not render on the Designer canvas, only in Preview and on the published
site, so the diagram will look like an empty grey box while you build around it. And the Embed element
caps at 50,000 characters; the largest of these is under 5,000, so there is room to spare.

**The Home stack graphic is not an embed.** It is four stacked flex rows with gradient backgrounds and
tag chips, which Webflow builds natively and your team can then edit without touching code. Build it as a
component with four instances.

**Editing a diagram later:** open the file, change the text, repaste. They are plain SVG. If the geometry
needs to move rather than the words, send it back to me.

---

## Step 6: CMS for case studies

Three studies does not need a CMS. Twelve will, and the SEO template is worth having from the start.

**Collection: Case studies**

| Field | Type | Notes |
|---|---|---|
| Name | Plain text | |
| Slug | Slug | |
| Sector | Plain text | Breadcrumb and index card |
| Card summary | Plain text | Index page only |
| Tags | Plain text | Comma separated, split in the template |
| Hero title | Plain text | Diagram shell title |
| Hero status | Plain text | Diagram shell status |
| Hero caption | Plain text | |
| Hero embed | Code / rich text | Paste the SVG here |
| Situation | Rich text | |
| What we built | Rich text | Numbered list, styled via the rich text class |
| What changed | Rich text | Three headings with body |
| What we would tell you | Rich text | The honesty block |

Style the rich text once with a `.rich-text` class and nested selectors. Do not build the body from
separate fields per paragraph; it will not survive the fourth case study.

**Case 3 is unfinished on purpose.** The bracketed placeholders are facts only you can supply. Either
fill them before publishing or unpublish that item and run the index with two.

---

## Step 7: Responsive

Webflow breakpoints, and what changes at each:

| Breakpoint | Changes |
|---|---|
| Base (1440 and up) | As designed. Container 1280 |
| 1280 | Container fills with 40px side padding. No layout change |
| 991 (tablet) | Hero stacks: copy above diagram. Three-column grids become two. Display 44px, section 34px |
| 767 (mobile landscape) | All grids single column. Section padding 64px. Nav becomes the hamburger |
| 479 (mobile portrait) | Container padding 24px. Display 36px, section 30px. Buttons full width, stacked |

The mobile artboard on the canvas shows this at 390 for StoreConnect. Every other page stacks the same
way, so build one page's mobile view carefully and the rest follow.

**The diagrams are the responsive risk.** They scale by viewBox, so at 390 wide the text inside gets
small. On the three densest (`npsp-model-map`, `case-routing-fan`, `gridmate-grid`) set the embed wrapper
to `overflow-x: auto` at mobile, or hide the diagram below 767 and show a short text summary instead.
Hiding is the better answer for GridMate specifically: a grid that needs horizontal scrolling on a phone
makes the opposite of the page's point.

---

## Step 8: Launch checklist

- [ ] **301 redirect** `/quick-starts` → `/waypoint`. Site settings → Publishing → 301 redirects.
- [ ] **Old practice-area anchors** from the current home page redirected to `/salesforce`.
- [ ] **SEO title and meta description** per page. The copy docs carry them for Home and StoreConnect;
      write the rest to the same pattern.
- [ ] **Open Graph image** per page. The hero diagram on a white ground crops well.
- [ ] **Contact form.** You already run HubSpot (`js.hs-scripts.com/5754742`). Either embed the HubSpot
      form or use a Webflow form and map it. Do not build a Webflow form that emails only, or enquiries
      will not appear in the CRM you are selling.
- [ ] **Form source field** set to the page, so StoreConnect and Waypoint enquiries are separable.
- [ ] **Alt text** on the logo and any photography. The SVGs carry `role="img"`; add an `aria-label` on
      each embed wrapper describing what the diagram shows.
- [ ] **Contrast pass.** Nothing should use white text on `#1EE885`. Check the old pages too.
- [ ] **StoreConnect page held back** until Enable is listed on storeconnect.com/partners.

---

## What not to do

**Do not paste whole pages in as embeds.** It will look right on day one and be unmaintainable on day
thirty, and nobody but a developer will be able to change a word. Embeds are for the SVG diagrams only.

**Do not skip variables and type hexes into styles.** The palette will drift within a month, and the
contrast fix in particular will get quietly undone by someone matching a colour by eye.

**Do not reintroduce the pills.** Uppercase letterspaced labels above headings, fully rounded tint pills
on small text, and decorative badges repeating the card heading. Those three are what made the earlier
version read as machine-made, and they will creep back in unless someone says no.

**Do not build the gradient cards as images.** They are backgrounds with live text. As images they stop
being editable, stop being selectable by search engines, and go blurry on retina.

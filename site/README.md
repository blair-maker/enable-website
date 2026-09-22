# Enable, as code

Fifteen static pages and one stylesheet, generated from the approved artboards. No build step, no
dependencies, no webfont requests. Open `index.html` or serve the folder.

```
python3 -m http.server 8422
```

## What is here

| | |
|---|---|
| `index.html` and 14 more | One page each, semantic HTML, classes only, no inline styles |
| `styles.css` | Every class, the tokens as custom properties, and the responsive rules |
| `assets/` | The logo |

Internal links all resolve. The hero diagrams are inline SVG, so they scale and stay sharp.

## Type

**System UI throughout.** Railroad Gothic ATF is retired: it is a caps-only titling face, which is why it
fought every sentence-case heading. The stack is `system-ui, -apple-system, Segoe UI, Roboto,
Helvetica Neue, Arial, sans-serif`. It renders natively, loads instantly, and costs nothing.

This also means **no Typekit and no Google Fonts requests at all**. Two fewer third parties, and the text
paints on first frame.

## Responsive

Two breakpoints, matching `../BUILD-GUIDE.md`:

- **1100px** — hero stacks copy above diagram, three-column grids become two, fixed-width columns go full
  width, headings scale to 76%, nav collapses to logo plus Contact us.
- **760px** — everything single column, headings to 60%, section padding 48/24.

## Still placeholder

- The Salesforce Partner badge in the footer is a dashed slot at 168×97.
- About has two dashed photo slots, the team shot and the portrait.
- Case 3 carries `[TO CONFIRM]` markers that are facts only Enable can supply.

## Regenerating

Edit the artboard on the canvas, then from the parent folder:

```
python3 build_static.py
```

Do not hand-edit these files; they are output. The same artboards also generate the Webflow paste set in
`../paste/`.

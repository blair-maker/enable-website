# Enable website

The Enable Digital site: fifteen static pages, generated from design artboards, deployed to Netlify.

## Layout

| | |
|---|---|
| `site/` | **The website.** Plain HTML and CSS, no build step. This is what Netlify publishes. |
| `paste/` | Webflow clipboard JSON, one file per page. Only needed if the site ever moves back to Webflow. |
| `embeds/` | The hero diagrams as standalone SVG. |
| `BUILD-GUIDE.md` | How the design system is put together, for anyone rebuilding it elsewhere. |
| `SEO.md` | Titles, meta descriptions, redirects. |
| `tokens.css` | The palette and shape tokens, as CSS custom properties. |
| `build_static.py` | Regenerates `site/` from the artboards. |
| `generate.py` | Regenerates `paste/` from the artboards. |

## Making a change

**Copy or styling:** edit the files in `site/` directly, commit, push. Netlify redeploys in under a minute.

**Structural change:** the artboards are the source. Change the design, then run `python3 build_static.py`,
which rewrites `site/`. Do not hand-edit and regenerate in the same week without checking which wins.

Either editor works. Cursor, VS Code, Claude Code: the repo does not care.

## Deploying

Netlify is connected to this repository. Pushing to `main` deploys to production. Pull requests get their
own preview URL, which is the safe way to review anything substantial.

To deploy by hand without pushing:

```
npx netlify-cli deploy --dir site --prod
```

## Before the first production deploy

- [ ] Salesforce Partner badge: replace the dashed slot in every footer
- [ ] About: two photo slots, team shot and portrait
- [ ] `site/work-marketing-cloud-next.html` still contains `[TO CONFIRM]` markers. Fill it, or unpublish
      it and remove its card from `site/work.html`
- [ ] StoreConnect page claims implementation-partner status. Confirm the listing on
      storeconnect.com/partners first
- [ ] Point the contact form at HubSpot. Enquiries belong in the CRM

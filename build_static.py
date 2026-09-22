"""Build a static HTML/CSS site from the approved artboards.

Inline styles are lifted into a single stylesheet with named classes, links are rewritten,
and responsive rules are generated for the breakpoints in BUILD-GUIDE.md.

Run: python3 build_static.py
"""
import os, re, html, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wf_transpile import Tree, norm, infer_name, quantise

SRC = ('/private/tmp/claude-501/-Users-blairrooney-Claude-Cowork-Folder/'
       '34c8abdb-267a-45a6-843f-6c1951098ca9/scratchpad/sc/project')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')

PAGES = [
    ('Home', 'index', 'Salesforce partner, Auckland and Wellington | Enable'),
    ('Waypoint', 'waypoint', 'Waypoint: continuous Salesforce improvement | Enable'),
    ('Salesforce', 'salesforce', 'Salesforce consultancy, Auckland and Wellington | Enable'),
    ('About', 'about', 'About Enable: business first, Salesforce second'),
    ('Contact', 'contact', 'Contact Enable | Salesforce partner, New Zealand'),
    ('Main', 'storeconnect', 'StoreConnect on Salesforce, NZ implementation partner | Enable'),
    ('Lumin', 'lumin', 'Lumin Sign for Salesforce, NZ implementation partner | Enable'),
    ('Gridmate', 'gridmate', 'GridMate for Salesforce, implementation partner | Enable'),
    ('Nonprofit', 'nonprofit', 'Nonprofit Cloud consultants, New Zealand | Enable'),
    ('NpspMigration', 'npsp-migration', 'NPSP to Nonprofit Cloud migration | Enable'),
    ('MarketingCloudNext', 'marketing-cloud-next', 'Marketing Cloud Next, first APAC partner | Enable'),
    ('CaseStudies', 'work', 'Our work, described honestly | Enable'),
    ('Case1', 'work-heritage', 'Case study: six systems, one supporter profile | Enable'),
    ('Case2', 'work-retirement-living', 'Case study: when every enquiry reaches one person | Enable'),
    ('Case3', 'work-marketing-cloud-next', 'Case study: first Marketing Cloud Next in APAC | Enable'),
]
SLUG = {stem: slug for stem, slug, _ in PAGES}
INLINE_OK = {'href', 'alt', 'id', 'role', 'aria-label', 'aria-hidden', 'for', 'type', 'rows', 'lang'}


def collect(stem, counts, samples):
    body = open(os.path.join(SRC, stem + '.dc.html')).read()
    body = body[body.index('<div style="width:'):body.rindex('</x-dc>')]
    t = Tree(); t.feed(body)

    def walk(n):
        if n.tag in ('__skip__', '__svg__'):
            return
        st = n.attrs.get('style')
        if st:
            k = norm(st)
            counts[k] = counts.get(k, 0) + 1
            samples.setdefault(k, (st, n.tag))
        for k in n.kids:
            walk(k)
    for k in t.root.kids:
        walk(k)
    return t


def name_classes(counts, samples):
    groups = {}
    for key, (st, tag) in samples.items():
        groups.setdefault(infer_name(st, tag), []).append(key)
    names = {}
    for base, keys in groups.items():
        for i, key in enumerate(sorted(keys, key=lambda k: -counts[k])):
            names[key] = base if i == 0 else '%s-%d' % (base, i + 1)
    return names


def render(n, names, depth=1):
    pad = '  ' * depth
    if n.tag == '__skip__':
        return ''
    if n.tag == '__svg__':
        return pad + n.raw + '\n'
    if n.tag == 'img':
        return pad + '<img src="assets/enable-logo-navy.png" alt="Enable Digital" class="logo">\n'

    tag = n.tag
    attrs = []
    st = n.attrs.get('style')
    if st:
        attrs.append('class="%s"' % names[norm(st)])
    for k, v in n.attrs.items():
        if k in INLINE_OK and v is not None:
            if k == 'href' and v.endswith('.dc.html'):
                v = SLUG.get(v[:-8], 'index') + '.html'
            attrs.append('%s="%s"' % (k, html.escape(v, quote=True)))
    a = (' ' + ' '.join(attrs)) if attrs else ''

    if tag in ('input', 'textarea'):
        return pad + '<%s%s></%s>\n' % (tag, a, tag) if tag == 'textarea' else pad + '<input%s>\n' % a

    inner = ''
    if n.text.strip() and not n.kids:
        return pad + '<%s%s>%s</%s>\n' % (tag, a, html.escape(n.text.strip()), tag)
    for k in n.kids:
        inner += render(k, names, depth + 1)
    return pad + '<%s%s>\n%s%s</%s>\n' % (tag, a, inner, pad, tag)


def stylesheet(names, samples):
    out = ["""/* Enable. Generated from the approved artboards by build_static.py.
   Tokens are in tokens.css; this file holds the layout and component classes. */

:root{--white:#fff;--mist:#F4F8FC;--tint:#E8FCF2;--ink:#0C2B4B;--slate:#47566B;--muted:#5D7290;
--hair:#DCE6F0;--edge:#C5D6E8;--green:#1EE885;--green-ink:#0A6B44;--shadow:0 8px 28px rgba(12,43,75,.10)}

*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:system-ui,-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;color:var(--ink);background:var(--white)}
img{max-width:100%;display:block}
a{color:var(--green-ink);text-decoration:none}
a:hover{color:#085434}
h1,h2,h3,h4{margin:0;letter-spacing:-.02em}
p{margin:0}
button{font-family:inherit;cursor:pointer}
input,textarea{font-family:inherit}
.page{max-width:1440px;margin:0 auto}
.logo{height:28px;width:auto;align-self:flex-start;flex:0 0 auto}
svg{max-width:100%;height:auto}
:focus-visible{outline:2px solid var(--green-ink);outline-offset:2px}
"""]
    seen = set()
    for key, nm in sorted(names.items(), key=lambda kv: kv[1]):
        if nm in seen:
            continue
        seen.add(nm)
        decl = quantise(samples[key][0]).rstrip(';')
        decl = re.sub(r'\s*;\s*', ';', decl)
        decl = re.sub(r':\s+', ':', decl)
        out.append('.%s{%s}' % (nm, decl))

    # ---- responsive, per BUILD-GUIDE.md ----
    tablet, mobile = [], []
    for key, nm in sorted(names.items(), key=lambda kv: kv[1]):
        st = samples[key][0]
        if re.search(r'width:\s*\d{3,}px', st) and 'max-width' not in st:
            tablet.append('.%s{width:100%%}' % nm)
        m = re.search(r'grid-template-columns:\s*repeat\((\d)', st)
        if m and int(m.group(1)) >= 3:
            tablet.append('.%s{grid-template-columns:repeat(2,minmax(0,1fr))}' % nm)
            mobile.append('.%s{grid-template-columns:1fr}' % nm)
        elif m:
            mobile.append('.%s{grid-template-columns:1fr}' % nm)
        fs = re.search(r'font-size:\s*(\d+)px', st)
        if fs and int(fs.group(1)) >= 38:
            v = int(fs.group(1))
            tablet.append('.%s{font-size:%dpx}' % (nm, max(30, round(v * .76))))
            mobile.append('.%s{font-size:%dpx}' % (nm, max(26, round(v * .60))))
        if re.search(r'padding:\s*(8[0-9]|9[0-9])px 80px', st):
            tablet.append('.%s{padding:64px 40px}' % nm)
            mobile.append('.%s{padding:48px 24px}' % nm)
        if re.search(r'padding:\s*0 80px', st):
            tablet.append('.%s{padding:56px 40px}' % nm)
            mobile.append('.%s{padding:44px 24px}' % nm)
        if re.search(r'height:\s*\d{3,}px', st) and 'section' in nm:
            tablet.append('.%s{height:auto}' % nm)
        # a flex row with a flex-shrink:0 child overflows once the viewport is narrower
        # than that child: stack every row at phone width
        if 'display: flex' in st and 'flex-direction: column' not in st:
            if 'split' in nm:
                mobile.append('.%s{flex-wrap:wrap;gap:8px}' % nm)
            else:
                mobile.append('.%s{flex-direction:column;align-items:stretch}' % nm)
        if 'flex-shrink: 0' in st:
            mobile.append('.%s{flex-shrink:1;width:auto;max-width:100%%}' % nm)

    out.append('\n@media (max-width:1100px){')
    out.append('.page{max-width:100%}')
    out.append('[class*="row"],[class*="hero"]{flex-wrap:wrap}')
    # flex children collapse without this, which crushes the hero diagram
    out.append('section>div,footer>div{min-width:0}')
    # hero: copy above diagram, never side by side once the column is too narrow
    out.append('#top{flex-direction:column!important;align-items:stretch!important;height:auto!important;gap:36px}')
    out.append('#top>*{width:100%!important;flex:0 0 auto!important}')
    # two-up heading + lead rows stack
    out.append('section>div[class*="row"]{flex-direction:column;align-items:stretch;gap:20px}')
    # the header is a row but must never wrap: logo left, one action right
    out.append('header{flex-wrap:nowrap!important;height:auto;padding:16px 40px;gap:16px}')
    out.append('header nav{gap:18px}')
    out.append('header nav a:not(:last-child){display:none}')
    out.append('\n'.join(sorted(set(tablet))))
    out.append('}')
    out.append('\n@media (max-width:760px){')
    out.append('[class*="row"],[class*="hero"]{flex-direction:column;align-items:stretch}')
    out.append('*{min-width:0}')
    out.append('header{flex-direction:row!important;align-items:center;padding:14px 24px}')
    out.append('header>a{flex-shrink:0;width:auto}')
    out.append('footer [class*="grid"]{grid-template-columns:1fr 1fr}')
    out.append('svg{min-width:0}')
    out.append('\n'.join(sorted(set(mobile))))
    out.append('}')
    return '\n'.join(out) + '\n'


def main():
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    counts, samples, trees = {}, {}, {}
    for stem, _, _ in PAGES:                       # pass 1: tally every inline style
        trees[stem] = collect(stem, counts, samples)
    names = name_classes(counts, samples)          # commonest style in each group takes the bare name

    open(os.path.join(OUT, 'styles.css'), 'w').write(stylesheet(names, samples))

    for stem, slug, title in PAGES:                # pass 2: emit the pages
        t = trees[stem]
        wrapper = t.root.kids[0]
        inner = ''.join(render(k, names, 2) for k in wrapper.kids)
        desc = ''
        doc = ('<!doctype html>\n<html lang="en-NZ">\n<head>\n'
               '<meta charset="utf-8">\n'
               '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
               '<title>%s</title>\n'
               '<link rel="stylesheet" href="styles.css">\n</head>\n<body>\n'
               '<div class="page">\n%s</div>\n</body>\n</html>\n') % (html.escape(title), inner)
        open(os.path.join(OUT, slug + '.html'), 'w').write(doc)

    logo = os.path.join(os.path.dirname(SRC), '..', 'enable-logo-navy.png')
    if os.path.exists(logo):
        shutil.copy(logo, os.path.join(OUT, 'assets', 'enable-logo-navy.png'))

    css = open(os.path.join(OUT, 'styles.css')).read()
    print('%d pages, %d classes, stylesheet %.1f KB'
          % (len(PAGES), len(set(names.values())), len(css) / 1024))
    for _, slug, _ in PAGES:
        p = os.path.join(OUT, slug + '.html')
        print('  %-32s %6.1f KB' % (slug + '.html', os.path.getsize(p) / 1024))


if __name__ == '__main__':
    main()

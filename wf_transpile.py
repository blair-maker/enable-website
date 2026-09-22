"""Transpile an approved .dc.html artboard into Webflow clipboard JSON (@webflow/XscpData).

Inline styles are deduplicated into named classes, so the paste lands as a maintainable
class system rather than two hundred anonymous selectors.
"""
import json, re, itertools
from html.parser import HTMLParser

VOID = {'img', 'br', 'hr', 'input', 'path', 'circle', 'rect', 'line', 'polygon', 'text', 'marker', 'defs'}
SKIP = {'script', 'style', 'helmet', 'x-dc', 'head', 'meta', 'title', 'link'}

TAG_TYPE = {
    'section': ('Section', 'section'), 'header': ('Block', 'header'), 'footer': ('Block', 'footer'),
    'nav': ('Block', 'nav'), 'div': ('Block', 'div'), 'span': ('Block', 'div'),
    'h1': ('Heading', 'h1'), 'h2': ('Heading', 'h2'), 'h3': ('Heading', 'h3'), 'h4': ('Heading', 'h4'),
    'p': ('Paragraph', 'p'), 'a': ('Link', 'a'), 'label': ('Block', 'div'), 'button': ('Block', 'div'),
}


# ----------------------------------------------------------------- parse
class Node:
    __slots__ = ('tag', 'attrs', 'kids', 'text', 'raw')

    def __init__(self, tag, attrs):
        self.tag, self.attrs, self.kids, self.text, self.raw = tag, dict(attrs), [], '', None


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root', {})
        self.stack = [self.root]
        self.svg_depth, self.svg_buf = 0, ''

    def handle_starttag(self, tag, attrs):
        if self.svg_depth:
            self.svg_buf += self.get_starttag_text()
            if tag == 'svg':
                self.svg_depth += 1
            return
        if tag == 'svg':
            self.svg_depth = 1
            self.svg_buf = self.get_starttag_text()
            return
        if tag in SKIP:
            self.stack.append(Node('__skip__', {}))
            return
        n = Node(tag, attrs)
        self.stack[-1].kids.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        if self.svg_depth:
            self.svg_buf += self.get_starttag_text(); return
        if tag not in SKIP:
            self.stack[-1].kids.append(Node(tag, attrs))

    def handle_endtag(self, tag):
        if self.svg_depth:
            self.svg_buf += '</%s>' % tag
            if tag == 'svg':
                self.svg_depth -= 1
                if self.svg_depth == 0:
                    n = Node('__svg__', {}); n.raw = self.svg_buf
                    self.stack[-1].kids.append(n)
            return
        if tag in VOID:
            return
        if len(self.stack) > 1:
            self.stack.pop()

    def handle_data(self, d):
        if self.svg_depth:
            self.svg_buf += d; return
        if d.strip():
            self.stack[-1].text += d


# ----------------------------------------------------------------- class naming
SPACING = ('gap', 'row-gap', 'column-gap', 'padding', 'margin', 'padding-top', 'padding-bottom',
           'padding-left', 'padding-right', 'margin-top', 'margin-bottom')


def quantise(style):
    """Snap spacing to a 4px scale so cosmetically identical styles share a class."""
    out = []
    for part in style.split(';'):
        part = part.strip()
        if not part or ':' not in part:
            continue
        prop, val = part.split(':', 1)
        prop, val = prop.strip(), val.strip()
        if prop in SPACING or prop.endswith('-gap'):
            val = re.sub(r'(\d+)px', lambda m: '%dpx' % (round(int(m.group(1)) / 4) * 4), val)
        if prop == 'line-height':
            try:
                val = '%.2f' % float(val)
            except ValueError:
                pass
        out.append('%s: %s' % (prop, val))
    return ';'.join(out)


def norm(style):
    parts = [p.strip() for p in quantise(style).split(';') if p.strip()]
    return ';'.join(sorted(parts))


def infer_name(style, tag):
    s = style
    def has(*bits): return all(b in s for b in bits)

    if 'linear-gradient(150deg, #0B5C45' in s: return 'card-gradient-teal'
    if 'linear-gradient(150deg, #0E5470' in s: return 'card-gradient-cyan'
    if 'linear-gradient(150deg, #143F6B' in s: return 'card-gradient-blue'
    if 'linear-gradient(150deg, #0C2B4B' in s: return 'card-gradient-navy'
    if 'linear-gradient(90deg, #0B5C45' in s: return 'stack-row-aiforce'
    if 'linear-gradient(90deg, #0E5470' in s: return 'stack-row-agentforce'
    if 'linear-gradient(90deg, #143F6B' in s: return 'stack-row-customer360'
    if 'linear-gradient(90deg, #0C2B4B' in s: return 'stack-row-data360'
    if 'linear-gradient(180deg, #ffffff 0%, #E6F1FB' in s: return 'section-wash'
    if has('background: #1EE885', 'border-radius: 999px'): return 'btn-primary'
    if has('border: 1px solid #C5D6E8', 'border-radius: 999px'): return 'btn-outline'
    if has('border-radius: 999px', 'height: 4px'): return 'rule-green'
    if has('border-radius: 999px', 'background: #1EE885'): return 'num-puck'
    if has('border-radius: 3px', 'border: 1px solid #DCE6F0'): return 'tag'
    if has('border-radius: 3px', 'rgba(255,255,255,0.35)'): return 'tag-on-gradient'
    if has('border: 1px dashed #DCE6F0'): return 'badge-slot'
    if 'font-size: 58px' in s or 'font-size: 60px' in s or 'font-size: 62px' in s: return 'h-display'
    if 'font-size: 52px' in s: return 'h-display-sm'
    if 'font-size: 44px' in s: return 'h-section'
    if 'font-size: 40px' in s or 'font-size: 38px' in s: return 'h-section-sm'
    if 'font-size: 32px' in s and 'font-weight: 600' in s: return 'h-cta'
    if 'font-size: 30px' in s and 'font-weight: 600' in s: return 'h-sub'
    if 'font-size: 26px' in s and 'font-weight: 600' in s: return 'h-card-lg'
    if 'font-size: 24px' in s and 'font-weight: 600' in s:
        return 'h-card-on-gradient' if 'color: #ffffff' in s else 'h-card'
    if 'font-size: 21px' in s and 'font-weight: 600' in s: return 'h-item'
    if 'font-size: 19px' in s and 'font-weight: 600' in s: return 'h-item-sm'
    if 'font-size: 19px' in s: return 'body-lg'
    if 'font-size: 18px' in s and 'line-height: 1.7' in s: return 'body-lead'
    if 'font-size: 17px' in s: return 'body-md'
    if 'font-size: 16px' in s and 'line-height: 1.7' in s: return 'body'
    if 'font-size: 15px' in s and 'line-height: 1.6' in s: return 'body-sm'
    if 'font-size: 14px' in s and 'color: #5D7290' in s: return 'caption'
    if 'font-size: 13px' in s and 'color: #5D7290' in s: return 'caption-sm'
    if 'box-shadow: 0 8px 28px' in s: return 'card-float'
    if has('background: #ffffff', 'border: 1px solid #DCE6F0', 'border-radius'): return 'card-bordered'
    if 'background: #E8FCF2' in s: return 'card-tint'
    if 'background: #F4F8FC' in s and 'border-radius' in s: return 'card-mist'
    if 'grid-template-columns: repeat(2' in s: return 'grid-2'
    if 'grid-template-columns: repeat(3' in s: return 'grid-3'
    if 'grid-template-columns: repeat(4' in s: return 'grid-4'
    if 'grid-template-columns: repeat(5' in s: return 'grid-5'
    if 'background: #F4F8FC' in s and 'padding: 92px 80px' in s: return 'section-mist'
    if 'padding: 92px 80px' in s or 'padding: 96px 80px' in s: return 'section'
    if 'border-bottom: 1px solid #DCE6F0' in s and 'height: 84px' in s: return 'navbar'

    if has('border-radius', 'padding') and ('background' in s or 'border:' in s): return 'card'
    if 'display: grid' in s: return 'grid'
    if 'flex-direction: column' in s:
        return 'col' if re.search(r'width: \d+px', s) else 'stack'
    if 'display: flex' in s:
        if 'justify-content: space-between' in s: return 'row-split'
        if 'flex-wrap: wrap' in s: return 'row-wrap'
        return 'row'
    if re.search(r'width: \d+px', s): return 'col'
    return 'wrap'


# ----------------------------------------------------------------- emit
class Emitter:
    def __init__(self):
        self.ids = itertools.count(1)
        self.nodes, self.styles = [], []
        self.by_style, self.name_count, self.reg = {}, {}, None

    def nid(self):
        return 'n%04d' % next(self.ids)

    def cls(self, style, tag):
        key = norm(style)
        if self.reg is not None and self.reg.names is None:
            self.reg.tally(key, style, tag)
        if key in self.by_style:
            return self.by_style[key]
        if self.reg is not None and self.reg.names is not None:
            name = self.reg.names[key]
        else:
            base = infer_name(style, tag)
            self.name_count[base] = self.name_count.get(base, 0) + 1
            name = base if self.name_count[base] == 1 else '%s-%d' % (base, self.name_count[base])
        sid = 's_%s' % name
        self.styles.append({
            '_id': sid, 'fake': False, 'type': 'class', 'name': name, 'namespace': '', 'comb': '',
            'styleLess': quantise(style).rstrip(';') + ';',
            'variants': {}, 'children': [], 'createdBy': 'Enable', 'origin': None, 'selector': None,
        })
        self.by_style[key] = sid
        return sid

    def walk(self, n):
        if n.tag == '__skip__':
            return None
        if n.tag == '__svg__':
            _id = self.nid()
            self.nodes.append({'_id': _id, 'type': 'HtmlEmbed', 'tag': 'div', 'classes': [], 'children': [],
                               'data': {'embed': {'type': 'html', 'meta': {'html': n.raw}}, 'insideRTE': False}})
            return _id
        if n.tag == 'img':                                   # site logo already lives in Webflow assets
            _id = self.nid()
            self.nodes.append({'_id': _id, 'type': 'Block', 'tag': 'div',
                               'classes': [self.cls('width: 130px; height: 28px; background: #DCE6F0; '
                                                    'border-radius: 3px;', 'div')], 'children': []})
            return _id
        if n.tag in ('input', 'textarea'):
            _id = self.nid()
            t = 'FormTextarea' if n.tag == 'textarea' else 'FormTextInput'
            self.nodes.append({'_id': _id, 'type': t, 'tag': n.tag,
                               'classes': [self.cls(n.attrs.get('style', ''), n.tag)], 'children': [],
                               'data': {'attr': {'name': n.attrs.get('id', 'field'), 'type': 'text'}}})
            return _id

        etype, tag = TAG_TYPE.get(n.tag, ('Block', 'div'))
        _id = self.nid()
        node = {'_id': _id, 'type': etype, 'tag': tag,
                'classes': [self.cls(n.attrs['style'], n.tag)] if n.attrs.get('style') else [],
                'children': []}
        if etype == 'Heading':
            node['data'] = {'tag': tag}
        if etype == 'Link':
            href = n.attrs.get('href', '#')
            mode = 'external'
            if href.endswith('.dc.html'):
                href = '/' + href.replace('.dc.html', '').lower()
                if href == '/home':
                    href = '/'
                if href == '/main':
                    href = '/storeconnect'
            node['data'] = {'link': {'mode': mode, 'url': href}}
        self.nodes.append(node)

        kids = []
        if n.text.strip() and not n.kids:
            t = self.nid()
            self.nodes.append({'_id': t, 'text': True, 'v': n.text.strip()})
            kids.append(t)
        for k in n.kids:
            cid = self.walk(k)
            if cid:
                kids.append(cid)
        node['children'] = kids
        return _id

    def dump(self):
        return json.dumps({
            'type': '@webflow/XscpData',
            'payload': {'nodes': self.nodes, 'styles': self.styles, 'assets': [], 'ix1': [],
                        'ix2': {'interactions': [], 'events': [], 'actionLists': []}},
            'meta': {'unlinkedSymbolCount': 0, 'droppedLinks': 0, 'dynBindRemovedCount': 0,
                     'dynListBindRemovedCount': 0, 'paginationRemovedCount': 0,
                     'universalBindingsRemovedCount': 0},
        }, separators=(',', ':'))


class Registry:
    """Shared across every page so a class name always means the same thing."""
    def __init__(self):
        self.by_style, self.name_count, self.styles = {}, {}, []
        self.counts, self.names, self.tags = {}, None, {}

    def tally(self, key, style, tag):
        self.counts[key] = self.counts.get(key, 0) + 1
        self.tags.setdefault(key, (style, tag))

    def finalise(self):
        """Assign names by usage: the commonest style in a group takes the bare name."""
        groups = {}
        for key, (style, tag) in self.tags.items():
            groups.setdefault(infer_name(style, tag), []).append(key)
        self.names = {}
        for base, keys in groups.items():
            for i, key in enumerate(sorted(keys, key=lambda k: -self.counts[k])):
                self.names[key] = base if i == 0 else '%s-%d' % (base, i + 1)
        self.by_style, self.name_count, self.styles = {}, {}, []


def transpile(path, reg=None):
    html = open(path).read()
    body = html[html.index('<div style="width:'):html.rindex('</x-dc>')]
    t = Tree(); t.feed(body)
    e = Emitter()
    if reg is not None:
        e.reg = reg
        e.by_style, e.name_count, e.styles = reg.by_style, reg.name_count, reg.styles
    roots = [e.walk(k) for k in t.root.kids]
    roots = [r for r in roots if r]
    # the artboard's fixed-size wrapper is a canvas artefact, not page structure: unwrap it
    if len(roots) == 1:
        wrapper = next(n for n in e.nodes if n['_id'] == roots[0])
        keep = set()
        def mark(i):
            keep.add(i)
            for c in next(n for n in e.nodes if n['_id'] == i).get('children', []):
                mark(c)
        for c in wrapper['children']:
            mark(c)
        e.nodes = [n for n in e.nodes if n['_id'] in keep or n.get('text')]
        used = {c for n in e.nodes for c in n.get('children', [])}
        e.nodes = [n for n in e.nodes if not n.get('text') or n['_id'] in used]
    # ship only the classes this page actually uses, from the shared registry
    mine = {c for n in e.nodes for c in n.get('classes', [])}
    page_styles = [st for st in e.styles if st['_id'] in mine]
    all_styles, e.styles = e.styles, page_styles
    out = e.dump()
    e.styles = all_styles
    return out, len(e.nodes), len(page_styles)

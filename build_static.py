"""Build a static HTML/CSS site from the approved artboards.

Inline styles are lifted into a single stylesheet with named classes, links are rewritten,
and responsive rules are generated for the breakpoints in BUILD-GUIDE.md.

Run: python3 build_static.py
"""
import os, re, html, shutil, sys, json
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
    ('Case3', 'work-farm-focus', 'Case study: Farm Focus | Enable'),
    ('Case4', 'work-st-john', 'Case study: rapid AI delivery at Hato Hone St John | Enable'),
]
SLUG = {stem: slug for stem, slug, _ in PAGES}
DRAWER = '''<button class="agent-launch" type="button" aria-haspopup="dialog" aria-controls="agent-drawer" aria-expanded="false" data-agent-open>
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
Ask Enable</button>
<form name="enable-drawer" data-netlify="true" netlify-honeypot="company" hidden>
  <input type="hidden" name="form-name" value="enable-drawer">
  <input type="text" name="name"><input type="email" name="email"><input type="text" name="company">
  <textarea name="message"></textarea><input type="text" name="asked">
</form>
<div class="agent-scrim" data-agent-scrim hidden></div>
<aside class="agent-drawer" id="agent-drawer" role="dialog" aria-modal="true" aria-labelledby="agent-drawer-title" aria-hidden="true">
  <div class="agent-head">
    <div><div class="agent-name" id="agent-drawer-title">Ask Enable</div><div class="agent-role">Answers about this site, not a sales bot</div></div>
    <button class="agent-close" type="button" aria-label="Close" data-agent-close><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg></button>
  </div>
  <div class="agent-body" id="agent-root">
    <div class="agent-card">
      <span class="agent-mark"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0C2B4B" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/><circle cx="12" cy="12" r="3.4"/></svg></span>
      <p class="agent-grounding">Grounded in the pages on this site: Waypoint, the product pages, the case studies and the Salesforce practice. It will say when it does not know rather than guess.</p>
    </div>
    <p class="agent-msg">What are you trying to do? If you tell me the problem rather than the product, I can point you at the right page, or tell you there is not one.</p>
    <div class="agent-prompts">
      <button class="agent-prompt" type="button" data-agent-prompt>What does Waypoint actually include?</button>
      <button class="agent-prompt" type="button" data-agent-prompt>We are on NPSP. Should we move?</button>
      <button class="agent-prompt" type="button" data-agent-prompt>Can we sell online without leaving Salesforce?</button>
      <button class="agent-prompt" type="button" data-agent-prompt>What would this cost?</button>
    </div>
    <p class="agent-human">Would rather talk to a person? <a href="contact.html">Blair answers these himself</a>.</p>
  </div>
  <div class="agent-foot">
    <form class="agent-field" data-agent-form>
      <input class="agent-input" type="text" aria-label="Ask a question" placeholder="Ask about Waypoint, StoreConnect, Data 360…" autocomplete="off">
      <button class="agent-send" type="submit" aria-label="Send"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
    </form>
    <p class="agent-disclaimer">An AI, so check anything that matters. Conversations are not recorded.</p>
  </div>
</aside>
<script>
(function(){
  var d=document.getElementById('agent-drawer'), sc=document.querySelector('[data-agent-scrim]'),
      op=document.querySelector('[data-agent-open]'), fm=document.querySelector('[data-agent-form]'), last=null;
  if(!d) return;
  function open(){ last=document.activeElement; d.setAttribute('data-open',''); sc.hidden=false;
    requestAnimationFrame(function(){ sc.setAttribute('data-open',''); });
    d.setAttribute('aria-hidden','false'); op.setAttribute('aria-expanded','true');
    var i=d.querySelector('.agent-input'); if(i) i.focus(); }
  function close(){ d.removeAttribute('data-open'); sc.removeAttribute('data-open');
    d.setAttribute('aria-hidden','true'); op.setAttribute('aria-expanded','false');
    setTimeout(function(){ sc.hidden=true; },280); if(last) last.focus(); }
  var loaded=false;
  function boot(){ if(loaded) return; loaded=true;
    var sc2=document.createElement('script'); sc2.src='__AGENTJS__'; sc2.defer=true; document.body.appendChild(sc2); }
  op.addEventListener('click',function(){ boot(); open(); });
  sc.addEventListener('click',close);
  d.querySelector('[data-agent-close]').addEventListener('click',close);
  document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&d.hasAttribute('data-open')) close(); });
  d.addEventListener('keydown',function(e){                 // keep tab inside the drawer
    if(e.key!=='Tab') return;
    var f=d.querySelectorAll('button,input:not([disabled]),a[href],textarea,select');
    if(!f.length) return; var first=f[0], lastEl=f[f.length-1];
    if(e.shiftKey&&document.activeElement===first){ e.preventDefault(); lastEl.focus(); }
    else if(!e.shiftKey&&document.activeElement===lastEl){ e.preventDefault(); first.focus(); }
  });
  [].forEach.call(d.querySelectorAll('[data-agent-prompt]'),function(b){
    b.addEventListener('click',function(){ var i=d.querySelector('.agent-input');
      i.value=b.textContent.trim(); i.focus();
      d.dispatchEvent(new CustomEvent('agent:ask',{detail:{text:i.value},bubbles:true})); });
  });
  if(fm) fm.addEventListener('submit',function(e){ e.preventDefault();
    var i=d.querySelector('.agent-input'); if(!i.value.trim()) return;
    d.dispatchEvent(new CustomEvent('agent:ask',{detail:{text:i.value.trim()},bubbles:true})); });
  // hand-off point: an agent listens for agent:ask and renders into #agent-root
  window.EnableAgent={open:open,close:close,root:document.getElementById('agent-root'),
                      el:d,on:function(fn){ d.addEventListener('agent:ask',function(e){ fn(e.detail.text); }); }};
})();
(function(){                                   // Products dropdown
  var g = document.querySelector('[data-nav-group]');
  if(!g) return;
  var t = g.querySelector('.nav-trigger'), shut;
  var fine = window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  function open(){ clearTimeout(shut); g.setAttribute('data-open',''); t.setAttribute('aria-expanded','true'); }
  function close(){ g.removeAttribute('data-open'); t.setAttribute('aria-expanded','false'); }
  t.addEventListener('click', function(){ g.hasAttribute('data-open') ? close() : open(); });
  if(fine){                                    // pointer users expect hover, with a forgiving exit
    g.addEventListener('mouseenter', open);
    g.addEventListener('mouseleave', function(){ shut = setTimeout(close, 160); });
  }
  // deliberately not opening on focus: tabbing past the nav should not pop a menu.
  // Enter and Space already reach the button's click handler.
  g.addEventListener('focusout', function(e){
    if(!g.contains(e.relatedTarget)) close();
  });
  document.addEventListener('click', function(e){ if(!g.contains(e.target)) close(); });
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' && g.hasAttribute('data-open')){ close(); t.focus(); }
  });
})();
</script>
'''

AGENT_JS = r'''
/* Enable answer engine. Retrieval over this site's own pages, built at deploy time.
   No model, no backend: it finds the passage that actually answers and cites the page. */
(function(){
  var INDEX = __INDEX__;
  var STOP = {the:1,a:1,an:1,and:1,or:1,of:1,to:1,in:1,on:1,for:1,with:1,is:1,are:1,was:1,be:1,do:1,does:1,
    we:1,you:1,i:1,it:1,that:1,this:1,what:1,how:1,can:1,should:1,our:1,your:1,my:1,at:1,as:1,by:1,from:1,
    have:1,has:1,will:1,would:1,if:1,about:1,me:1,us:1,they:1,there:1,their:1,but:1,not:1,so:1,any:1};

  function toks(str){
    return (str||'').toLowerCase().replace(/[^a-z0-9\s]/g,' ').split(/\s+/)
      .filter(function(w){ return w && w.length>2 && !STOP[w]; })
      .map(function(w){ return w.replace(/(ies)$/,'y').replace(/(es|s)$/,''); });
  }

  var DF = {}, N = INDEX.length;
  INDEX.forEach(function(e){
    var seen = {};
    toks(e.h+' '+e.x).forEach(function(w){ if(!seen[w]){ seen[w]=1; DF[w]=(DF[w]||0)+1; } });
  });
  function idf(w){ return Math.log(1 + N/(1+(DF[w]||0))); }

  function search(q){
    var qt = toks(q); if(!qt.length) return [];
    return INDEX.map(function(e){
      var h = toks(e.h), x = toks(e.x), ttl = toks(e.t + ' ' + e.p), sc = 0, hit = 0;
      qt.forEach(function(w){
        var inT = ttl.indexOf(w)>=0 ? 1 : 0;
        var inH = h.indexOf(w)>=0 ? 1 : 0;
        var n = 0; for(var i=0;i<x.length;i++) if(x[i]===w) n++;
        if(inT || inH || n){
          hit++;
          // square the idf so a distinctive word like "waypoint" outweighs "actually"
          sc += Math.pow(idf(w), 2) * (inT*4 + inH*3 + Math.min(n,3));
        }
      });
      // answering half the question is worth less than half as much
      return {e:e, s:sc * Math.pow(hit/qt.length, 2)};
    }).filter(function(r){ return r.s > 0; })
      .sort(function(a,b){ return b.s-a.s; }).slice(0,3);
  }

  function snippet(text, q){
    var qt = toks(q);
    var sents = text.split(/(?<=[.!?])\s+/);
    var best = sents[0], bestScore = -1;
    sents.forEach(function(sn){
      var t = toks(sn), sc = 0;
      qt.forEach(function(w){ if(t.indexOf(w)>=0) sc++; });
      if(sc > bestScore){ bestScore = sc; best = sn; }
    });
    var i = sents.indexOf(best);
    return sents.slice(i, i+2).join(' ').trim();
  }

  function el(tag, cls, txt){ var n=document.createElement(tag); if(cls) n.className=cls; if(txt) n.textContent=txt; return n; }

  var STAR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
    + '<path d="M12 2l1.9 6.1L20 10l-6.1 1.9L12 18l-1.9-6.1L4 10l6.1-1.9z"/></svg>';

  function thinking(root){
    var box = el('div','agent-think');
    var stars = el('span','agent-stars'); stars.innerHTML = STAR+STAR+STAR;
    var label = el('span',null,'Reading the site');
    box.appendChild(stars); box.appendChild(label); root.appendChild(box);
    root.scrollTop = root.scrollHeight;
    var lines = ['Reading the site','Finding the passage','Checking what it says'], i = 0;
    var t = setInterval(function(){ i++; if(i<lines.length) label.textContent = lines[i]; }, 620);
    return function(){ clearInterval(t); box.remove(); };
  }

  function followUp(root, asked){
    if(root.querySelector('.agent-followup')) return;
    var box = el('div','agent-followup');
    box.appendChild(el('p',null,'Did that answer it? If you would rather talk it through, leave your details '
      + 'and Blair will come back to you. He replies to everything.'));
    var f = document.createElement('form');
    f.style.cssText = 'display:flex;flex-direction:column;gap:12px';
    [['name','Your name','text'],['email','Email','email']].forEach(function(spec){
      var w = el('div','agent-f-field');
      var l = el('label',null,spec[1]); l.setAttribute('for','af-'+spec[0]);
      var inp = document.createElement('input');
      inp.id='af-'+spec[0]; inp.name=spec[0]; inp.type=spec[2]; inp.required=true; inp.autocomplete=spec[0];
      w.appendChild(l); w.appendChild(inp); f.appendChild(w);
    });
    var w3 = el('div','agent-f-field');
    var l3 = el('label',null,'What are you trying to do?'); l3.setAttribute('for','af-message');
    var ta = document.createElement('textarea'); ta.id='af-message'; ta.name='message'; ta.value = asked || '';
    w3.appendChild(l3); w3.appendChild(ta); f.appendChild(w3);
    var send = el('button','agent-f-send','Send it to Blair'); send.type='submit'; f.appendChild(send);
    var no = el('button','agent-f-no','No thanks, just browsing'); no.type='button';
    no.addEventListener('click', function(){ box.remove(); }); f.appendChild(no);

    f.addEventListener('submit', function(e){
      e.preventDefault();
      // f.name is the form's own name attribute, not the input - go through elements
      var data = new URLSearchParams({ 'form-name':'enable-drawer', name:f.elements.name.value,
                                       email:f.elements.email.value, message:f.elements.message.value,
                                       asked:asked||'' });
      send.disabled = true; send.textContent = 'Sending…';
      fetch('/', {method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded'}, body:data.toString()})
        .then(function(){ box.innerHTML='';
          box.appendChild(el('p',null,'That is with Blair. He replies to everything, usually the same working day.')); })
        .catch(function(){ box.innerHTML='';
          var pEl=el('p',null,'That did not send. Email blair@enabledigital.co and it will get there.');
          box.appendChild(pEl); });
    });
    box.appendChild(f); root.appendChild(box); root.scrollTop = root.scrollHeight;
  }

  function respond(q){
    var root = document.getElementById('agent-root');
    var intro = root.querySelector('.agent-prompts'); if(intro) intro.remove();
    var card = root.querySelector('.agent-card'); if(card) card.remove();
    var msg = root.querySelector('.agent-msg'); if(msg) msg.remove();

    root.appendChild(el('p','agent-you', q));
    var i0 = document.querySelector('.agent-input'); if(i0) i0.value = '';
    var done = thinking(root);
    var hits = search(q);
    // a considered pause: the answer is ready instantly, but arriving instantly reads as a lookup
    setTimeout(function(){ done(); paint(q, hits, root); }, 900 + Math.min(hits.length,3) * 220);
  }

  function paint(q, hits, root){
    if(!hits.length || hits[0].s < 2.5){
      var miss = el('div','agent-answer');
      miss.appendChild(el('p','agent-msg',
        'I cannot find that on this site, and I would rather say so than guess. Blair will know.'));
      var a = el('a','agent-cite','Ask him directly'); a.href='contact.html';
      miss.appendChild(a); root.appendChild(miss);
    } else {
      hits.slice(0,2).forEach(function(hit){
        var box = el('div','agent-answer');
        box.appendChild(el('div','agent-answer-h', hit.e.h));
        box.appendChild(el('p','agent-msg', snippet(hit.e.x, q)));
        var a = el('a','agent-cite', 'Read it on ' + hit.e.t.split('|')[0].split(':')[0].trim());
        a.href = hit.e.p + '.html';
        a.target = '_blank'; a.rel = 'noopener';   // keep the drawer alive behind the page they opened
        a.addEventListener('click', function(){ setTimeout(function(){ followUp(root, q); }, 1200); });
        box.appendChild(a);
        root.appendChild(box);
      });
    }
    root.scrollTop = root.scrollHeight;
  }

  if(window.EnableAgent) window.EnableAgent.on(respond);
  window.EnableAgent.answer = respond;
})();
'''

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
        src = n.attrs.get('src', '')
        alt = html.escape(n.attrs.get('alt', ''), quote=True)
        for blob, fname, w, h in [('c7e26ded6e55f89e6455c7367dd1089b', 'client-heritage.svg', 60, 49),
                                  ('c3e8dc2293d25390284df6aa749d6a11', 'client-realliving.svg', 270, 65),
                                  ('280dbb6c7d3cb0003ea400be530dc064', 'client-farmfocus.png', 2000, 860),
                                  ('ac44c2678b1924fe010da0da783e6cb3', 'client-stjohn.png', 70, 76),
                                  ('8d66061b576bc2104feb2af562bb134e', 'logo-gridmate.svg', 182, 38),
                                  ('1735550ab6564ff2f04f1d10e52b11e3', 'logo-lumin.svg', 126, 28),
                                  ('4c6351deefdaaf2f3f56f4676f9c543d', 'logo-storeconnect.jpg', 1085, 184)]:
            if blob in src:
                cls = 'logo-product'
                st = n.attrs.get('style', '')
                m2 = re.search(r'height:\s*(\d+)px', st)
                px = m2.group(1) if m2 else '28'
                return pad + ('<img src="assets/%s" alt="%s" class="%s" style="height:%spx" '
                              'width="%d" height="%d">\n') % (fname, alt, cls, px, w, h)
        own = names.get(norm(n.attrs['style'])) if n.attrs.get('style') else None
        for blob, fname, w, h in [('056670e8f10d448082d96732476903e2', 'stack-hero.webp', 2000, 1125),
                                  ('7a25399c69e4ec438ce149534ac4e0ba', 'nonprofit-one-person.webp', 1920, 1150),
                                  ('573dbbaf76c7353c0dba42041738d9b8', 'stack-cards.webp', 1900, 470),
                                  ('f804320afea9631b2b0476d9c0716114', 'hnz-identity-resolution.webp', 2000, 1000)]:
            if blob in src:
                # keep the artboard's own sizing class: it carries max-width and flex behaviour
                cls = (own + ' figure') if own else 'figure'
                return pad + ('<img src="assets/%s" alt="%s" class="%s" width="%d" height="%d" '
                              'fetchpriority="high">\n') % (fname, alt, cls, w, h)
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


PRODUCTS = [('lumin', 'Lumin', 'Agreements signed and filed without leaving Salesforce'),
            ('gridmate', 'GridMate', 'Spreadsheet-speed editing, and RevenueMate for quoting'),
            ('storeconnect', 'StoreConnect', 'Storefront and point of sale, natively on Salesforce')]


def products_menu(inner, slug):
    """The Products nav item pointed at lumin.html, which picked one product arbitrarily.
    Swap it for a group the visitor chooses from. The trigger keeps whatever class the
    original anchor carried, so it stays typographically identical to its neighbours."""
    m = re.search(r'<a class="([^"]+)" href="lumin\.html">Products</a>', inner)
    if not m:
        return inner
    cls = m.group(1)
    items = []
    for s_, name, blurb in PRODUCTS:
        cur = ' aria-current="page"' if s_ == slug else ''
        items.append('<a class="nav-item" role="menuitem" href="%s.html"%s>'
                     '<span class="nav-item-t">%s</span>'
                     '<span class="nav-item-d">%s</span></a>' % (s_, cur, name, blurb))
    open_ = ' data-on' if slug in {s_ for s_, _, _ in PRODUCTS} else ''
    group = ('<div class="nav-group"%s data-nav-group>'
             '<button class="%s nav-trigger" type="button" aria-expanded="false" '
             'aria-haspopup="true" aria-controls="nav-products">Products'
             '<svg width="10" height="7" viewBox="0 0 10 7" aria-hidden="true">'
             '<path d="M1 1.5L5 5.5L9 1.5" fill="none" stroke="currentColor" '
             'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
             '</button>'
             '<div class="nav-menu" id="nav-products" role="menu">%s</div>'
             '</div>') % (open_, cls, ''.join(items))
    return inner.replace(m.group(0), group, 1)


def build_index(bodies, slugs):
    """Pull heading + prose pairs out of the rendered pages, so the drawer can answer
    from what the site actually says rather than from anything invented."""
    import html as _h
    entries = []
    for slug, (inner, title) in bodies.items():
        # headings and paragraphs in document order
        # <p(?:\s...)?> not <p[^>]*>: the nav chevron's <path> matched the loose form and
        # swallowed the whole menu into the index
        toks = re.findall(r'<(h1|h2|h3)[^>]*>(.*?)</\1>|<p(?:\s[^>]*)?>(.*?)</p>', inner, re.S)
        heading, buf = title, []

        def flush():
            text = ' '.join(buf).strip()
            if len(text) > 80:
                entries.append({'p': slug, 't': title, 'h': heading, 'x': text[:520]})

        for h_tag, h_txt, p_txt in toks:
            if h_tag:
                flush(); buf = []
                heading = _h.unescape(re.sub(r'<[^>]+>', '', h_txt)).strip()
            elif p_txt:
                t = _h.unescape(re.sub(r'<[^>]+>', ' ', p_txt))
                t = re.sub(r'\s+', ' ', t).strip()
                if t:
                    buf.append(t)
        flush()
    return entries


def stylesheet(names, samples, used=None):
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
.page{width:100%}
.logo{height:28px;width:auto;align-self:flex-start;flex:0 0 auto}
.figure{height:auto;max-width:100%}
.logo-product{width:auto;align-self:flex-start;flex:0 0 auto;max-width:100%}
/* ---- Agent drawer ---- */
.agent-launch{position:fixed;right:24px;bottom:24px;z-index:60;display:flex;align-items:center;gap:10px;
 background:var(--green);color:var(--ink);border:none;border-radius:999px;padding:14px 22px;font-size:15px;
 font-weight:600;box-shadow:0 8px 28px rgba(12,43,75,.18);cursor:pointer}
.agent-launch:hover{box-shadow:0 10px 32px rgba(12,43,75,.24)}
.agent-scrim{position:fixed;inset:0;z-index:70;background:rgba(12,43,75,.28);opacity:0;visibility:hidden;
 transition:opacity .25s ease,visibility .25s ease}
.agent-scrim[data-open]{opacity:1;visibility:visible}
.agent-drawer{position:fixed;top:0;right:0;bottom:0;z-index:80;width:440px;max-width:100vw;background:#fff;
 display:flex;flex-direction:column;box-shadow:-8px 0 40px rgba(12,43,75,.16);
 transform:translateX(100%);transition:transform .28s cubic-bezier(.32,.72,0,1)}
.agent-drawer[data-open]{transform:translateX(0)}
.agent-head{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;padding:20px 22px;
 border-bottom:1px solid var(--hair)}
.agent-name{font-size:17px;font-weight:600;color:var(--ink)}
.agent-role{font-size:13px;color:var(--muted);margin-top:2px}
.agent-close{background:none;border:none;padding:8px;margin:-8px;cursor:pointer;color:var(--muted);line-height:0}
.agent-close:hover{color:var(--ink)}
.agent-body{flex:1;overflow-y:auto;padding:22px;display:flex;flex-direction:column;gap:18px}
.agent-card{background:var(--tint);border-radius:14px;padding:20px;display:flex;gap:14px;align-items:flex-start}
.agent-mark{width:40px;height:40px;flex:0 0 auto;border-radius:10px;background:var(--green);
 display:flex;align-items:center;justify-content:center}
.agent-grounding{font-size:13.5px;line-height:1.55;color:var(--ink)}
.agent-msg{font-size:15px;line-height:1.65;color:var(--slate)}
.agent-prompts{display:flex;flex-direction:column;gap:8px}
.agent-prompt{text-align:left;background:#fff;border:1px solid var(--hair);border-radius:3px;padding:11px 13px;
 font-size:14px;color:var(--ink);cursor:pointer;font-family:inherit}
.agent-prompt:hover{border-color:var(--edge);background:var(--mist)}
.agent-human{font-size:13.5px;color:var(--muted);line-height:1.55}
.agent-foot{border-top:1px solid var(--hair);padding:14px 22px 16px}
.agent-field{display:flex;align-items:center;gap:8px;border:1px solid var(--hair);border-radius:10px;
 background:var(--mist);padding:4px 4px 4px 14px}
.agent-input{flex:1;border:none;background:none;padding:11px 0;font-size:15px;color:var(--ink);outline:none}
.agent-send{border:none;background:var(--green);color:var(--ink);border-radius:8px;width:36px;height:36px;
 display:flex;align-items:center;justify-content:center;cursor:pointer;flex:0 0 auto}
.nav-group{position:relative;display:inline-flex}
.nav-trigger{background:none;border:none;padding:0;margin:0;font:inherit;color:inherit;
 cursor:pointer;display:inline-flex;align-items:center;gap:6px;line-height:inherit}
.nav-trigger svg{transition:transform .18s ease;opacity:.6;flex-shrink:0}
.nav-group[data-open] .nav-trigger svg{transform:rotate(180deg);opacity:1}
.nav-group[data-on] .nav-trigger{color:var(--ink)}
.nav-menu{position:absolute;top:100%;left:50%;transform:translate(-50%,6px);margin-top:14px;
 min-width:330px;background:#fff;border:1px solid var(--hair);border-radius:14px;padding:8px;
 box-shadow:var(--shadow);display:flex;flex-direction:column;gap:2px;z-index:60;
 opacity:0;visibility:hidden;pointer-events:none;transition:opacity .16s ease,transform .16s ease,visibility .16s}
.nav-group[data-open] .nav-menu{opacity:1;visibility:visible;pointer-events:auto;transform:translate(-50%,0)}
.nav-menu::before{content:"";position:absolute;left:0;right:0;top:-14px;height:14px}
.nav-item{display:flex;flex-direction:column;gap:2px;padding:11px 14px;border-radius:9px;
 text-decoration:none;transition:background .12s ease}
.nav-item:hover,.nav-item:focus-visible{background:var(--mist);outline:none}
.nav-item[aria-current="page"]{background:var(--tint)}
.nav-item-t{font-size:15px;font-weight:600;color:var(--ink);letter-spacing:-.01em}
.nav-item-d{font-size:13px;line-height:1.45;color:var(--muted)}
@media (prefers-reduced-motion:reduce){.nav-menu,.nav-trigger svg{transition:none}}
.agent-think{display:flex;align-items:center;gap:10px;color:var(--muted);font-size:14px}
.agent-stars{display:inline-flex;gap:3px;color:var(--green)}
.agent-stars svg{animation:agent-tw 1.4s ease-in-out infinite}
.agent-stars svg:nth-child(2){animation-delay:.2s}
.agent-stars svg:nth-child(3){animation-delay:.4s}
@keyframes agent-tw{0%,100%{opacity:.25;transform:scale(.8)}50%{opacity:1;transform:scale(1.1)}}
.agent-followup{background:var(--mist);border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:12px}
.agent-followup p{font-size:14px;line-height:1.6;color:var(--slate)}
.agent-followup label{font-size:12.5px;font-weight:600;color:var(--ink)}
.agent-f-field{display:flex;flex-direction:column;gap:5px}
.agent-followup input,.agent-followup textarea{border:1px solid var(--hair);border-radius:8px;padding:10px 12px;
 font-size:14px;font-family:inherit;color:var(--ink);background:#fff}
.agent-followup textarea{resize:vertical;min-height:64px}
.agent-f-send{background:var(--green);color:var(--ink);border:none;border-radius:999px;padding:12px 22px;
 font-size:14px;font-weight:600;cursor:pointer;align-self:flex-start;font-family:inherit}
.agent-f-no{background:none;border:none;color:var(--muted);font-size:13px;cursor:pointer;text-decoration:underline;
 padding:0;align-self:flex-start;font-family:inherit}
@media (prefers-reduced-motion:reduce){.agent-stars svg{animation:none;opacity:.7}}
.agent-you{align-self:flex-end;max-width:85%;background:var(--ink);color:#fff;font-size:14.5px;line-height:1.5;
 padding:11px 14px;border-radius:12px 12px 3px 12px;margin:0}
.agent-answer{border-left:2px solid var(--green);padding-left:14px;display:flex;flex-direction:column;gap:7px}
.agent-answer-h{font-size:13px;font-weight:600;color:var(--ink)}
.agent-cite{font-size:13px;font-weight:600;color:var(--green-ink);text-decoration:underline;align-self:flex-start}
.agent-disclaimer{font-size:11.5px;line-height:1.5;color:var(--muted);margin-top:10px}
@media (max-width:560px){.agent-drawer{width:100vw}.agent-launch{right:16px;bottom:16px}}
@media (prefers-reduced-motion:reduce){.agent-drawer,.agent-scrim{transition:none}}

svg{max-width:100%;height:auto}
:focus-visible{outline:2px solid var(--green-ink);outline-offset:2px}
"""]
    seen = set()
    for key, nm in sorted(names.items(), key=lambda kv: kv[1]):
        if nm in seen or (used is not None and nm not in used):
            continue
        seen.add(nm)
        decl = quantise(samples[key][0]).rstrip(';')
        decl = re.sub(r'\s*;\s*', ';', decl)
        decl = re.sub(r':\s+', ':', decl)
        # 80px gutters become "80px, or half the overflow past 1280", so bands go
        # edge to edge on a wide monitor while the text stays a readable measure
        decl = re.sub(r'(padding:\s*[^;]*?)\b80px\b',
                      r'\1max(80px, calc((100% - 1280px) / 2))', decl)
        out.append('.%s{%s}' % (nm, decl))

    # ---- responsive, per BUILD-GUIDE.md ----
    tablet, mobile = [], []
    for key, nm in sorted(names.items(), key=lambda kv: kv[1]):
        if used is not None and nm not in used:
            continue
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
    out.append('.nav-group{display:none}')
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
    import hashlib, glob as _glob
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    counts, samples, trees = {}, {}, {}
    for stem, _, _ in PAGES:                       # pass 1: tally every inline style
        trees[stem] = collect(stem, counts, samples)
    names = name_classes(counts, samples)          # commonest style in each group takes the bare name

    # pass 2: render the pages, and note which classes they actually use
    bodies, used = {}, set()
    for stem, slug, title in PAGES:
        wrapper = trees[stem].root.kids[0]
        inner = ''.join(render(k, names, 2) for k in wrapper.kids)
        inner = products_menu(inner, slug)
        bodies[slug] = (inner, title)
        for attr in re.findall(r'class="([^"]+)"', inner):
            used.update(attr.split())      # multi-class attrs, or rules get pruned

    css = stylesheet(names, samples, used)
    digest = hashlib.sha256(css.encode()).hexdigest()[:10]
    cssname = 'styles.%s.css' % digest
    for old in _glob.glob(os.path.join(OUT, 'styles*.css')):
        os.remove(old)                             # a stale stylesheet is worse than none:
    open(os.path.join(OUT, cssname), 'w').write(css)   # class names shift between builds

    entries = build_index(bodies, None)
    agent_js = AGENT_JS.replace('__INDEX__', json.dumps(entries, separators=(',', ':')))
    jsdigest = hashlib.sha256(agent_js.encode()).hexdigest()[:10]
    jsname = 'agent.%s.js' % jsdigest
    for old in _glob.glob(os.path.join(OUT, 'agent.*.js')):
        os.remove(old)
    keep = {slug + '.html' for _, slug, _ in PAGES}
    for old in _glob.glob(os.path.join(OUT, '*.html')):
        if os.path.basename(old) not in keep:
            os.remove(old)          # a renamed slug must not leave the old page behind
    open(os.path.join(OUT, jsname), 'w').write(agent_js)

    for slug, (inner, title) in bodies.items():
        doc = ('<!doctype html>\n<html lang="en-NZ">\n<head>\n'
               '<meta charset="utf-8">\n'
               '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
               '<title>%s</title>\n'
               '<link rel="stylesheet" href="%s">\n</head>\n<body>\n'
               '<div class="page">\n%s</div>\n' + DRAWER.replace('__AGENTJS__', jsname)
               + '</body>\n</html>\n') % (html.escape(title), cssname, inner)
        open(os.path.join(OUT, slug + '.html'), 'w').write(doc)

    logo = os.path.join(os.path.dirname(SRC), '..', 'enable-logo-navy.png')
    if os.path.exists(logo):
        shutil.copy(logo, os.path.join(OUT, 'assets', 'enable-logo-navy.png'))

    print('answer index: %d passages, %s %.1f KB' % (len(entries), jsname, len(agent_js) / 1024))
    print('%d pages, %d classes used (of %d defined), %s %.1f KB'
          % (len(PAGES), len(used & set(names.values())), len(set(names.values())), cssname, len(css) / 1024))


if __name__ == '__main__':
    main()

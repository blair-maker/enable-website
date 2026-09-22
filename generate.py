"""Regenerate every Webflow paste file from the approved artboards. Run: python3 generate.py"""
import json, os, sys, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wf_transpile import transpile, Registry

SRC = ('/private/tmp/claude-501/-Users-blairrooney-Claude-Cowork-Folder/'
       '34c8abdb-267a-45a6-843f-6c1951098ca9/scratchpad/sc/project')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paste')

PAGES = [
    ('Home', '01-home', '/'),
    ('Waypoint', '02-waypoint', '/waypoint'),
    ('Salesforce', '03-salesforce', '/salesforce'),
    ('About', '04-about', '/about'),
    ('Contact', '05-contact', '/contact'),
    ('Main', '06-storeconnect', '/storeconnect'),
    ('Lumin', '07-lumin', '/lumin'),
    ('Gridmate', '08-gridmate', '/gridmate'),
    ('Nonprofit', '09-nonprofit', '/nonprofit'),
    ('NpspMigration', '10-npsp-migration', '/nonprofit/npsp-migration'),
    ('MarketingCloudNext', '11-marketing-cloud-next', '/marketing-cloud-next'),
    ('CaseStudies', '12-work', '/work'),
    ('Case1', '13-work-heritage', '/work/heritage-unified-profile'),
    ('Case2', '14-work-retirement-living', '/work/retirement-living-routing'),
    ('Case3', '15-work-marketing-cloud-next', '/work/first-marketing-cloud-next-apac'),
]

if __name__ == '__main__':
    for f in glob.glob(os.path.join(OUT, '[0-9]*.json')):
        os.remove(f)
    reg = Registry()
    for stem, _, _ in PAGES:                       # pass 1: tally style usage
        transpile(os.path.join(SRC, stem + '.dc.html'), reg)
    reg.finalise()                                 # commonest style in each group takes the bare name
    rows, bad_total = [], 0
    for stem, out, url in PAGES:                   # pass 2: emit
        js, n, st = transpile(os.path.join(SRC, stem + '.dc.html'), reg)
        open(os.path.join(OUT, out + '.json'), 'w').write(js)
        p = json.loads(js)['payload']
        ids = {x['_id'] for x in p['nodes']}
        sids = {s['_id'] for s in p['styles']}
        bad = [c for x in p['nodes'] for c in x.get('children', []) if c not in ids]
        bad += [c for x in p['nodes'] for c in x.get('classes', []) if c not in sids]
        bad_total += len(bad)
        rows.append((out, url, n, st, sum(1 for x in p['nodes'] if x.get('type') == 'HtmlEmbed'),
                     len(bad), round(len(js) / 1024, 1)))
    print('%-32s %-38s %5s %6s %5s %4s %6s' % ('file', 'url', 'nodes', 'styles', 'embed', 'bad', 'KB'))
    for r in rows:
        print('%-32s %-38s %5d %6d %5d %4d %6s' % r)
    use = collections.Counter()
    for f in sorted(glob.glob(os.path.join(OUT, '[0-9]*.json'))):
        p = json.load(open(f))['payload']
        nm = {s['_id']: s['name'] for s in p['styles']}
        for x in p['nodes']:
            if not x.get('text'):
                for c in x.get('classes', []):
                    use[nm.get(c, c)] += 1
    open(os.path.join(OUT, 'CLASSES.txt'), 'w').write(
        '\n'.join('%-28s %d' % (k, v) for k, v in use.most_common()))
    print('\n%d pages, %d unique classes, %d dangling refs' % (len(rows), len(use), bad_total))

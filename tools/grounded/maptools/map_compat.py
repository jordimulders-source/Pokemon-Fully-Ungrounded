"""Fully Ungrounded: overgangslaag voor verdwenen kaarten (PLAN_HOENN_ERUIT.md, stap 4 en 5).

Schrijft twee bestanden, allebei gegenereerd (niet met de hand bewerken):

1. include/constants/map_compat.h (ingevoegd via constants/maps.h, dus in alle C-bestanden en scripts): voor elke
   MAP_*, LAYOUT_*, HEAL_LOCATION_* en LOCALID_* die de code nog noemt maar die niet meer bestaat een vervangende
   waarde.
   - MAP_*: een EIGEN waarde in een groep die niet bestaat (groep 0x40 + de oude groep, oud kaartnummer). Zo blijven
     switches met meerdere oude kaarten geldig (geen dubbele case-waarden) en is een test op zo'n kaart nooit waar.
   - LAYOUT_*: 0x4000 + oude index; HEAL_LOCATION_*: 0x80 + oude index; LOCALID_*: 0xF0 (komt op geen kaart voor).
   Code die zo'n waarde als index gebruikt (gMapGroups[MAP_GROUP(x)], gMapLayouts[LAYOUT_X - 1],
   gHealLocations[...]) leest buiten de tabel: dat is code voor verdwenen kaarten en hoort bij stap 7.
2. data/scripts/map_compat_stubs.inc (ingevoegd in data/event_scripts.s): een stub voor elk label uit een
   verdwenen kaartscript dat elders nog gebruikt wordt (C-code, algemene scripts). Tekst -> lege tekst, script ->
   `end`, beweging -> `step_end`, data -> een nul-word.

Beide lijsten krimpen vanzelf als de code per systeem wordt opgeruimd (stap 7); leeg = weg ermee.
De oude nummering en de oude scripts komen uit git (commit BASE).
Gebruik: python3 tools/grounded/maptools/map_compat.py (na elke kaart- of scriptwijziging).
"""
import json, os, re, subprocess

BASE = 'a64c32e28d'  # laatste commit met de volledige Hoenn-wereld
OUT = 'include/constants/map_compat.h'
STUBS = 'data/scripts/map_compat_stubs.inc'
CACHE = 'build/map_compat_base.json'
SCAN = ['src', 'include', 'data', 'asm', 'test']
SKIP = {OUT, STUBS, 'include/constants/map_groups.h', 'include/constants/layouts.h',
        'include/constants/heal_locations.h', 'include/constants/map_event_ids.h', 'src/data/debug_zone_warps.h',
        'src/data/map_group_count.h', 'src/data/heal_locations.h'}
EXT = ('.c', '.h', '.s', '.inc', '.json', '.party', '.txt')
LABEL = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)::?')


def git(path):
    return subprocess.run(['git', 'show', '%s:%s' % (BASE, path)], capture_output=True, check=True, text=True).stdout


def git_ls(path):
    out = subprocess.run(['git', 'ls-tree', '-r', '--name-only', BASE, path], capture_output=True, check=True,
                         text=True).stdout
    return out.split()


def stub_kind(block):
    """Soort stub voor een label, uit de regels erna (tot het volgende label)."""
    lines = [l.split('@')[0].strip() for l in block]
    lines = [l for l in lines if l]
    if not lines:
        return 'script'
    if lines[0].startswith('.string'):
        return 'text'
    if 'step_end' in lines:
        return 'movement'
    if lines[0].startswith(('.2byte', '.byte', '.4byte', '.align', 'pokemartlistend')):
        return 'data'
    return 'script'


def read_base():
    """Oude kaarten, layouts, heal locations, local ids en scriptlabels (met soort) uit BASE."""
    groups = json.loads(git('data/maps/map_groups.json'))
    maps, localids, labels = {}, set(), {}
    for gi, g in enumerate(groups['group_order']):
        for mi, name in enumerate(groups[g]):
            d = json.loads(git('data/maps/%s/map.json' % name))
            maps[d['id']] = (gi, mi)
            for o in d.get('object_events') or []:
                if o.get('local_id'):
                    localids.add(o['local_id'])
    for p in git_ls('data/maps'):
        if not p.endswith(('/scripts.inc', '/text.inc')):
            continue
        lines = git(p).split('\n')
        starts = [(i, LABEL.match(l).group(1)) for i, l in enumerate(lines) if LABEL.match(l)]
        for k, (i, lab) in enumerate(starts):
            end = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
            labels[lab] = stub_kind(lines[i + 1:end])
    lay = json.loads(git('data/layouts/layouts.json'))['layouts']
    layouts = {l['id']: i + 1 for i, l in enumerate(lay) if l and 'id' in l}
    heal = [h['id'] for h in json.loads(git('src/data/heal_locations.json'))['heal_locations']]
    heals = {h: i + 1 for i, h in enumerate(heal)}
    return {'maps': maps, 'layouts': layouts, 'heals': heals, 'localids': sorted(localids), 'labels': labels}


def current():
    groups = json.load(open('data/maps/map_groups.json'))
    maps, localids = set(), set()
    for g in groups['group_order']:
        for name in groups[g]:
            d = json.load(open('data/maps/%s/map.json' % name))
            maps.add(d['id'])
            for o in d.get('object_events') or []:
                if o.get('local_id'):
                    localids.add(o['local_id'])
    lays = {l['id'] for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l and 'id' in l}
    heals = {h['id'] for h in json.load(open('src/data/heal_locations.json'))['heal_locations']}
    return maps, lays, heals, localids


def scan():
    """Alle woorden in de bronbestanden, en alle labels die nu nog gedefinieerd worden."""
    words, defined = set(), set()
    pat = re.compile(r'\b[A-Za-z_][A-Za-z0-9_]*\b')
    for top in SCAN:
        for root, _dirs, files in os.walk(top):
            for f in files:
                p = os.path.join(root, f)
                if p in SKIP or not f.endswith(EXT):
                    continue
                try:
                    t = open(p, errors='ignore').read()
                except OSError:
                    continue
                if p.startswith('include/') and f.endswith('.h') and p != 'include/constants/maps.h':
                    # headers met alleen extern-declaraties (strings.h, event_scripts.h) maken geen stub nodig,
                    # maar constanten erin wel: neem alleen MAP_/LAYOUT_/HEAL_/LOCALID_-woorden mee
                    words.update(w for w in pat.findall(t) if w.startswith(('MAP_', 'LAYOUT_', 'HEAL_LOCATION_',
                                                                            'LOCALID_')))
                else:
                    words.update(pat.findall(t))
                    # labels die met ## in een macro worden samengesteld (battle_tower.c): het voorvoegsel telt
                    words.update('PREFIX:' + x for x in re.findall(r'\b([A-Za-z_][A-Za-z0-9_]*_)##', t))
                if f.endswith(('.inc', '.s')):
                    for l in t.split('\n'):
                        m = LABEL.match(l)
                        if m:
                            defined.add(m.group(1))
    return words, defined


def main():
    if os.path.exists(CACHE):
        base = json.load(open(CACHE))
    else:
        base = read_base()
        os.makedirs('build', exist_ok=True)
        json.dump(base, open(CACHE, 'w'))
    cur_maps, cur_lays, cur_heals, cur_ids = current()
    words, defined = scan()
    gone_maps = sorted(m for m in words if m in base['maps'] and m not in cur_maps)
    gone_lays = sorted(l for l in words if l in base['layouts'] and l not in cur_lays)
    gone_heals = sorted(h for h in words if h in base['heals'] and h not in cur_heals)
    gone_ids = sorted(i for i in words if i in set(base['localids']) and i not in cur_ids)
    prefixes = tuple(w[len('PREFIX:'):] for w in words if w.startswith('PREFIX:'))
    stubs = sorted(l for l in base['labels'] if (l in words or (prefixes and l.startswith(prefixes)))
                   and l not in defined)

    lines = [
        '#ifndef GUARD_CONSTANTS_MAP_COMPAT_H',
        '#define GUARD_CONSTANTS_MAP_COMPAT_H',
        '',
        '// Gegenereerd door tools/grounded/maptools/map_compat.py, niet met de hand bewerken.',
        '// Fully Ungrounded: verdwenen Hoenn-kaarten die de code nog noemt. Elke kaart heeft een eigen waarde in een',
        '// groep die niet bestaat (0x40 + oude groep), dus een test erop is nooit waar. Opruimen per systeem',
        '// (PLAN_HOENN_ERUIT.md, stap 7) laat deze lijst krimpen tot hij leeg is en weg kan.',
        '// %d kaarten, %d layouts, %d heal locations, %d local ids.' % (len(gone_maps), len(gone_lays),
                                                                       len(gone_heals), len(gone_ids)),
        '',
    ]
    # als enum (zoals map_groups.h): preproc maakt er in scripts symbolen van, zodat `.ifdef` in de map-macro werkt
    for title, items, fmt in [('kaarten', gone_maps, lambda x: '(%d | (0x%X << 8))' % (base['maps'][x][1],
                                                                                       0x40 + base['maps'][x][0])),
                              ('layouts', gone_lays, lambda x: '0x%X' % (0x4000 + base['layouts'][x])),
                              ('heal locations', gone_heals, lambda x: '0x%X' % (0x80 + base['heals'][x])),
                              ('local ids', gone_ids, lambda x: '0xF0')]:
        if items:
            lines += ['// ' + title, 'enum {']
            lines += ['    %s = %s,' % (x, fmt(x)) for x in items]
            lines += ['};', '']
    lines += ['', '#endif // GUARD_CONSTANTS_MAP_COMPAT_H', '']
    text = '\n'.join(lines)
    if not os.path.exists(OUT) or open(OUT).read() != text:
        open(OUT, 'w').write(text)

    body = {'text': '\t.string "$"', 'script': '\tend', 'movement': '\tstep_end', 'data': '\t.align 2\n\t.4byte 0'}
    s = ['@ Gegenereerd door tools/grounded/maptools/map_compat.py, niet met de hand bewerken.',
         '@ Fully Ungrounded: stubs voor labels uit verdwenen kaartscripts die elders nog gebruikt worden (%d).'
         % len(stubs), '@ Opruimen per systeem (PLAN_HOENN_ERUIT.md, stap 7) laat deze lijst krimpen.', '']
    for lab in stubs:
        kind = base['labels'][lab]
        if kind == 'data':
            s += ['\t.align 2', '%s::' % lab, '\t.4byte 0', '']
        else:
            s += ['%s::' % lab, body[kind], '']
    text = '\n'.join(s)
    if not os.path.exists(STUBS) or open(STUBS).read() != text:
        open(STUBS, 'w').write(text)
    print('map_compat: %d kaarten, %d layouts, %d heal locations, %d local ids, %d label-stubs'
          % (len(gone_maps), len(gone_lays), len(gone_heals), len(gone_ids), len(stubs)))


if __name__ == '__main__':
    main()

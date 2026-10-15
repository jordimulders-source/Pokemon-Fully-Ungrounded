#!/usr/bin/env python3
"""Kleurvarianten ("skins") voor Pokémon.

Leest alle normale paletten uit src/data/graphics/pokemon.h, schrijft per palet een
variants.pal (6 x 16 kleuren, variant 1..6) naast normal.pal en genereert
src/data/pokemon/variant_palettes.h (koppeling normaal palet -> varianten,
opgenomen in src/pokemon.c na data/graphics/pokemon.h).

Alleen soorten met een recept in recipes.py krijgen varianten (kleurgroepen per
soort: ramps.py; herkleuren: colorlib.py).

Gebruik: python3 tools/grounded/variants/variants.py
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
GFX_H = os.path.join(ROOT, 'src/data/graphics/pokemon.h')
OUT_H = os.path.join(ROOT, 'src/data/pokemon/variant_palettes.h')
NUM_VARIANTS = 6  # naast normaal
EDGE_FRAC = 0.3   # donkerste index van een groep, >= 30% tegen de achtergrond: omlijning
EDGE_MAX_L = 0.5  # die wordt nooit lichter dan het origineel (+0,05) en nooit lichter dan dit (OKLab)

PAL_RE = re.compile(r'const u16 (gMonPalette_\w+)\[\] = INCBIN_U16\("([^"]+)\.gbapal"\);')
IF_RE = re.compile(r'^\s*#\s*(if|ifdef|ifndef|elif|else|endif)\b(.*)$')


def read_pal(path):
    with open(path) as f:
        lines = f.read().split()
    n = int(lines[2])
    vals = list(map(int, lines[3:3 + n * 3]))
    return [tuple(vals[i:i + 3]) for i in range(0, n * 3, 3)]


def write_pal(path, colors):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n%d\n' % len(colors))
        for c in colors:
            f.write('%d %d %d\n' % c)


def gba(c):
    """Rond af op 5 bits per kanaal (zoals de GBA het toont)."""
    return tuple(min(255, (int(round(v)) >> 3) << 3) for v in c)


def collect_palettes():
    """[(symbool, pad zonder extensie, [condities])] uit pokemon.h, alleen de niet-GBA-stijl."""
    out, stack = [], []  # stack: lijst van (conditie, in_else)
    for line in open(GFX_H):
        m = IF_RE.match(line)
        if m:
            kind, rest = m.group(1), m.group(2).split('//')[0].strip()
            if kind == 'if':
                stack.append([rest, False])
            elif kind == 'ifdef':
                stack.append(['defined(%s)' % rest, False])
            elif kind == 'ifndef':
                stack.append(['!defined(%s)' % rest, False])
            elif kind == 'elif':
                stack[-1] = ['!(%s) && (%s)' % (stack[-1][0], rest), False]
            elif kind == 'else':
                stack[-1][1] = True
            else:
                stack.pop()
            continue
        m = PAL_RE.search(line)
        if not m:
            continue
        sym, path = m.groups()
        conds, skip = [], False
        for cond, in_else in stack:
            if 'P_GBA_STYLE_SPECIES_GFX' in cond:
                # alleen de tak met de moderne sprites
                if (cond.startswith('!') and in_else) or (not cond.startswith('!') and not in_else):
                    skip = True
                continue
            conds.append('!(%s)' % cond if in_else else '(%s)' % cond)
        if not skip:
            out.append((sym, path, conds))
    return out


def recipe_variants(folder, colors):
    """6 varianten volgens recipes.py, of None als de soort nog geen recept heeft."""
    from recipes import LINES
    from colorlib import recolor
    from ramps import stats, edge_fraction
    from colorlib import to_oklch, from_oklch, gba
    for line in LINES.values():
        ramps = line['species'].get(folder)
        if ramps is None:
            continue
        count, _ = stats(os.path.join(ROOT, 'graphics/pokemon', folder))
        edge = edge_fraction(os.path.join(ROOT, 'graphics/pokemon', folder))
        out = []
        for var in line['variants']:
            pal = list(colors)
            for part, idxs in ramps.items():
                spec = var.get('%s:%s' % (folder, part), var.get(part))
                if spec is None:
                    continue
                target, opts = (spec, {}) if isinstance(spec, str) else spec
                base = max(idxs, key=lambda i: count[i])
                darkest = min(idxs, key=lambda i: to_oklch(colors[i])[0])
                for i, c in recolor(colors, idxs, base, target, lscale=opts.get('l', 1.0),
                                    cscale=opts.get('c')).items():
                    # Gekleurde omlijning (pixels langs de rand) blijft donker genoeg,
                    # anders lost een lichte variant op in de achtergrond.
                    if i == darkest and edge[i] >= EDGE_FRAC:
                        L, C, h = to_oklch(c)
                        cap = min(to_oklch(colors[i])[0] + 0.05, EDGE_MAX_L)
                        if L > cap:
                            c = gba(from_oklch(cap, C, h))
                    pal[i] = c
            out.append(pal)
        return out
    return None


def main():
    entries = []
    for sym, path, conds in collect_palettes():
        pal = os.path.join(ROOT, path + '.pal')
        if not os.path.exists(pal):
            print('geen .pal:', path, file=sys.stderr)
            continue
        # Alcremie heeft al 63 kleurvormen
        if '/question_mark/' in path or '/egg/' in path or '/alcremie/' in path:
            continue
        folder = os.path.relpath(os.path.dirname(pal), os.path.join(ROOT, 'graphics/pokemon'))
        colors = read_pal(pal)[:16]
        colors += [(0, 0, 0)] * (16 - len(colors))
        base = os.path.basename(path)
        vfile = os.path.join(os.path.dirname(path), base.replace('normal', 'variants') if 'normal' in base else base + '_variants')
        variants = recipe_variants(folder, colors) if base in ('normal', 'normalf') else None
        if variants is None:
            if os.path.exists(os.path.join(ROOT, vfile + '.pal')):
                os.remove(os.path.join(ROOT, vfile + '.pal'))
            continue
        base = base.replace('normal', 'variants') if 'normal' in base else base + '_variants'
        vpath = os.path.join(os.path.dirname(path), base)
        write_pal(os.path.join(ROOT, vpath + '.pal'), [c for v in variants for c in v])
        entries.append((sym, vpath, conds))

    lines = ['// Gegenereerd door tools/grounded/variants/variants.py; niet met de hand bewerken.', '']
    for sym, vpath, conds in entries:
        if conds:
            lines.append('#if ' + ' && '.join(conds))
        lines.append('static const u16 sVariants_%s[] = INCBIN_U16("%s.gbapal");' % (sym[len('gMonPalette_'):], vpath))
        if conds:
            lines.append('#endif')
    lines += ['', 'const struct VariantPalettes gVariantPalettes[] =', '{']
    for sym, vpath, conds in entries:
        if conds:
            lines.append('#if ' + ' && '.join(conds))
        lines.append('    {%s, sVariants_%s},' % (sym, sym[len('gMonPalette_'):]))
        if conds:
            lines.append('#endif')
    lines += ['    {NULL, NULL},', '};', '']
    with open(OUT_H, 'w') as f:
        f.write('\n'.join(lines))
    print('%d paletten' % len(entries))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Kleurvarianten ("skins") voor Pokémon.

Leest alle normale paletten uit src/data/graphics/pokemon.h, schrijft per palet een
variants.pal (6 x 16 kleuren, variant 1..6) naast normal.pal en genereert
src/data/pokemon/variant_palettes.h (koppeling normaal palet -> varianten,
opgenomen in src/pokemon.c na data/graphics/pokemon.h).

Stap 1 (techniek): placeholder-recepten. De echte recepten (rolherkenning, zwart,
albino, ondersoorten, thema's) komen in stap 2 in recipes.py.

Gebruik: python3 tools/grounded/variants/variants.py [--only bulbasaur,charmander]
"""
import colorsys
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
GFX_H = os.path.join(ROOT, 'src/data/graphics/pokemon.h')
OUT_H = os.path.join(ROOT, 'src/data/pokemon/variant_palettes.h')
NUM_VARIANTS = 6  # naast normaal

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


# --- placeholder-recepten (stap 1) ------------------------------------------

def _keep(c):
    """Omlijning, wit en bijna-grijs blijven staan."""
    h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in c))
    return l < 0.12 or l > 0.93 or s < 0.08


def _hls_map(colors, fn):
    out = [colors[0]]
    for c in colors[1:]:
        if _keep(c):
            out.append(c)
            continue
        h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in c))
        h, l, s = fn(h, l, s)
        out.append(gba(v * 255 for v in colorsys.hls_to_rgb(h % 1.0, max(0, min(1, l)), max(0, min(1, s)))))
    return out


def placeholder_variants(colors):
    return [
        _hls_map(colors, lambda h, l, s: (h + 1 / 6, l, s)),
        _hls_map(colors, lambda h, l, s: (h + 1 / 3, l, s)),
        _hls_map(colors, lambda h, l, s: (h + 1 / 2, l, s)),
        _hls_map(colors, lambda h, l, s: (h - 1 / 6, l, min(1, s * 1.2))),
        _hls_map(colors, lambda h, l, s: (h, 0.12 + l * 0.35, s * 0.35)),          # zwart
        _hls_map(colors, lambda h, l, s: (h, 0.75 + l * 0.2, s * 0.15)),           # albino
    ]


def main():
    only = None
    if len(sys.argv) > 2 and sys.argv[1] == '--only':
        only = set(sys.argv[2].split(','))
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
        if only and folder.split('/')[0] not in only:
            continue
        colors = read_pal(pal)[:16]
        colors += [(0, 0, 0)] * (16 - len(colors))
        variants = placeholder_variants(colors)
        base = os.path.basename(path)
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

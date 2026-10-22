"""Controle van een nieuwe (fakemon-/regional-)sprite tegen de Hoenn-regels.

  python3 tools/concept/sprites/check.py <map> [--stage 1|2|3] [--legend]

<map> bevat anim_front.png (64x128, 2 frames) en back.png (64x64), optioneel
icon.png (32x64) en normal.pal. Uitvoer: FOUT (moet), LET OP (afwijkend van
Hoenn: bewust?) en OK, met de Hoenn-spreiding (p10..p90) erbij, plus de waarden
voor species_info (frontPicYOffset, backPicYOffset, *PicSize).
"""
import sys, os
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
import spritelib as L
import measure as M

ICON_PALS = [L.read_pal(os.path.join(L.GFX, 'icon_palettes', 'pal%d.pal' % i)) for i in range(6)]
_REF = None


def hoenn_ref():
    global _REF
    if _REF is None:
        rows = []
        for s in L.hoenn_species():
            try:
                fr, pal = L.load_front(s, 'gba'); bk, _ = L.load_back(s, 'gba')
                r = M.measure_sprite(fr, bk, pal)
                r['stage'] = s
                rows.append((s, r))
            except Exception:
                pass
        _REF = rows
    return _REF


def ref_range(key, stage=None, stagefn=None):
    v = [r[key] for s, r in hoenn_ref() if r.get(key) is not None and (stage is None or stagefn(s) == stage)]
    return np.percentile(v, 10), np.median(v), np.percentile(v, 90)


def main():
    a = sys.argv[1:]
    d = a.pop(0)
    stage = None; legend = False
    while a:
        k = a.pop(0)
        if k == '--stage': stage = int(a.pop(0))
        elif k == '--legend': legend = True
    errs, warns, oks = [], [], []
    fp = os.path.join(d, 'anim_front.png')
    im = Image.open(fp)
    if im.mode != 'P': errs.append('anim_front.png is geen geïndexeerde PNG (modus %s)' % im.mode)
    if im.size != (64, 128): errs.append('anim_front.png is %dx%d, moet 64x128 (2 frames)' % im.size)
    fa, pal = L.load_png(fp)
    if os.path.exists(os.path.join(d, 'normal.pal')):
        p2 = L.read_pal(os.path.join(d, 'normal.pal'))
        if p2[:16] != pal[:16]:
            warns.append('normal.pal wijkt af van het palet in anim_front.png (gbagfx gebruikt de PNG; houd ze gelijk)')
    if fa.max() > 15: errs.append('indexen boven 15: maximaal 16 kleuren (4bpp)')
    frames = [fa[k * 64:(k + 1) * 64] for k in range(fa.shape[0] // 64)]
    bk = None
    if os.path.exists(os.path.join(d, 'back.png')):
        bimg = Image.open(os.path.join(d, 'back.png'))
        if bimg.size != (64, 64): errs.append('back.png is %dx%d, moet 64x64' % bimg.size)
        if bimg.mode != 'P': errs.append('back.png is niet geïndexeerd')
        bk, bpal = L.load_png(os.path.join(d, 'back.png')); bk = bk[:64]
        if bpal[:16] != pal[:16]:
            errs.append('back.png heeft een ander palet dan anim_front.png (moeten exact gelijk zijn)')
    else:
        warns.append('geen back.png')
    # GBA-kleuren
    for i, c in enumerate(pal):
        if any(v != int(round(v / 255 * 31)) * 255 // 31 for v in c):
            warns.append('kleur %d #%02x%02x%02x is niet exact 15-bit (wordt afgerond; gebruik ramp.gba())' % (i, *c)); break
    allidx = frames + ([bk] if bk is not None else [])
    used = sorted(set(int(v) for x in allidx for v in np.unique(x)) - {0})
    lums = {k: L.lum(pal[k]) for k in used}
    darkest = min(used, key=lambda k: lums[k])
    if lums[darkest] > 0.10:
        errs.append('donkerste kleur #%02x%02x%02x is geen (bijna) zwart: Hoenn gebruikt #101010 of #000000' % pal[darkest])
    if darkest != 15:
        warns.append('omlijning staat op index %d; conventie (GBA-sprites) is index 15' % darkest)
    # rand van het canvas
    for k, f in enumerate(frames):
        m = f > 0
        if m[:, 0].any() or m[:, 63].any() or m[0].any():
            warns.append('frame %d raakt de linker-/rechter-/bovenrand (wordt afgekapt; laat 1px marge tenzij bewust groot)' % (k + 1))
        if m[63].any():
            warns.append('frame %d raakt de onderrand (alleen voor eindvormen/legendaries)' % (k + 1))
    r = M.measure_sprite(frames, bk, pal)
    stagefn = None
    if stage:
        st, _, _ = M.evo_stage()
        stagefn = lambda s: st(s)
    def cmp(key, label, fmt='%.3g', hard=None):
        lo, med, hi = ref_range(key, stage, stagefn) if stage else ref_range(key)
        v = r.get(key)
        if v is None: return
        txt = '%-28s %s  (Hoenn%s p10..p90: %s..%s, mediaan %s)' % (label, fmt % v, ' fase %d' % stage if stage else '', fmt % lo, fmt % hi, fmt % med)
        (oks if lo <= v <= hi else warns).append(txt)
    cmp('h', 'hoogte (px)', '%d'); cmp('w', 'breedte (px)', '%d'); cmp('area', 'oppervlak (px)', '%d')
    cmp('colors', 'kleuren gebruikt', '%d')
    cmp('edge_darkest', 'rand: aandeel zwart')
    cmp('edge_lum_tl', 'rand linksboven: helderheid')
    cmp('edge_lum_br', 'rand rechtsonder: helderheid')
    cmp('light_dx', 'licht links(-)/rechts(+)')
    cmp('light_dy', 'licht boven(-)/onder(+)')
    cmp('shadow_frac', 'aandeel schaduwtinten')
    cmp('checker_frac', 'dithering (schaakbord)')
    cmp('isolated_px', 'losse pixels', '%d')
    cmp('inner_darkest_frac', 'binnenlijnen zwart')
    cmp('frame_diff_after_shift', 'verschil frame 1-2')
    if bk is not None:
        cmp('back_area', 'back: oppervlak', '%d')
    if r['colors'] > 15: errs.append('meer dan 15 kleuren + transparant')
    if len(frames) < 2: errs.append('maar 1 frame; Emerald-stijl heeft 2 (tweede = actiepose)')
    elif r.get('frame_diff', 0) == 0: errs.append('frame 2 is gelijk aan frame 1')
    if not legend and stage == 1 and r['h'] > 52: warns.append('fase 1 is groot (h %d); Hoenn-basisvormen zijn meestal 30-58 hoog' % r['h'])
    # wit en V=1-hooglicht
    import colorsys
    vmax = max(colorsys.rgb_to_hsv(*[x / 255 for x in pal[k]])[2] for k in used)
    if vmax < 0.95: warns.append('geen tint met volle helderheid (V=1); 97%% van de Hoenn-sprites heeft er een (max V=%.2f)' % vmax)
    # icoon
    ip = os.path.join(d, 'icon.png')
    if os.path.exists(ip):
        ic = Image.open(ip)
        if ic.size != (32, 64): errs.append('icon.png is %dx%d, moet 32x64 (2 frames)' % ic.size)
        icp = ic.getpalette()[:48]; icp = [tuple(icp[3 * i:3 * i + 3]) for i in range(16)]
        if icp not in ICON_PALS:
            warns.append('icon.png gebruikt geen van de 6 gedeelde icoonpaletten (graphics/pokemon/icon_palettes/pal0-5.pal)')
        ia = np.array(ic)
        b0 = L.bbox(ia[:32] > 0)
        if b0: oks.append('icoon frame 1: %dx%d, onderrand y=%d (Hoenn: ±20x20, onderrand 29)' % (b0[2] - b0[0] + 1, b0[3] - b0[1] + 1, b0[3]))
    else:
        warns.append('geen icon.png')
    # species_info-waarden
    bb = [L.bbox(f > 0) for f in frames]
    ceil8 = lambda v: min(64, (v + 7) // 8 * 8)
    info = ['.frontPicSize = MON_COORDS_SIZE(%d, %d),' % (ceil8(max(b[2] for b in bb) - min(b[0] for b in bb) + 1), ceil8(max(b[3] for b in bb) - min(b[1] for b in bb) + 1)),
            '.frontPicYOffset = %d,' % (63 - bb[0][3])]
    if bk is not None:
        b = L.bbox(bk > 0)
        info += ['.backPicSize = MON_COORDS_SIZE(%d, %d),' % (ceil8(b[2] - b[0] + 1), ceil8(b[3] - b[1] + 1)), '.backPicYOffset = %d,' % (63 - b[3])]
    for t, lst in (('FOUT', errs), ('LET OP', warns), ('OK', oks)):
        for x in lst:
            print('%-7s %s' % (t, x))
    print('\nspecies_info:\n  ' + '\n  '.join(info))
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())

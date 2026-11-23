"""Gemeenschappelijke knip-en-plakfuncties voor de Gnometrotter-hybrides.

Per onderdeel: masker in de basis (kleurklasse binnen een kader, naden en
kleine gaten erbij), masker in de donor (idem), donorkader -> basiskader
schalen (NEAREST), alleen binnen het basismasker plakken. Valt een
bemonsterde donorpixel buiten het donormasker (donoromlijning, baard die
ervoor hangt), dan wordt de dichtstbijzijnde donorpixel binnen het masker
genomen. Er wordt niets getekend: elke geplakte pixel is een donorpixel.
"""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def laad(p):
    return np.asarray(Image.open(p).convert('RGB')).astype(int)


def klasse(a, cls, breed=False):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    wit = np.all(a > 240, axis=-1)
    if cls == 'roze':
        # roze heeft b >= g; bruin hout (riem, zolen, stok) heeft b < g
        if breed:   # alles met roodzweem: vlak, glimlijnen, naden (niet het groenblauwe ijs)
            return (r > g + 6) & (r >= b - 12) & (b >= g - 3) & ~wit
        return (r - g > 28) & (r >= b - 5) & (r > 120) & (b >= g - 3)
    if cls == 'blauw':
        mx = a.max(axis=-1).clip(1)
        sat = (mx - a.min(axis=-1)) / mx
        if breed:   # verzadigd blauw (niet het grijsblauwe ijs van riem/zolen)
            return (b > r + 12) & ~wit & (sat >= 0.2)
        return (b - r > 38) & (b > 90) & (sat >= 0.22)
    raise ValueError(cls)


def kadermasker(shape, kader):
    m = np.zeros(shape[:2], bool)
    if isinstance(kader[0], (tuple, list)):
        # veelhoek: lijst van punten
        from PIL import ImageDraw
        im = Image.new('L', (shape[1], shape[0]), 0)
        ImageDraw.Draw(im).polygon([tuple(p) for p in kader], fill=1)
        return np.asarray(im).astype(bool)
    x0, y0, x1, y1 = kader
    m[y0:y1, x0:x1] = True
    return m


def zonder_omlijning(a, m, donker=60, rand=6, grijs=0.15):
    """Haal de zwarte buitenomlijning van het donoronderdeel uit het masker
    (die levert de basis); donkere naden binnenin blijven."""
    lum = a.mean(axis=-1)
    mx = a.max(axis=-1).clip(1)
    sat = (mx - a.min(axis=-1)) / mx
    buiten = ndi.binary_dilation(~m, iterations=rand)
    # zwart en grijze anti-aliaspixels van de buitenrand
    return m & ~(((lum < donker) | (sat < grijs)) & buiten)


def deelmasker(a, cls, kader, sluit=2, gat=600, uitsluit=None):
    """Onderdeel = samenhangende stukken van de brede kleurklasse binnen het
    kader die echte onderdeelkleur bevatten; daarna naden en kleine gaten dicht."""
    k = kadermasker(a.shape, kader)
    if uitsluit is not None:
        k &= ~uitsluit
    streng = klasse(a, cls) & k
    breed = klasse(a, cls, True) & k
    lab, n = ndi.label(breed)
    if n:
        tel = ndi.sum(streng, lab, range(1, n + 1))
        m = np.isin(lab, [i + 1 for i, t in enumerate(tel) if t >= 20])
    else:
        m = breed
    if sluit:
        st = ndi.generate_binary_structure(2, 1)
        m = ndi.binary_closing(m, st, iterations=sluit) & k
    gaten = ndi.binary_fill_holes(m) & ~m
    lab, n = ndi.label(gaten)
    if n:
        maten = ndi.sum(gaten, lab, range(1, n + 1))
        for i, s in enumerate(maten, 1):
            if s <= gat:
                m |= lab == i
    m &= k
    lab, n = ndi.label(m)
    if n > 1:
        maten = ndi.sum(m, lab, range(1, n + 1))
        m = np.isin(lab, [i + 1 for i, s in enumerate(maten) if s >= 150])
    return m


def bbox(m):
    ys, xs = np.nonzero(m)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def rijranden(m, y0, y1, glad=4):
    """Linker- en rechterrand van het masker per rij (gladgestreken)."""
    L = np.full(y1 - y0, np.nan)
    R = np.full(y1 - y0, np.nan)
    for i, y in enumerate(range(y0, y1)):
        xs = np.nonzero(m[y])[0]
        if len(xs):
            L[i], R[i] = xs.min(), xs.max() + 1
    idx = np.arange(len(L))
    ok = ~np.isnan(L)
    L = np.interp(idx, idx[ok], L[ok])
    R = np.interp(idx, idx[ok], R[ok])
    if glad:
        k = np.ones(2 * glad + 1) / (2 * glad + 1)
        pad = lambda a: np.pad(a, glad, mode='edge')
        L = np.convolve(pad(L), k, 'valid')
        R = np.convolve(pad(R), k, 'valid')
    return L, R


def pingpong(t, n):
    """Spiegeltegels: 0..n-1, n-1..0, 0..n-1, ..."""
    t = np.mod(t, 2 * n)
    return np.where(t < n, t, 2 * n - 1 - t)


def plak(uit, basis_m, donor, donor_m, spiegel=False, kader_b=None, kader_d=None,
         rij=False, tegel=None):
    """Schaal het donorstuk op het basisonderdeel en plak alleen binnen basis_m.
    Verticaal: kader op kader. Horizontaal (rij=True): per rij de randen van het
    basisonderdeel op de randen van het donoronderdeel (zo valt de donorrand op
    de basisrand en wordt er geen donoromlijning of achtergrond bemonsterd)."""
    bx0, by0, bx1, by1 = kader_b or bbox(basis_m)
    dx0, dy0, dx1, dy1 = kader_d or bbox(donor_m)
    # dichtstbijzijnde donorpixel binnen het masker voor elke pixel
    _, (iy, ix) = ndi.distance_transform_edt(~donor_m, return_indices=True)
    ys, xs = np.nonzero(basis_m)
    v = (ys - by0 + 0.5) / (by1 - by0)
    sy = np.clip((dy0 + v * (dy1 - dy0)).astype(int), 0, donor.shape[0] - 1)
    if tegel:
        # vaste schaal; buiten het donorstuk gespiegeld herhaald (zelfde
        # textuur, geen uitrekken)
        tx = ((xs - bx0) / tegel).astype(int)
        ty = ((ys - by0) / tegel).astype(int)
        tx = pingpong(tx, dx1 - dx0)
        ty = pingpong(ty, dy1 - dy0)
        if spiegel:
            tx = (dx1 - dx0 - 1) - tx
        sx = dx0 + tx
        sy = dy0 + ty
    elif rij:
        bL, bR = rijranden(basis_m, by0, by1)
        dm = donor_m.copy()
        dm[:, :dx0] = False
        dm[:, dx1:] = False
        dL, dR = rijranden(dm, dy0, dy1)
        bl, br = bL[ys - by0], bR[ys - by0]
        u = (xs - bl + 0.5) / np.maximum(br - bl, 1)
        if spiegel:
            u = 1 - u
        dl = dL[np.clip(sy - dy0, 0, len(dL) - 1)]
        dr = dR[np.clip(sy - dy0, 0, len(dR) - 1)]
        sx = np.clip((dl + u * (dr - dl)).astype(int), 0, donor.shape[1] - 1)
    else:
        u = (xs - bx0 + 0.5) / (bx1 - bx0)
        if spiegel:
            u = 1 - u
        sx = np.clip((dx0 + u * (dx1 - dx0)).astype(int), 0, donor.shape[1] - 1)
    ny, nx = iy[sy, sx], ix[sy, sx]
    # buiten het donormasker: spiegelen in de dichtstbijzijnde rand
    # (de textuur loopt door, geen strepen); lukt dat niet, dan de randpixel
    ry = np.clip(2 * ny - sy, 0, donor.shape[0] - 1)
    rx = np.clip(2 * nx - sx, 0, donor.shape[1] - 1)
    ok = donor_m[ry, rx]
    ny = np.where(ok, ry, ny)
    nx = np.where(ok, rx, nx)
    uit[ys, xs] = donor[ny, nx]
    return float((~donor_m[sy, sx]).mean())


def omtrek(a):
    """Silhouet: alle niet-witte pixels, binnengaten dicht."""
    return ndi.binary_fill_holes(~(np.all(a > 235, axis=-1)))


def nietwit(a):
    return ~(np.all(a > 235, axis=-1))


def debug_maskers(a, maskers, pad):
    kleuren = [(255, 0, 0), (0, 200, 0), (0, 0, 255), (255, 160, 0),
               (200, 0, 200), (0, 200, 200), (120, 60, 0), (90, 90, 90)]
    o = a.copy().astype(float)
    for i, m in enumerate(maskers):
        c = np.array(kleuren[i % len(kleuren)])
        o[m] = o[m] * 0.4 + c * 0.6
    Image.fromarray(o.astype(np.uint8)).save(pad)


def vergelijk(paden, uit, crop=(250, 20, 780, 540), schaal=1):
    ims = [Image.open(p).convert('RGB').crop(crop) for p in paden]
    w, h = ims[0].size
    v = Image.new('RGB', (w * len(ims) + 10 * (len(ims) - 1), h), (255, 255, 255))
    for i, im in enumerate(ims):
        v.paste(im, (i * (w + 10), 0))
    if schaal != 1:
        v = v.resize((v.width * schaal, v.height * schaal), Image.NEAREST)
    v.save(uit)


def achtergrond(a):
    """Witte achtergrond = bijna-witte pixels die met de beeldrand verbonden zijn."""
    w = np.all(a > 235, axis=-1)
    lab, n = ndi.label(w)
    rand = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return np.isin(lab, list(rand))


def basismaskers(a, delen, donker=105, gat=40, minkern=10, binnennaad=0):
    """Basismaskers die de zwarte lijnen van de basis heilig houden.
    Kandidaten = brede kleurklasse zonder donkere lijnpixels; samenhangende
    vlakken (4-buren) gaan naar het onderdeel waarvan het kader het meeste
    van het vlak bevat. Donkere lijnen (omlijning, naden tussen onderdelen)
    vallen buiten elk masker en blijven dus van de basis."""
    lum = a.mean(axis=-1)
    kaders = [kadermasker(a.shape, d[2]) for d in delen]
    maskers = [np.zeros(a.shape[:2], bool) for _ in delen]
    for cls in sorted({d[1] for d in delen}):
        idx = [i for i, d in enumerate(delen) if d[1] == cls]
        kand = klasse(a, cls, True) & (lum >= donker)
        kand0 = kand
        # dunne lichte barst-/glimlijnen tussen twee stukken van dezelfde kleur
        # horen erbij (sluiten), donkere lijnen en achtergrond niet
        st = ndi.generate_binary_structure(2, 1)
        dicht = ndi.binary_closing(kand, st, iterations=3)
        bijlijn = ndi.binary_dilation(lum < donker, iterations=2)
        kand = kand | (dicht & (lum >= 170) & ~achtergrond(a) & ~bijlijn)
        streng = klasse(a, cls)
        # vlakken die via een gaatje in een zwarte lijn aan elkaar hangen
        # (schouderschijf en romp) splitsen: eerst 2 px eroderen, labelen,
        # dan elke pixel het label van het dichtstbijzijnde kernvlak geven
        kernm = ndi.binary_erosion(kand0, iterations=2)
        klab, n = ndi.label(kernm)
        dist, (iy, ix) = ndi.distance_transform_edt(~kernm, return_indices=True)
        lab = np.where(kand & (dist <= 5), klab[iy, ix], 0)
        if not n:
            continue
        overlap = np.stack([ndi.sum(kaders[i], lab, range(1, n + 1)) for i in idx])
        maat = ndi.sum(kand, lab, range(1, n + 1))
        kern = ndi.sum(streng, lab, range(1, n + 1))
        objs = ndi.find_objects(lab)
        vrij = np.ones(a.shape[:2], bool)
        for c in range(n):
            if kern[c] < minkern or kern[c] < 0.25 * maat[c] or overlap[:, c].max() == 0:
                continue
            sl = objs[c]
            comp = np.zeros(a.shape[:2], bool)
            comp[sl] = lab[sl] == c + 1
            heel = [j for j in range(len(idx)) if overlap[j, c] >= maat[c] * 0.97]
            j = int(overlap[:, c].argmax())
            if heel:
                # vlak ligt (vrijwel) helemaal in één kader: heel naar dat onderdeel
                maskers[idx[heel[0]]] |= comp
            elif overlap[j, c] >= maat[c] * 0.85:
                # vlak ligt grotendeels in één kader: ook heel naar dat onderdeel
                maskers[idx[j]] |= comp
            else:
                # vlak loopt over kaders heen: per pixel, op volgorde van DELEN
                for i in idx:
                    deel = comp & kaders[i] & vrij
                    maskers[i] |= deel
                    comp &= ~deel
        # niet ver buiten het eigen kader (bv. het gezicht naast de nek)
        for i in idx:
            maskers[i] &= ndi.binary_dilation(kaders[i], iterations=8)
        # een pixel hoort bij één onderdeel
        for i in idx:
            maskers[i] &= vrij
            vrij &= ~maskers[i]
        # losse lichte barstpixels die tegen het vlak aan liggen (vaak waar een
        # barst de zwarte lijn raakt) erbij; niet over een zwarte lijn heen
        bezet = np.zeros(a.shape[:2], bool)
        for m in maskers:
            bezet |= m
        for i in idx:
            rand = ndi.binary_dilation(maskers[i], iterations=2) & ~bezet & kaders[i]
            licht = (lum >= 150) & ~achtergrond(a) & (a.max(axis=-1) - a.min(axis=-1) < 60)
            maskers[i] |= rand & licht
        donkerpx = lum < donker
        for i in idx:
            m = maskers[i]
            # gaten: ingesloten door het onderdeel (en eventueel zwarte lijnen
            # eromheen), bv. glimlijnen, noesten/jaarringen
            r_ = m | (donkerpx & ndi.binary_dilation(m, iterations=6))
            gaten = ndi.binary_fill_holes(r_) & ~r_ & kaders[i]
            gl, gn = ndi.label(gaten)
            if gn:
                maten = ndi.sum(gaten, gl, range(1, gn + 1))
                klein = [j + 1 for j, s in enumerate(maten) if s <= gat]
                m |= np.isin(gl, klein)
            maskers[i] = m
    if binnennaad:
        maskers = binnennaden(a, maskers, donker, binnennaad)
    return maskers


def binnennaden(a, maskers, donker, r):
    """Donkere lijnen die helemaal binnen één onderdeel liggen (naden, nerf,
    jaarringen van de basis) horen bij dat onderdeel en worden vervangen.
    Donkere pixels die binnen r px iets anders zien (achtergrond, ander
    materiaal, een ander onderdeel) zijn omlijning en blijven van de basis."""
    lum = a.mean(axis=-1)
    dark = lum < donker
    alle = np.zeros(a.shape[:2], bool)
    for m in maskers:
        alle |= m
    vreemd = ~dark & ~alle
    st = ndi.generate_binary_structure(2, 2)
    bij_vreemd = ndi.binary_dilation(vreemd, st, iterations=r)
    bij = [ndi.binary_dilation(m, st, iterations=r) for m in maskers]
    uit = []
    for i, m in enumerate(maskers):
        ander = np.zeros(a.shape[:2], bool)
        for j, bj in enumerate(bij):
            if j != i:
                ander |= bj
        uit.append(m | (dark & bij[i] & ~bij_vreemd & ~ander))
    return uit

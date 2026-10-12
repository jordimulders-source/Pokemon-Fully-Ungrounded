"""Project Grounded: film-tilemaps als verschil met de vorige tilemap opslaan (v0.9.229, scheelt ±320 KB ROM).

De filmspeler (Film_Update in src/battle_transition.c) houdt de laatst uitgepakte tilemap in zijn buffer. Een tilemap
met bit 31 in mapofs is een delta: XOR met tilemap i-1. Dat mag alleen als de speler tilemap i altijd direct na i-1
uitpakt; dat volgt uit een simulatie van de seq (zelfde logica als Film_Update). Anders blijft het een keyframe.

Gebruik: python3 tools/grounded/film_delta.py [naam ...]   (zonder namen: alle films; al omgezette films worden
overgeslagen). film.py roept encode() zelf aan na het opslaan.
"""
import glob, os, struct, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR = os.path.join(ROOT, 'graphics/battle_transitions/')
DELTA = 0x80000000
BLANK = 0xFFFF


def unlz(d, o=0):
    assert d[o] == 0x10
    n = d[o + 1] | d[o + 2] << 8 | d[o + 3] << 16
    i, out = o + 4, bytearray()
    while len(out) < n:
        f = d[i]
        i += 1
        for b in range(8):
            if len(out) >= n:
                break
            if f & (0x80 >> b):
                x = d[i] << 8 | d[i + 1]
                i += 2
                disp = (x & 0xFFF) + 1
                for _ in range((x >> 12) + 3):
                    out.append(out[-disp])
            else:
                out.append(d[i])
                i += 1
    return bytes(out)


def lz(raw):
    with tempfile.TemporaryDirectory() as t:
        a = os.path.join(t, 'x.bin')
        open(a, 'wb').write(raw)
        subprocess.run([os.path.join(ROOT, 'tools/gbagfx/gbagfx'), a, a + '.lz'], check=True)
        out = open(a + '.lz', 'rb').read()
    return out + bytes((-len(out)) % 4)


def encode(name):
    p = DIR + 'film_%s_' % name
    ofs = list(struct.unpack('<%dI' % (os.path.getsize(p + 'mapofs.bin') // 4), open(p + 'mapofs.bin', 'rb').read()))
    if any(o & DELTA for o in ofs):
        return None
    blob = open(p + 'maps.bin', 'rb').read()
    maps = [unlz(blob, o) for o in ofs]
    seq = open(p + 'seq.bin', 'rb').read()
    # simulatie van Film_Update: welke tilemap staat in de buffer als tilemap m wordt uitgepakt
    before = {}
    shown, last = None, None
    for k in range(len(seq) // 8):
        m = struct.unpack_from('<H', seq, k * 8)[0]
        if m == shown:
            continue
        shown = m
        if m == BLANK:
            continue
        before.setdefault(m, set()).add(last)
        last = m
    new_blob, new_ofs = b'', []
    for i, m in enumerate(maps):
        delta = i > 0 and before.get(i) == {i - 1}
        raw = bytes(a ^ b for a, b in zip(m, maps[i - 1])) if delta else m
        new_ofs.append(len(new_blob) | (DELTA if delta else 0))
        new_blob += lz(raw)
    open(p + 'maps.bin', 'wb').write(new_blob)
    open(p + 'mapofs.bin', 'wb').write(struct.pack('<%dI' % len(new_ofs), *new_ofs))
    return len(blob), len(new_blob), sum(1 for o in new_ofs if o & DELTA), len(new_ofs)


def recompress(name):
    """Pakt alle LZ-blokken (tiles en tilemaps) uit en comprimeert ze opnieuw (na een betere gbagfx, v0.9.229)."""
    p = DIR + 'film_%s_' % name
    loads = open(p + 'loads.bin', 'rb').read()
    tiles = open(p + 'tiles.bin', 'rb').read()
    new_tiles, new_loads = b'', b''
    for k in range(len(loads) // 8):
        o, nr, fr = struct.unpack_from('<IHH', loads, k * 8)
        new_loads += struct.pack('<IHH', len(new_tiles), nr, fr)
        new_tiles += lz(unlz(tiles, o))
    ofs = struct.unpack('<%dI' % (os.path.getsize(p + 'mapofs.bin') // 4), open(p + 'mapofs.bin', 'rb').read())
    maps = open(p + 'maps.bin', 'rb').read()
    new_maps, new_ofs = b'', []
    for o in ofs:
        new_ofs.append(len(new_maps) | (o & DELTA))
        new_maps += lz(unlz(maps, o & ~DELTA))
    before = len(tiles) + len(maps)
    open(p + 'tiles.bin', 'wb').write(new_tiles)
    open(p + 'loads.bin', 'wb').write(new_loads)
    open(p + 'maps.bin', 'wb').write(new_maps)
    open(p + 'mapofs.bin', 'wb').write(struct.pack('<%dI' % len(new_ofs), *new_ofs))
    return before, len(new_tiles) + len(new_maps)


if __name__ == '__main__':
    names = sys.argv[1:] or sorted(os.path.basename(f)[5:-9] for f in glob.glob(DIR + 'film_*_maps.bin'))
    for n in names:
        r = encode(n)
        print(n, 'al omgezet' if r is None else '%d -> %d bytes, %d/%d delta' % r)

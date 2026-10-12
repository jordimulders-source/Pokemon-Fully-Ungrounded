#!/usr/bin/env python3
"""Project Grounded: een nummer 1-op-1 uit een andere GBA-game met de MP2K-engine ('Sappy') halen (v0.9.236).

Wario Land 4 en Mario Kart: Super Circuit gebruiken dezelfde muziekengine als Pokémon Emerald: de sporen (bytecode),
de voicegroup (128 instrumenten van 12 bytes) en de samples (WaveData: 16 bytes kop + 8-bit PCM) kunnen ongewijzigd
over. Dit script:
- leest het nummer uit de songtabel van de ROM, ontleedt elk spoor (tot FINE) en zet elke pointer (GOTO/PATT/REPT)
  om naar een label, zodat de bytes als assembly (`sound/songs/<naam>.s`) in onze ROM passen;
- kopieert alleen de instrumenten die het nummer gebruikt (programma's uit VOICE-commando's; keysplits en drumkits
  met hun subtabellen) naar een eigen voicegroup in hetzelfde .s-bestand;
- schrijft elke sample als .wav (sound/direct_sound_samples/rip/<game>/, grondtoon 60 + loop), zodat wav2agb hem
  exact terugbouwt; samples worden per game gedeeld (één label per ROM-adres).
Gebruik:  python3 tools/grounded/mp2k_rip.py <rom.gba> <songtabel-hex> <game> <songnummer> <MUS_CONSTANTE> ["beschrijving"]
"""
import os, re, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)

ARG1 = {0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF, 0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC8}


class Rom:
    def __init__(self, path):
        self.d = open(path, 'rb').read()

    def u32(self, o):
        return struct.unpack_from('<I', self.d, o)[0]

    def off(self, p):
        return p - 0x08000000 if 0x08000000 <= p < 0x08000000 + len(self.d) else None


def parse_track(rom, o):
    """Geeft (eind-offset, [pointer-posities], {programma: noten}).
    Zoals m4a: alleen commando's >= 0xBD worden 'running status'; wachttijden en B1-BC nemen geen argumenten over."""
    d = rom.d
    ptrs, used, prog, rs, key = [], {}, 0, None, 60
    while True:
        if o >= len(d) - 8:
            raise ValueError('spoor zonder FINE')
        b = d[o]
        if b >= 0x80:
            c = b
            o += 1
            if c >= 0xBD:
                rs = c
        else:
            if rs is None:
                raise ValueError('argument-byte 0x%02X zonder running status op 0x%X' % (b, o))
            c = rs
        if c <= 0xB0:                      # wachttijd
            continue
        if c == 0xB1:
            return o, ptrs, used
        if c in (0xB2, 0xB3):
            ptrs.append(o)
            o += 4
            if c == 0xB2 and d[o] == 0xB1:
                return o + 1, ptrs, used
            continue
        if c == 0xB4:
            continue
        if c == 0xB5:
            ptrs.append(o + 1)
            o += 5
            continue
        if c == 0xB9:
            o += 3
            continue
        if c in ARG1:
            if c == 0xBD:
                prog = d[o]
            o += 1
            continue
        if c == 0xCD:
            o += 2
            continue
        if c == 0xCE:
            if d[o] < 0x80:
                o += 1
            continue
        if c >= 0xCF:
            if d[o] < 0x80:
                key = d[o]
                o += 1
                if d[o] < 0x80:
                    o += 1
                    if d[o] < 0x80 and c != 0xCF:
                        o += 1
            used.setdefault(prog, set()).add(key)
            continue
        # onbekend commando (B6-B8, C6, C7, C9-CC): geen argument


def wav_from_wave(rom, p, path):
    """MP2K-WaveData -> 8-bit wav (rate = freq/1024, grondtoon 60, loop)."""
    o = rom.off(p)
    typ, status, freq, loop, size = struct.unpack_from('<HHIII', rom.d, o)
    pcm = bytes((x + 128) & 0xFF for x in rom.d[o + 16:o + 16 + size])
    rate = max(1, round(freq / 1024))
    fmt = struct.pack('<HHIIHH', 1, 1, rate, rate, 1, 8)
    loops = [struct.pack('<IIIIII', 0, 0, loop, size - 1, 0, 0)] if status & 0x4000 else []
    smpl = struct.pack('<IIIIIIIII', 0, 0, int(1e9 / rate), 60, 0, 0, 0, len(loops), 0) + b''.join(loops)
    body = b'fmt ' + struct.pack('<I', 16) + fmt + b'smpl' + struct.pack('<I', len(smpl)) + smpl + b'data' + \
        struct.pack('<I', len(pcm)) + pcm + (b'\0' if len(pcm) & 1 else b'')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(b'RIFF' + struct.pack('<I', 4 + len(body)) + b'WAVE' + body)
    return 16 + size


def rip(rompath, table, game, num, const, desc=''):
    rom = Rom(rompath)
    tbl = rom.off(int(table, 16))
    h = rom.off(rom.u32(tbl + num * 8))
    ntr, blocks, prio, rev = rom.d[h:h + 4]
    vg = rom.u32(h + 4)
    lab = const.lower()
    tracks, used, ranges = [], {}, []
    for t in range(ntr):
        s = rom.off(rom.u32(h + 8 + 4 * t))
        e, ptrs, u = parse_track(rom, s)
        tracks.append((s, e, ptrs))
        ranges.append((s, e))
        for k, v in u.items():
            used.setdefault(k, set()).update(v)

    def where(p):
        o = rom.off(p)
        for i, (s, e, _) in enumerate(tracks):
            if s <= o < e:
                return '%s_%d+%d' % (lab, i, o - s)
        raise ValueError('pointer 0x%X buiten de sporen' % p)

    out = ['@ Project Grounded: %s (%s, song %d), 1-op-1 uit de ROM: tools/grounded/mp2k_rip.py' % (desc or const, game, num),
           '\t.include "MPlayDef.s"', '', '\t.section .rodata', '\t.align 2', '']
    for i, (s, e, ptrs) in enumerate(tracks):
        out.append('%s_%d:' % (lab, i))
        o = s
        pset = set(ptrs)
        line = []
        while o < e:
            if o in pset:
                if line:
                    out.append('\t.byte ' + ', '.join(line))
                    line = []
                out.append('\t.4byte ' + where(rom.u32(o)))
                o += 4
                continue
            line.append('0x%02X' % rom.d[o])
            o += 1
            if len(line) == 16:
                out.append('\t.byte ' + ', '.join(line))
                line = []
        if line:
            out.append('\t.byte ' + ', '.join(line))
        out.append('')
    # voicegroup: alleen gebruikte programma's echt, de rest leeg (vierkant)
    samples = {}
    subs = {}

    def sample_label(p):
        if p not in samples:
            name = '%s_%06x' % (game, rom.off(p))
            samples[p] = name
            wav_from_wave(rom, p, 'sound/direct_sound_samples/rip/%s/%s.wav' % (game, name))
        return 'DirectSoundWaveData_' + samples[p]

    def voice_lines(base, idx, keys, prefix, depth=0):
        """Assembly voor één instrument (12 bytes); subtabellen worden apart toegevoegd."""
        e = rom.off(base) + idx * 12
        raw = rom.d[e:e + 12]
        t = raw[0]
        if t in (0x00, 0x08, 0x10, 0x18):
            return ['\t.byte ' + ', '.join('0x%02X' % x for x in raw[:4]), '\t.4byte ' + sample_label(rom.u32(e + 4)),
                    '\t.byte ' + ', '.join('0x%02X' % x for x in raw[8:])]
        if t in (0x03, 0x0B):          # programmeerbare golf: 16 bytes golfdata
            wp = rom.u32(e + 4)
            wl = '%s_wave_%x' % (prefix, rom.off(wp))
            subs[wl] = ['\t.byte ' + ', '.join('0x%02X' % x for x in rom.d[rom.off(wp):rom.off(wp) + 16])]
            return ['\t.byte ' + ', '.join('0x%02X' % x for x in raw[:4]), '\t.4byte ' + wl,
                    '\t.byte ' + ', '.join('0x%02X' % x for x in raw[8:])]
        if t == 0x40 and depth == 0:
            sub, split = rom.u32(e + 4), rom.u32(e + 8)
            tab = rom.d[rom.off(split):rom.off(split) + 128]
            sl = '%s_split_%x' % (prefix, rom.off(split))
            subs[sl] = ['\t.byte ' + ', '.join('0x%02X' % x for x in tab[i:i + 16]) for i in range(0, 128, 16)]
            vl = '%s_sub_%x' % (prefix, rom.off(sub))
            need = sorted(set(tab[k] for k in keys if k < 128))
            body = []
            for j in range(max(need) + 1 if need else 1):
                body += voice_lines(sub, j, {k for k in keys if tab[k] == j}, prefix, 1) if j in need else EMPTY
            subs[vl] = body
            return ['\t.byte ' + ', '.join('0x%02X' % x for x in raw[:4]), '\t.4byte ' + vl, '\t.4byte ' + sl]
        if t == 0x80 and depth == 0:
            sub = rom.u32(e + 4)
            vl = '%s_drums_%x' % (prefix, rom.off(sub))
            body = []
            for j in range(max(keys) + 1 if keys else 1):
                body += voice_lines(sub, j, {j}, prefix, 1) if j in keys else EMPTY
            subs[vl] = body
            return ['\t.byte ' + ', '.join('0x%02X' % x for x in raw[:4]), '\t.4byte ' + vl,
                    '\t.byte ' + ', '.join('0x%02X' % x for x in raw[8:])]
        # PSG (vierkant/ruis) zonder pointers: zo laten
        return ['\t.byte ' + ', '.join('0x%02X' % x for x in raw)]
    EMPTY = ['\t.byte 0x01, 0x3C, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0F, 0x00']
    vgl = lab + '_vg'
    body = []
    for p in range(max(used) + 1 if used else 1):
        body += voice_lines(vg, p, used.get(p, set()), lab) if p in used else EMPTY
    out += ['\t.align 2', vgl + ':'] + body + ['']
    for name, lines in subs.items():
        out += ['\t.align 2', name + ':'] + lines + ['']
    out += ['\t.align 2', '\t.global ' + lab, lab + ':', '\t.byte %d, %d, %d, %d' % (ntr, blocks, prio, rev), '\t.4byte ' + vgl]
    out += ['\t.4byte %s_%d' % (lab, i) for i in range(ntr)]
    open('sound/songs/%s.s' % lab, 'w').write('\n'.join(out) + '\n')
    register(lab, const, desc, game, num, samples)
    return sum(e - s for s, e, _ in tracks), samples


def register(lab, const, desc, game, num, samples):
    p = 'sound/direct_sound_data.inc'
    s = open(p).read()
    add = []
    for name in sorted(samples.values()):
        if 'DirectSoundWaveData_%s::' % name not in s:
            add += ['\t.align 2', 'DirectSoundWaveData_%s::' % name,
                    '\t.incbin "sound/direct_sound_samples/rip/%s/%s.bin"' % (game, name), '']
    if add:
        s = s.rstrip('\n') + '\n\n@ rip %s (mp2k_rip.py)\n' % game + '\n'.join(add)
        open(p, 'w').write(s.rstrip('\n') + '\n')
    sh = 'include/constants/songs.h'
    h = open(sh).read()
    if '#define %s ' % const not in h:
        n = max(int(x) for x in re.findall(r'#define MUS_\w+\s+(\d+)\s', h)) + 1
        h = h.replace('\n#define MUS_ROUTE118', '\n#define %s %d // Project Grounded: %s, 1-op-1 uit %s (song %d, tools/grounded/mp2k_rip.py)\n#define MUS_ROUTE118'
                      % (const.ljust(27), n, desc or const, game, num), 1)
        open(sh, 'w').write(h)
        st = 'sound/song_table.inc'
        t = open(st).read()
        t = t.replace('\n\t.align 2\ndummy_song_header:', '\n\tsong %s, MUSIC_PLAYER_BGM, 0\n\n\t.align 2\ndummy_song_header:' % lab, 1)
        open(st, 'w').write(t)


if __name__ == '__main__':
    a = sys.argv[1:]
    seq, smp = rip(a[0], a[1], a[2], int(a[3]), a[4], a[5] if len(a) > 5 else '')
    print('%s: %d bytes noten, %d samples' % (a[4], seq, len(smp)))

#!/usr/bin/env python3
"""Project Grounded: SNES-muziek (SPC) naar onze GBA-engine (MP2K), voor Yoshi's Island (v0.9.235).

Werkwijze: de SPC wordt in blargg's snes_spc afgespeeld (spclog, met een haak op elke DSP-schrijfactie); uit de log
komen per SNES-stem de noten (KON/KOFF), toonhoogte (pitch-register, ook bends/vibrato), instrument (SRCN) en volume.
De instrumenten zijn de originele BRR-samples uit het SPC-RAM (dezelfde bank wordt door de nummers gedeeld).
- melodische samples: wav met grondtoon (autocorrelatie, bijgestemd tot een hele noot) en de BRR-loop,
- drums (samples die op max. 3 toonhoogtes klinken): per toonhoogte een eigen drumtoets, 16 kHz, zonder resample,
- tijd: 1 tick = 1 GBA-frame (150 BPM, 24 ticks per tel), loop automatisch gevonden ([ en ] markers),
- ADSR/GAIN van de SNES omgerekend naar de MP2K-envelope (attack/decay/sustain/release per frame).

Gebruik: python3 tools/grounded/spc/spc2gba.py <map-met-spc's> [naam ...]
Vereist: g++ en de bron van game-music-emu (wordt bij de eerste keer gekloond naar build/gme)."""
import collections, hashlib, json, math, os, re, struct, subprocess, sys
import numpy as np
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spclib  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.chdir(ROOT)
BUILD = 'build/spc'
SAMPLES = 'sound/direct_sound_samples/grounded/'
VG = 'sound/voicegroups/grounded_yi.inc'
KIT = 'sound/voicegroups/drumsets/yi.inc'
KIT_BASE = 36
REL = 40          # SNES-KOFF klinkt ±8 ms uit; 40/256 per frame = ±25 ms (geen kanaalroof, geen klik)
TICK_MS = 1000 / 60

# naam: (spc-bestand, songconstante, beschrijving, -V)
SONGS = {
    'flower_garden': ('yi-07a.spc', 'MUS_GROUNDED_YI_FLOWER_GARDEN', "Flower Garden (Yoshi's Island)", 110),
    'athletic':      ('yi-13a.spc', 'MUS_GROUNDED_YI_ATHLETIC', "Athletic (Yoshi's Island)", 110),
    'overworld':     ('yi-14a.spc', 'MUS_GROUNDED_YI_OVERWORLD', "Overworld (Yoshi's Island)", 110),
    'fuzzy':         ('yi-14b.spc', 'MUS_GROUNDED_YI_FUZZY', "Overworld (Fuzzy), Touch Fuzzy Get Dizzy", 110),
    'castle':        ('yi-10.spc', 'MUS_GROUNDED_YI_CASTLE', "Castle & Fortress (Yoshi's Island)", 110),
}

# SNES-envelope: perioden (samples bij 32 kHz) per rate 0..31
RATE = [0, 2048, 1536, 1280, 1024, 768, 640, 512, 384, 320, 256, 192, 160, 128, 96, 80, 64, 48, 40, 32, 24, 20,
        16, 12, 10, 8, 6, 5, 4, 3, 2, 1]


def spclog():
    exe = os.path.join(BUILD, 'spclog')
    if os.path.exists(exe):
        return exe
    os.makedirs(BUILD, exist_ok=True)
    src = 'build/gme'
    if not os.path.exists(src):
        subprocess.run(['git', 'clone', '-q', '--depth', '1', 'https://github.com/libgme/game-music-emu.git', src],
                       check=True)
    subprocess.run(['g++', '-O2', '-w', '-DBLARGG_LITTLE_ENDIAN=1', '-I' + src + '/gme', '-o', exe,
                    'tools/grounded/spc/spclog.cpp'], check=True)
    return exe


def exp_frame(rate):
    """MP2K-factor (x/256 per frame) voor een exponentiële SNES-rate."""
    if rate <= 0:
        return 255
    steps = 32000 / RATE[rate] / 60
    return max(0, min(255, int(round(256 * (1 - 1 / 256) ** steps))))   # SNES: env *= 255/256 per stap


def envelope(adsr1, adsr2, gain):
    """(attack, decay, sustain, release) in MP2K-termen."""
    if adsr1 & 0x80:
        ar, dr, sl, sr = adsr1 & 15, (adsr1 >> 4) & 7, adsr2 >> 5, adsr2 & 31
        att = 255 if ar >= 14 else max(8, int(255 * (ar + 1) / 16))
        if sr:
            return att, exp_frame(sr), 0, REL
        return att, exp_frame(dr * 2 + 16), min(255, (sl + 1) * 32 - 1), REL
    if not gain & 0x80:
        return 255, 0, min(255, (gain & 0x7F) * 2 + 1), REL
    mode, rate = (gain >> 5) & 3, gain & 31
    if mode in (1, 2):          # lineair/exponentieel omlaag
        return 255, exp_frame(rate), 0, REL
    return 200, 0, 255, REL     # omhoog: zachte aanzet


def wav8(path, x, rate, base, loop=None):
    x = np.clip(np.round(x / max(1e-9, np.abs(x).max()) * 127), -128, 127).astype(np.int16) + 128
    data = x.astype(np.uint8).tobytes()
    fmt = struct.pack('<HHIIHH', 1, 1, rate, rate, 1, 8)
    loops = [] if loop is None else [struct.pack('<IIIIII', 0, 0, loop, len(x) - 1, 0, 0)]
    smpl = struct.pack('<IIIIIIIII', 0, 0, int(1e9 / rate), base, 0, 0, 0, len(loops), 0) + b''.join(loops)
    body = b'fmt ' + struct.pack('<I', 16) + fmt + b'smpl' + struct.pack('<I', len(smpl)) + smpl + b'data' + \
        struct.pack('<I', len(data)) + data + (b'\0' if len(data) & 1 else b'')
    open(path, 'wb').write(b'RIFF' + struct.pack('<I', 4 + len(body)) + b'WAVE' + body)


def stretch(x, factor):
    """Lengte * factor (lineaire interpolatie; band is al laag bij BRR)."""
    n = max(2, int(round(len(x) * factor)))
    return np.interp(np.arange(n) / factor, np.arange(len(x)), x)


def find_loop(ns, end):
    on = sorted((round(n['t0'] / TICK_MS), n['voice'], n['srcn'], n['pitch']) for n in ns)
    keys = set(on)
    best = None
    for P in range(int(15000 / TICK_MS), int(end * 0.75)):
        cand = [e for e in on if e[0] + P <= end - 2]
        if len(cand) < 50:
            break
        hit = sum(1 for (t, v, s, p) in cand if (t + P, v, s, p) in keys or (t + P + 1, v, s, p) in keys or
                  (t + P - 1, v, s, p) in keys)
        frac = hit / len(cand)
        # zoek de eerste A vanaf waar alles herhaalt
        if frac > 0.6 and (best is None or frac > best[0] + 0.02):
            best = (frac, P)
            if frac > 0.97:
                break
    if not best:
        return None
    P = best[1]
    ok = [((t + P, v, s, p) in keys or (t + P + 1, v, s, p) in keys or (t + P - 1, v, s, p) in keys)
          for (t, v, s, p) in on if t + P <= end - 2]
    ts = [t for (t, v, s, p) in on if t + P <= end - 2]
    bad = np.cumsum([0] + [0 if o else 1 for o in ok][::-1])[::-1]       # missers vanaf index i
    A = ts[-1]
    for i in range(len(ts)):
        if bad[i] <= 0.02 * (len(ts) - i):                               # vanaf hier herhaalt ≥98%
            A = ts[i]
            break
    return A, P


def convert(spcdir, name, bank):
    fn, const, desc, vol = SONGS[name]
    path = os.path.join(spcdir, fn)
    spc = spclib.Spc(path)
    secs = int(open(path, 'rb').read(0x100)[0xA9:0xAC].split(b'\0')[0] or 120)
    log = os.path.join(BUILD, name + '.log')
    subprocess.run([spclog(), path, str(min(400, secs * 2 + 10)), log], check=True)
    ev = spclib.read_log(log)
    ns, regs = spclib.notes(ev, spc.dsp)
    dirp = regs[spclib.DSP_DIR]
    end = round(ev[-1][0] / TICK_MS)
    lp = find_loop(ns, end)
    A, P = lp if lp else (0, round(secs * 1000 / TICK_MS))
    stop = A + P
    print('%s: %d noten, loop %.1f s + %.1f s' % (name, len(ns), A * TICK_MS / 1000, P * TICK_MS / 1000))

    # instrumenten
    by = collections.defaultdict(list)
    for n in ns:
        if round(n['t0'] / TICK_MS) < stop:
            by[n['srcn']].append(n)
    inst = {}
    for s, L in by.items():
        x, loop = spc.brr(s, dirp)
        h = hashlib.sha1(x.tobytes()).hexdigest()[:8]
        env = collections.Counter((n['adsr'], n['gain']) for n in L).most_common(1)[0][0]
        pitches = sorted(set(n['pitch'] for n in L))
        f0 = spclib.fundamental(x, loop=loop)
        if f0 is None and loop is not None:
            f0 = 32000 / (len(x) - loop)                              # loop = één periode
        drum = f0 is None or (loop is None and len(pitches) <= 3)
        if drum:
            keys = {}
            for p in pitches:
                k = (h, p)
                if k not in bank['drums']:
                    bank['drums'][k] = dict(key=KIT_BASE + len(bank['drums']), x=stretch(x, 4096 / p * 16000 / 32000),
                                            env=envelope(env[0][0], env[0][1], env[1]), name='yi_d%s_%d' % (h, p))
                keys[p] = bank['drums'][k]['key']
            inst[s] = dict(drum=True, keys=keys)
        else:
            if h not in bank['mel']:
                base = 69 + 12 * math.log2(f0 / 440)
                b = round(base)
                fac = 2 ** ((base - b) / 12)          # langer maken = lager: precies op noot b bij 32 kHz
                xs = stretch(x, fac)
                bank['mel'][h] = dict(prog=len(bank['mel']), x=xs, base=b, loop=None if loop is None else
                                      int(round(loop * fac)), env=envelope(env[0][0], env[0][1], env[1]),
                                      name='yi_m%s' % h)
            inst[s] = dict(drum=False, prog=bank['mel'][h]['prog'], base=69 + 12 * math.log2(f0 / 440))

    # MIDI: één spoor per SNES-stem
    mid = mido.MidiFile(ticks_per_beat=24)
    cond = mido.MidiTrack()
    mid.tracks.append(cond)
    cond.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(150), time=0))
    marks = [(A, '['), (stop, ']')]
    t = 0
    for at, txt in marks:
        cond.append(mido.MetaMessage('marker', text=txt, time=at - t))
        t = at
    used_echo = any(n['echo'] for n in ns)
    vmax = max(1, max((abs(int(n['vol'][0])) + abs(int(n['vol'][1]))) / 2 for n in ns))
    K = 120 / vmax                                    # luidste noot van het nummer = velocity 120
    for v in range(8):
        vn = [n for n in ns if n['voice'] == v and round(n['t0'] / TICK_MS) < stop]
        if not vn:
            continue
        evs = []
        maxdev = 0
        notes = []
        for n in vn:
            i = inst[n['srcn']]
            t0 = round(n['t0'] / TICK_MS)
            t1 = max(t0 + 1, min(stop, round(n['t1'] / TICK_MS)))
            l, r = abs(int(n['vol'][0])), abs(int(n['vol'][1]))
            velo = max(1, min(127, int(round((l + r) / 2 * K))))
            pan = 64 if l + r == 0 else max(0, min(127, int(round(64 + 63 * (r - l) / (l + r)))))
            if i['drum']:
                key, bends = i['keys'][n['pitch']], []
                prog = 127
            else:
                exact = i['base'] + 12 * math.log2(max(1, n['pitch']) / 4096)
                key = int(round(exact))
                bends = []
                for bt, bp in n['bends']:
                    dev = i['base'] + 12 * math.log2(max(1, bp) / 4096) - key
                    maxdev = max(maxdev, abs(dev))
                    bends.append((round(bt / TICK_MS), dev))
                prog = i['prog']
                if abs(exact - key) > 0.05:
                    bends.insert(0, (t0, exact - key))
            notes.append((t0, t1, key, velo, pan, prog, bends))
        rng = 2 if maxdev <= 1.9 else 12
        tr = mido.MidiTrack()
        mid.tracks.append(tr)
        evs.append((0, 0, mido.Message('control_change', control=20, value=rng)))
        evs.append((0, 0, mido.Message('control_change', control=7, value=127)))
        cur_prog = cur_pan = cur_bend = None
        for (t0, t1, key, velo, pan, prog, bends) in notes:
            if prog != cur_prog:
                evs.append((t0, 1, mido.Message('program_change', program=prog)))
                cur_prog = prog
            if pan != cur_pan:
                evs.append((t0, 1, mido.Message('control_change', control=10, value=pan)))
                cur_pan = pan
            if cur_bend not in (None, 0) and not (bends and bends[0][0] == t0):
                evs.append((t0, 2, mido.Message('pitchwheel', pitch=0)))
                cur_bend = 0
            last = None
            for bt, dev in bends:
                bt = max(t0, min(t1 - 1, bt))
                val = max(-8192, min(8191, int(round(dev / rng * 8192))))
                q = val >> 7
                if q != last and bt >= t0:
                    evs.append((bt, 2, mido.Message('pitchwheel', pitch=val)))
                    last = q
                    cur_bend = val
            evs.append((t0, 3, mido.Message('note_on', note=max(0, min(127, key)), velocity=velo)))
            evs.append((t1, 0, mido.Message('note_off', note=max(0, min(127, key)), velocity=0)))
        evs.sort(key=lambda e: (e[0], e[1]))
        t = 0
        for at, _, m in evs:
            tr.append(m.copy(time=at - t))
            t = at
    out = 'sound/songs/midi/%s.mid' % const.lower()
    mid.save(out)
    return const, desc, vol, used_echo


def write_bank(bank):
    # wav's
    for h, m in bank['mel'].items():
        wav8(SAMPLES + m['name'] + '.wav', m['x'], 32000, m['base'], m['loop'])
    for k, d in bank['drums'].items():
        wav8(SAMPLES + d['name'] + '.wav', d['x'], 16000, 60)
    # voicegroup: programma's = melodische samples, 127 = kit
    lines = ['@ Project Grounded: Yoshi\'s Island (SNES-samples uit de SPC-rip). Gegenereerd door '
             'tools/grounded/spc/spc2gba.py; 127 = drumkit yi_drumset.', 'voice_group grounded_yi']
    progs = sorted(bank['mel'].values(), key=lambda m: m['prog'])
    for p in range(128):
        if p < len(progs):
            m = progs[p]
            a, d, s, r = m['env']
            lines.append('\tvoice_directsound 60, 0, DirectSoundWaveData_%s, %d, %d, %d, %d  @ %d' %
                         (m['name'], a, d, s, r, p))
        elif p == 127:
            lines.append('\tvoice_keysplit_all voicegroup_yi_drumset  @ 127')
        else:
            lines.append('\tvoice_square_1 60, 0, 0, 2, 0, 0, 15, 0  @ %d' % p)
    open(VG, 'w').write('\n'.join(lines) + '\n')
    kit = sorted(bank['drums'].values(), key=lambda d: d['key'])
    kl = ['@ Project Grounded: Yoshi\'s Island-drums (spc2gba.py), vanaf toets %d.' % KIT_BASE,
          'voice_group yi_drumset, %d' % KIT_BASE]
    for d in kit:
        a, dd, s, r = d['env']
        kl.append('\tvoice_directsound_no_resample 60, 0, DirectSoundWaveData_%s, 255, %d, %d, %d' % (d['name'], dd, s, r))
    open(KIT, 'w').write('\n'.join(kl) + '\n')
    # direct_sound_data.inc
    p = 'sound/direct_sound_data.inc'
    s = re.sub(r'\n@ yi_samples \{.*?@ \} yi_samples\n', '\n', open(p).read(), flags=re.S)
    blk = ['', '@ yi_samples { (tools/grounded/spc/spc2gba.py)']
    for m in list(bank['mel'].values()) + list(bank['drums'].values()):
        blk += ['\t.align 2', 'DirectSoundWaveData_%s::' % m['name'], '\t.incbin "%s%s.bin"' % (SAMPLES, m['name']), '']
    blk.append('@ } yi_samples')
    open(p, 'w').write(s.rstrip('\n') + '\n' + '\n'.join(blk) + '\n')


def register(songs):
    vgi = 'sound/voice_groups.inc'
    s = open(vgi).read()
    for inc in ('sound/voicegroups/drumsets/yi.inc', 'sound/voicegroups/grounded_yi.inc'):
        if inc not in s:
            s = s.rstrip('\n') + '\n.include "%s"\n' % inc
    open(vgi, 'w').write(s)
    cfg = 'sound/songs/midi/midi.cfg'
    c = open(cfg).read()
    sh = 'include/constants/songs.h'
    h = open(sh).read()
    st = 'sound/song_table.inc'
    t = open(st).read()
    nums = [int(x) for x in re.findall(r'#define MUS_\w+\s+(\d+)\s', h)]
    for const, desc, vol, echo in songs:
        lab = const.lower()
        line = '%s.mid: -E -R%d -G_grounded_yi -V%03d' % (lab, 50 if echo else 0, vol)
        c = re.sub(r'^%s\.mid:.*$' % lab, line, c, flags=re.M) if re.search(r'^%s\.mid:' % lab, c, re.M) else \
            c.rstrip('\n') + '\n' + line + '\n'
        if '#define %s ' % const not in h:
            n = max(nums) + 1
            nums.append(n)
            anchor = '\n#define MUS_ROUTE118'
            h = h.replace(anchor, '\n#define %s %d // Project Grounded: %s, SPC-rip (tools/grounded/spc/spc2gba.py)%s'
                          % (const.ljust(27), n, desc, anchor), 1)
            t = t.replace('\n\t.align 2\ndummy_song_header:', '\n\tsong %s, MUSIC_PLAYER_BGM, 0\n\n\t.align 2\ndummy_song_header:'
                          % lab, 1)
    open(cfg, 'w').write(c)
    open(sh, 'w').write(h)
    open(st, 'w').write(t)


def main():
    spcdir = sys.argv[1]
    names = sys.argv[2:] or list(SONGS)
    os.makedirs(BUILD, exist_ok=True)
    bank = dict(mel={}, drums={})
    songs = [convert(spcdir, n, bank) for n in names]
    write_bank(bank)
    register(songs)
    print('%d melodische samples, %d drumtoetsen' % (len(bank['mel']), len(bank['drums'])))


if __name__ == '__main__':
    main()

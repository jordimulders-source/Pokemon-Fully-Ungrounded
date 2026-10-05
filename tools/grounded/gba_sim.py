#!/usr/bin/env python3
"""Project Grounded: eenvoudige offline-weergave van de DirectSound-sporen van een nummer zoals m4a ze speelt
(sample op toonhoogte = samplerate x 2^((noot - label)/12), lineaire interpolatie, envelope per frame (attack/decay/
sustain/release als in m4a), drumkits via voice_keysplit_all, no_resample = vaste snelheid, mix op 21.024 Hz).
PSG-stemmen, keysplit-tabellen, pitch bend en de m4a-galm worden niet nagebootst: bedoeld voor klank-/spectrum-
controles per spoor (gym_remixes.py: kermis_meter 'klinkt als ...') en offline vergelijkingen, niet als preview.

Gebruik als module: render(mid, vg_text, kit_texts, tracks=None, t0=0, t1=None) -> (signaal float, 21024)."""
import math, os, re, struct, wave
import numpy as np
import mido

MIX = 21024
FPS = 59.7275
_SAMPLES = {}
_LABELS = None


def _labels():
    global _LABELS
    if _LABELS is None:
        txt = open('sound/direct_sound_data.inc').read()
        _LABELS = {m.group(1): m.group(2) for m in
                   re.finditer(r'DirectSoundWaveData_(\w+)::\s*\n\s*\.incbin "([^"]+)\.bin"', txt)}
    return _LABELS


def sample(name):
    """(signaal -1..1, samplerate, label-toets, loop (begin, eind) of None)."""
    if name not in _SAMPLES:
        path = _labels()[name] + '.wav'
        w = wave.open(path)
        a = (np.frombuffer(w.readframes(w.getnframes()), np.uint8).astype(float) - 128) / 128
        d = open(path, 'rb').read()
        key, loop = 60, None
        i = d.find(b'smpl')
        if i >= 0:
            sm = struct.unpack('<9I', d[i + 8:i + 44])
            key = sm[3]
            if sm[7]:
                l = struct.unpack('<6I', d[i + 44:i + 68])
                loop = (l[2], l[3] + 1)
        _SAMPLES[name] = (a, w.getframerate(), key, loop)
    return _SAMPLES[name]


def voices(text):
    """voice-regels uit een voicegroup-/drumkittekst (zonder voice_group)."""
    return [l.strip() for l in text.split('\n') if l.strip().startswith('voice_') and not l.strip().startswith('voice_group')]


def parse(line):
    """-> dict(kind, key, sample, a, d, s, r, fixed) of None (PSG/keysplit: niet nagebootst)."""
    m = re.match(r'voice_directsound(_no_resample|_alt)?\s+(\d+),\s*(\d+),\s*DirectSoundWaveData_(\w+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)', line)
    if not m:
        return None
    return dict(fixed=m.group(1) == '_no_resample', key=int(m.group(2)), sample=m.group(4),
                a=int(m.group(5)), d=int(m.group(6)), s=int(m.group(7)), r=int(m.group(8)))


def envelope(n_on, v, total):
    """Envelope per frame (m4a): attack +a tot 255, decay x d/256 tot sustain, na de note-off x r/256."""
    env, e, phase = [], 0.0, 'a' if v['a'] < 255 else 'd'
    e = 255.0 if phase == 'd' else 0.0
    for f in range(total):
        if f >= n_on:
            e = e * v['r'] / 256.0
        elif phase == 'a':
            e += v['a']
            if e >= 255:
                e, phase = 255.0, 'd'
        elif phase == 'd':
            if v['s'] < 255:
                e = max(v['s'], e * v['d'] / 256.0) if v['d'] else v['s']
        env.append(e / 255.0)
        if f >= n_on and e < 1:
            break
    return np.array(env)


def render(mid, vg_text, kit_texts=(), tracks=None, t0=0.0, t1=None, master=1.0):
    """Mono offline-mix van de DirectSound-noten. tracks = MIDI-spoornummers (None = alle). kit_texts: teksten van
    de drumkits die voice_keysplit_all-regels noemen (op volgorde van naam opgezocht)."""
    vg = voices(vg_text)
    kits = {}
    for kt in kit_texts:
        nm = re.search(r'voice_group (\w+)', kt).group(1)
        base = int(re.search(r'voice_group \w+, (\d+)', kt).group(1)) if re.search(r'voice_group \w+, (\d+)', kt) else 0
        kits[nm] = (base, voices(kt))
    m = mido.MidiFile(mid)
    tempo = next((x.tempo for t in m.tracks for x in t if x.type == 'set_tempo'), 500000)
    tps = 1e6 / tempo * m.ticks_per_beat
    end = t1 if t1 is not None else m.length
    n_out = int((end - t0) * MIX) + MIX
    out = np.zeros(n_out)
    for ti, tr in enumerate(m.tracks):
        if tracks is not None and ti not in tracks:
            continue
        tick, prog, vol, on, notes = 0, 0, 100, {}, []
        for x in tr:
            tick += x.time
            if x.type == 'program_change':
                prog = x.program
            elif x.type == 'control_change' and x.control == 7:
                vol = x.value
            elif x.type == 'note_on' and x.velocity:
                on.setdefault(x.note, []).append((tick, x.velocity, prog, vol))
            elif x.type in ('note_on', 'note_off') and on.get(x.note):
                s, vel, p, vo = on[x.note].pop(0)
                notes.append((s, tick, x.note, vel, p, vo))
        for s, e, n, vel, p, vo in notes:
            ts, te = s / tps, e / tps
            if te < t0 or ts > end:
                continue
            line = vg[p] if p < len(vg) else ''
            key = n
            if line.startswith('voice_keysplit_all'):
                kn = re.search(r'voicegroup_(\w+)', line).group(1)
                if kn not in kits:
                    continue
                base, kl = kits[kn]
                if not (0 <= n - base < len(kl)):
                    continue
                v = parse(kl[n - base])
                if v is None:
                    continue
                key = v['key']
            else:
                v = parse(line)
                if v is None:
                    continue
            a, rate, lab, loop = sample(v['sample'])
            step = rate / MIX if v['fixed'] else rate * 2 ** ((key - lab) / 12.0) / MIX
            n_on = max(1, int(round((te - ts) * FPS)))
            env = envelope(n_on, v, n_on + 600)
            ln = int(len(env) / FPS * MIX)
            pos = np.arange(ln) * step
            if loop:
                L = loop[1] - loop[0]
                over = pos >= loop[1]
                pos[over] = loop[0] + (pos[over] - loop[0]) % L
            else:
                pos = pos[pos < len(a) - 1]
            ln = len(pos)
            if not ln:
                continue
            i0 = pos.astype(int)
            fr = pos - i0
            y = a[i0] * (1 - fr) + a[np.minimum(i0 + 1, len(a) - 1)] * fr
            ef = np.interp(np.arange(ln), np.arange(len(env)) * MIX / FPS, env)
            y = y * ef * (vel / 127.0) * (vo / 127.0) * master
            st = int((ts - t0) * MIX)
            if st < 0:
                y, st = y[-st:], 0
            k = min(len(y), n_out - st)
            if k > 0:
                out[st:st + k] += y[:k]
    if t1 is not None:
        out = out[:int((t1 - t0) * MIX)]
    return out, MIX


# ---- klankvergelijking: op welk GM-instrument lijkt een spoor? ------------------------------------------------------
SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
GM = {0: 'piano', 16: 'drawbar-orgel', 19: 'kerkorgel', 21: 'accordeon', 22: 'mondharmonica', 23: 'tango-accordeon',
      24: 'nylon (akoestisch)', 25: 'staalsnaar (akoestisch)', 27: 'clean gitaar', 28: 'muted gitaar',
      29: 'overdrive gitaar', 30: 'distortion gitaar', 33: 'fingered bas', 34: 'pick bas', 38: 'synth bas',
      45: 'pizzicato', 56: 'trompet', 61: 'koperblazers', 62: 'synth-brass', 73: 'fluit', 78: 'fluitje',
      79: 'ocarina', 81: 'zaagtand-lead', 105: 'banjo', 9: 'glockenspiel'}


def _feats(y, sr):
    import librosa
    y = y / (np.abs(y).max() + 1e-9)
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=256))
    e = (S ** 2).sum(0)
    act = e > 0.02 * np.percentile(e, 98)
    M = librosa.feature.mfcc(S=librosa.power_to_db(librosa.feature.melspectrogram(S=S ** 2, sr=sr, n_mels=40)),
                             n_mfcc=14)[1:]
    C = librosa.feature.spectral_contrast(S=S, sr=sr, n_bands=5)
    cen = librosa.feature.spectral_centroid(S=S, sr=sr)
    fl = np.log10(librosa.feature.spectral_flatness(S=S) + 1e-6)
    F = np.vstack([M, C, cen / 1000.0, fl])[:, act[:M.shape[1]]]
    return np.concatenate([F.mean(1), F.std(1)])


def timbre_rank(mid, track, vg_text, kit_texts=(), t0=10.0, t1=30.0, cands=GM, audio=None, chord=(0,)):
    """De noten van één MIDI-spoor (nagebootst met zijn eigen samples, of `audio` = (signaal, sr), bv. een solo-
    opname uit de game) vergeleken met FluidR3-renders van dezelfde noten per GM-instrument (MFCC/contrast/centroid/
    flatness, gestandaardiseerd): [(afstand, naam)] oplopend. Brawly v3 in de game: chugs -> mondharmonica/tango-
    accordeon, bas -> pick bas/pizzicato. chord = intervallen waarmee elke noot gerenderd wordt (een powerchord-
    sample tegen GM-powerchords, (0, 7, 12))."""
    import subprocess, tempfile, warnings
    import librosa
    warnings.filterwarnings('ignore')
    y, sr = audio if audio is not None else render(mid, vg_text, kit_texts, tracks=[track], t0=t0, t1=t1)
    target = _feats(y, sr)
    m = mido.MidiFile(mid)
    tempo = next((x.tempo for t in m.tracks for x in t if x.type == 'set_tempo'), 500000)
    ev, tick = [], 0
    for x in m.tracks[track]:
        tick += x.time
        if x.type in ('note_on', 'note_off'):
            ev.append((tick, x))
    rows = []
    with tempfile.TemporaryDirectory() as d:
        for prog, nm in cands.items():
            out = mido.MidiFile(ticks_per_beat=m.ticks_per_beat)
            t = mido.MidiTrack(); out.tracks.append(t)
            t.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
            t.append(mido.Message('program_change', program=prog, time=0))
            last = 0
            for tk, x in ev:
                if mido.tick2second(tk, m.ticks_per_beat, tempo) > t1:
                    break
                for j, iv in enumerate(chord):
                    t.append(x.copy(channel=0, note=min(127, x.note + iv), time=(tk - last) if j == 0 else 0))
                last = tk
            p, w = os.path.join(d, 'r.mid'), os.path.join(d, 'r.wav')
            out.save(p)
            subprocess.run(['fluidsynth', '-ni', '-g', '0.6', '-R', '0', '-C', '0', '-r', '22050', '-F', w, SF2, p],
                           check=True, capture_output=True)
            f = wave.open(w)
            a = np.frombuffer(f.readframes(f.getnframes()), np.int16).reshape(-1, f.getnchannels()).mean(1) / 32768.0
            a = librosa.resample(a[int(t0 * 22050):int(t1 * 22050)], orig_sr=22050, target_sr=sr)
            a = np.round(a / (np.abs(a).max() + 1e-9) * 100) / 100.0
            rows.append((nm, _feats(a, sr)))
    X = np.array([r[1] for r in rows] + [target])
    Z = (X - X.mean(0)) / (X.std(0) + 1e-9)
    return sorted((float(np.linalg.norm(Z[i] - Z[-1])), rows[i][0]) for i in range(len(rows)))

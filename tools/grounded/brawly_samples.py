#!/usr/bin/env python3
"""Project Grounded: samples voor Brawly v4 (gymleider-remix, nu-metal; gym_remixes.py). Voorvoegsel gym_bra4_.

Ronde 4 (Jordi over v3: 'speelgoedaccordeon/fluitje, blije akoestische tokkels, onhoorbare bas, dunne drums, de
scratches zijn weg'). Gemeten oorzaak: zie gym_remixes.py (brawly) en MUZIEK.md. Nieuwe samples, de oude gym_bra_*
blijven byte-identiek (ze staan in gym_samples.py en worden hier niet aangeraakt):
  gym_bra4_wall     langgerekte powerchord (I-V-I') uit de tweede Emerald-distortiongitaar
                    (sd90_classical_distortion_guitar_high, C4): C3 + G3 + C4, dubbel ingespeeld (±7 cent), label 48
  gym_bra4_chug     palm-mute-chug (C2-G2-C3) uit sd90_classical_distortion_guitar_low met plectrumaanslag en een
                    dichtklappende lowpass; vervangt de v3-stoten (gym_bra_epower, 2 ticks: 'accordeon')
  gym_bra4_bass     overdrive-bas uit de Emerald-fingered bass (sc88pro_fingered_bass, C4 op 53.516 Hz = C2 op 13.379 Hz):
                    voorversterking + tanh-overdrive + lage boost, label 36, met loop (aangehouden achtsten)
  gym_bra4_kick     zware metal-kick: FluidR3 Power-kick + een vel dat van 120 naar 50 Hz zakt + beaterklik
  gym_bra4_snare    volle heavy-rock-snare: FluidR3 Power-snare + vel op ±200 Hz + korte kamer (geen ring, geen gate)
  gym_bra4_scratch  turntable-scratches (baby/chirp) van een vervormde 'aah' + vinylruis: breedbandig
  gym_bra4_chirp    (spectral flatness >= 0,1, geen vaste toonhoogte); de v3-scratch was een zuivere glijtoon rond 900 Hz
                    (flatness 0,008) = 'fluitje/speelgoedaccordeon'
Gedeelde hulpjes uit sample_utils.py; render/filters gekopieerd (niet geïmporteerd uit een ander thema).
Gebruik: python3 tools/grounded/brawly_samples.py"""
import os, struct, subprocess, sys, tempfile, wave
import numpy as np
import mido
from scipy.signal import butter, sosfilt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import resample, auto_loop, write_wav

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
FS = 44100
GR = 13379
STANDARD, POWER = 0, 16


def render(prog, events, dur, kit=False):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    ch = 9 if kit else 0
    t.append(mido.Message('program_change', channel=ch, program=prog, time=0))
    ev = []
    for s, n, v, ln in events:
        ev.append((int(s * 960), 1, n, v))
        ev.append((int((s + ln) * 960), 0, n, 0))
    ev.append((int(dur * 960), 0, 0, 0))
    last = 0
    for tk, on, n, v in sorted(ev):
        t.append(mido.Message('note_on' if on else 'note_off', channel=ch, note=n, velocity=v, time=tk - last))
        last = tk
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', str(FS), '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    a = a / 32768.0
    start = int(np.argmax(np.abs(a) > 0.002))
    return a[start:start + int(dur * FS)]


def drum(kit, key, dur, vel=120):
    return render(kit, [(0, key, vel, dur)], dur, kit=True)


def note(prog, key, dur, vel=112):
    return render(prog, [(0, key, vel, dur)], dur + 0.05)


def flt(a, f, kind, order=2, fs=FS):
    return sosfilt(butter(order, f, kind, fs=fs, output='sos'), a)


def norm(a, peak=1.0):
    return a / max(1e-9, np.abs(a).max()) * peak


def env_exp(n, tau, fs=FS):
    return np.exp(-np.arange(n) / fs / tau)


def fade_out(a, sec=0.03, fs=FS):
    k = min(len(a), int(fs * sec))
    a = a.copy()
    a[-k:] *= np.linspace(1, 0, k)
    return a


def gba_load(name):
    path = 'sound/direct_sound_samples/%s.wav' % name
    w = wave.open(path)
    a = (np.frombuffer(w.readframes(w.getnframes()), np.uint8).astype(float) - 128) / 127
    d = open(path, 'rb').read()
    i = d.index(b'smpl')
    sm = struct.unpack('<9I', d[i + 8:i + 44])
    loop = None
    if sm[7]:
        l = struct.unpack('<6I', d[i + 44:i + 68])
        loop = (l[2], l[3] + 1)
    return a, w.getframerate(), loop


def gba_tone(name, m, dur, base=60, R=GR):
    """GBA-sample getransponeerd naar MIDI-toon m (base = toon op de eigen samplerate), via zijn loop aangehouden."""
    a, rate, loop = gba_load(name)
    eff = rate * 2 ** ((m - base) / 12.0)
    need = int(dur * eff) + 8
    if loop and len(a) < need:
        reps = (need - loop[0]) // (loop[1] - loop[0]) + 1
        a = np.concatenate([a[:loop[0]]] + [a[loop[0]:loop[1]]] * reps)
    a = resample(a[:need], eff, R)
    out = np.zeros(int(dur * R))
    out[:min(len(a), len(out))] = a[:len(out)]
    return out


# ---- de samples --------------------------------------------------------------------------------------------------------
def wall(dur=1.8):
    """Powerchord C3-G3-C4 uit sd90_classical_distortion_guitar_high (C4 op toets 60), twee keer ingespeeld (±7 cent:
    dubbelgetrackte rhythmgitaar), op 13.379 Hz; label 48."""
    a = np.zeros(int(dur * GR))
    for cents in (-7, 7):
        for m, g in ((48, 1.0), (55, 0.85), (60, 0.5)):
            a += g * gba_tone('sd90_classical_distortion_guitar_high', m + cents / 100.0, dur)
    a = flt(a, 70, 'highpass', fs=GR)
    a = np.tanh(norm(a) * 3.0)                                        # meer gain: fizz i.p.v. riet
    a = flt(a, 4200, 'lowpass', 4, fs=GR)
    return norm(a) + 0.5 * pick(len(a))


def pick(n, fs=GR, seed=11):
    """Plectrumaanslag: korte ruisstoot 1,5-5 kHz + klik; maakt van een aangehouden vervormde toon een gitaar (zonder
    aanslag klinkt een GBA-distortionakkoord als een rietinstrument: v3 'accordeon/mondharmonica')."""
    t = np.arange(n) / fs
    nz = flt(np.random.default_rng(seed).standard_normal(n), [1500, min(5000, fs * 0.45)], 'bandpass', fs=fs)
    return norm(nz) * np.exp(-t / 0.006)


def chug(dur=0.34):
    """Palm-mute-chug (drop C: C2-G2-C3) uit de Emerald-distortiongitaar (sd90_classical_distortion_guitar_low):
    plectrumaanslag, een dichtklappende lowpass (3 kHz -> 700 Hz in 50 ms = de hand op de snaren), lage 'chunk'
    (65 Hz, 60 ms) en een uitsterving van ±0,12 s. Eén sample per aanslag, geen loop."""
    n = int(dur * GR)
    t = np.arange(n) / GR
    a = sum(g * gba_tone('sd90_classical_distortion_guitar_low', m, dur, base=60)
            for m, g in ((36, 1.0), (43, 0.8), (48, 0.5)))
    a = np.tanh(norm(a) * 2.5)
    early = flt(a, 3000, 'lowpass', 2, fs=GR)
    late = flt(a, 700, 'lowpass', 2, fs=GR)
    mix = np.clip(t / 0.05, 0, 1)
    a = early * (1 - mix) + late * mix
    a = a * (0.25 + 0.75 * np.exp(-t / 0.05)) * np.exp(-t / 0.12)
    chunk = np.sin(2 * np.pi * 65.4 * t) * np.exp(-t / 0.06)
    a = norm(a) + 0.6 * chunk + 0.45 * pick(n)
    return fade_out(norm(a), 0.04, fs=GR)


def obass(dur=1.2):
    """Overdrive-bas: de Emerald-fingered bass (C4 @ 53.516 Hz) op 13.379 Hz = C2, lage boost, tanh x3, lowpass."""
    a = gba_tone('sc88pro_fingered_bass', 36, dur, base=36, R=GR)     # rate/4 = 13.379: precies een C2
    low = flt(a, 220, 'lowpass', 2, fs=GR)
    a = a + 3.0 * low                                                 # dik: +12 dB onder 220 Hz
    a = np.tanh(norm(a) * 4.0)
    a = a + 1.5 * flt(a, 200, 'lowpass', 2, fs=GR)                    # na de overdrive nog eens de bodem erbij
    a = flt(a, 1400, 'lowpass', 4, fs=GR)
    return flt(a, 35, 'highpass', 2, fs=GR)


def kick():
    n = int(0.40 * FS)
    t = np.arange(n) / FS
    k = np.zeros(n)
    p = drum(POWER, 36, 0.4, 127)
    k[:min(n, len(p))] = p[:n]
    f = 50 + 70 * np.exp(-t / 0.025)
    thump = np.sin(2 * np.pi * np.cumsum(f) / FS) * np.exp(-t / 0.16)
    click = flt(np.random.default_rng(3).standard_normal(n), [2500, 7000], 'bandpass') * np.exp(-t / 0.004)
    a = 0.8 * norm(k) + 1.0 * thump + 0.35 * click
    return fade_out(norm(np.tanh(norm(a) * 1.6)), 0.05)


def snare():
    n = int(0.55 * FS)
    t = np.arange(n) / FS
    sn = np.zeros(n)
    s0 = drum(POWER, 38, 0.5, 127)
    s1 = drum(STANDARD, 40, 0.5, 120)
    sn[:min(n, len(s0))] += s0[:n]
    sn[:min(n, len(s1))] += 0.5 * s1[:n]
    f = 195 + 70 * np.exp(-t / 0.010)
    body = np.sin(2 * np.pi * np.cumsum(f) / FS) * np.exp(-t / 0.06)
    rng = np.random.default_rng(21)
    wires = flt(rng.standard_normal(n), [1800, 7500], 'bandpass') * np.exp(-t / 0.11)
    room = flt(rng.standard_normal(n), [250, 4500], 'bandpass') * np.exp(-t / 0.20)
    a = norm(sn) + 0.9 * body + 0.45 * wires + 0.18 * room
    return fade_out(norm(np.tanh(norm(a) * 1.8)), 0.08)


def _scratch(strokes, seed):
    """strokes: [(duur in s, snelheidsprofiel-functie van 0..1 -> snelheid x origineel, fader 0/1)].
    Bron: 'aah' (koor, GM 52) hard vervormd + vinylruis en knetter, zodat de scratch breedbandig is."""
    rng = np.random.default_rng(seed)
    v = note(52, 62, 0.8, 127)
    v = np.tanh(norm(flt(v, 250, 'highpass')) * 6.0)
    src = norm(v) + 1.0 * norm(flt(rng.standard_normal(len(v)), [400, 6000], 'bandpass'))
    src = norm(src)
    out, pos = [], 0.08 * FS
    for dur, prof, fader in strokes:
        n = int(dur * FS)
        u = np.arange(n) / max(1, n - 1)
        sp = prof(u)
        p = np.clip(pos + np.cumsum(sp), 0, len(src) - 2)
        pos = p[-1]
        seg = np.interp(p, np.arange(len(src)), src) * np.minimum(1, np.abs(sp) * 0.9) * fader
        out.append(seg)
    a = np.concatenate(out)
    a += 0.12 * flt(rng.standard_normal(len(a)), [800, 5000], 'bandpass')          # naald op de plaat
    return fade_out(norm(flt(a, 300, 'highpass')), 0.01)


def scratch():
    """'Wikka-wikka': vier snelle baby-strokes heen en weer (snelheid 0 -> 4x -> 0, dan achteruit), ±0,32 s."""
    fwd = lambda u: 4.2 * np.sin(np.pi * u) ** 0.7
    back = lambda u: -3.6 * np.sin(np.pi * u) ** 0.7
    return _scratch([(0.07, fwd, 1), (0.08, back, 1), (0.07, fwd, 1), (0.10, back, 1)], 5)


def chirp():
    """Chirp: snel vooruit met de fader open, terug met de fader dicht na de helft, twee keer, ±0,24 s."""
    fwd = lambda u: 5.0 * np.sin(np.pi * u) ** 0.5
    back = lambda u: -4.0 * np.sin(np.pi * u) ** 0.5 * (u < 0.45)
    return _scratch([(0.06, fwd, 1), (0.06, back, 1), (0.05, fwd, 1), (0.07, back, 1)], 7)


def build():
    """naam -> (signaal, samplerate van het signaal, samplerate in de rom, label-toets, loop?)"""
    return {
        'gym_bra4_wall': (wall(), GR, GR, 48, True),
        'gym_bra4_bass': (obass(), GR, GR, 36, True),
        'gym_bra4_chug': (chug(), GR, GR, 36, False),
        'gym_bra4_kick': (kick(), FS, 16000, 60, False),
        'gym_bra4_snare': (snare(), FS, 16000, 60, False),
        'gym_bra4_scratch': (scratch(), FS, 16000, 60, False),
        'gym_bra4_chirp': (chirp(), FS, 16000, 60, False),
    }


def main():
    inc = open(DATA).read()
    for name, (a, fs, rate, key, loop) in build().items():
        a = norm(resample(np.asarray(a, float), fs, rate) if fs != rate else np.asarray(a, float), 0.97)
        lpnt = None
        if loop:
            a, lpnt = auto_loop(a, rate)
        else:
            a = fade_out(a, 0.01, fs=rate)
        write_wav(OUT + name + '.wav', a, rate, key, lpnt)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-18s %6d samples @ %5d Hz, toets %d, loop %s' % (name, len(a), rate, key, lpnt))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()

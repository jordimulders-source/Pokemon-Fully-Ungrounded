#!/usr/bin/env python3
"""Project Grounded: samples voor de gymleider-remixes (gym_remixes.py): Roxanne (hard rock power ballad), Brawly
(nu-metal), Wattson (gabber/happy hardcore) en Flannery (flamenco). Voorvoegsel gym_.

Uit FluidR3 (fluidsynth, apt-get install fluidsynth fluid-soundfont-gm) of gesynthetiseerd; gedeelde hulpjes uit
sample_utils.py. Melodische instrumenten met een groot bereik krijgen een sample per octaaf (gym_remixes.py kiest per
noot het programma met de dichtstbijzijnde grondtoon), zodat niets ver getransponeerd wordt.
Akkoorden (powerchords, rasgueado, supersaw-stoten) zijn één sample = één kanaal per aanslag, zonder terts (de
harmonie van het origineel is grondtoon + kwint veilig: C, Bb, Db, Eb).
Ronde 2 (Jordi: 'echte Emerald-/GBA-samples'): byte-kopieën van GBA-samples met een andere label-toets (COPIES)
en gym_bra_epower, een powerchord die alleen uit de Emerald-distortiongitaar (sd90_classical_distortion_guitar_low)
bestaat, offline een octaaf (en een kwint) omlaag getransponeerd = drop-tuning.
Gebruik: python3 tools/grounded/gym_samples.py"""
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
STANDARD, POWER, ELECTRONIC = 0, 16, 24     # FluidR3-drumkits (kanaal 10)


# ---- renderen ------------------------------------------------------------------------------------------------------
def render(prog, events, dur, kit=False):
    """events: [(tijd in s, noot, velocity, lengte in s)] -> mono float op 44,1 kHz."""
    m = mido.MidiFile(ticks_per_beat=480)       # 120 bpm: 1 s = 960 ticks
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


def note(prog, key, dur, vel=112):
    return render(prog, [(0, key, vel, dur)], dur + 0.05)


def chord(prog, keys, dur, vel=112, spread=0.0):
    return render(prog, [(i * spread, k, vel, dur) for i, k in enumerate(keys)], dur + 0.05)


def drum(kit, key, dur, vel=120):
    return render(kit, [(0, key, vel, dur)], dur, kit=True)


def lp(a, f, order=4):
    return sosfilt(butter(order, f, 'lowpass', fs=FS, output='sos'), a)


def hp(a, f, order=2):
    return sosfilt(butter(order, f, 'highpass', fs=FS, output='sos'), a)


def bp(a, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], 'bandpass', fs=FS, output='sos'), a)


def norm(a, peak=1.0):
    return a / max(1e-9, np.abs(a).max()) * peak


def env_exp(n, tau):
    return np.exp(-np.arange(n) / FS / tau)


def fade_out(a, sec=0.03):
    k = min(len(a), int(FS * sec))
    a = a.copy()
    a[-k:] *= np.linspace(1, 0, k)
    return a


def crunch(a, drive=4.0, presence=1200, top=5500):
    """Gitaarversterker in de stijl van een Gen 3-sample: verzadigd, presence-bult, geen 'lucht'."""
    a = hp(a, 70)
    a = np.tanh(norm(a) * drive)
    a = a + 0.4 * bp(a, presence * 0.7, presence * 1.4)
    return lp(np.tanh(norm(a) * 1.5), top)


# ---- synthese -------------------------------------------------------------------------------------------------------
def saw(f, n, phase=0.0, rate=FS):
    """Bandbegrensde zaagtand (additief, tot 0,45 x de samplerate)."""
    t = np.arange(n) / rate
    out = np.zeros(n)
    k = 1
    fmax = np.max(f) if np.ndim(f) else f
    ph = 2 * np.pi * (np.cumsum(f) / rate if np.ndim(f) else f * t) + phase
    while k * fmax < 0.45 * rate and k < 80:
        out += np.sin(k * ph + k * phase) / k
        k += 1
    return out


def supersaw(f0, dur, voices=7, detune=0.011, seed=1):
    rng = np.random.default_rng(seed)
    n = int(dur * FS)
    a = np.zeros(n)
    for d in np.linspace(-detune, detune, voices):
        a += saw(f0 * (1 + d), n, rng.uniform(0, 2 * np.pi))
    return a


def gabber_kick():
    """Rotterdamse gabberkick: sinus die van ±330 Hz naar ±52 Hz zakt, hard geclipt (de vervorming geeft de 'brr'),
    klikje vooraan; ±0,30 s."""
    n = int(0.30 * FS)
    t = np.arange(n) / FS
    f = 52 + 280 * np.exp(-t / 0.022) + 40 * np.exp(-t / 0.09)
    a = np.sin(2 * np.pi * np.cumsum(f) / FS)
    a *= np.minimum(1, t / 0.001) * np.where(t < 0.17, 1.0, np.exp(-(t - 0.17) / 0.05))
    a = np.tanh(a * 9) * 0.9
    click = np.random.default_rng(3).standard_normal(n) * np.exp(-t / 0.002) * 0.6
    a = lp(hp(a + click, 35), 7000)
    return fade_out(norm(a), 0.02)


def hoover(f0, dur):
    """'Hoover' (Alpha Juno): drie ontstemde pulsgolven met PWM, een octaaf eronder, en een toonhoogte die bij de
    aanslag van -5 halve tonen omhoog glijdt ('whoo')."""
    n = int(dur * FS)
    t = np.arange(n) / FS
    glide = 2 ** (-5 / 12 * np.exp(-t / 0.045))
    a = np.zeros(n)
    for k, d in enumerate((-0.012, 0.0, 0.013)):
        f = f0 * (1 + d) * glide
        ph = np.cumsum(f) / FS
        duty = 0.5 + 0.35 * np.sin(2 * np.pi * (0.9 + 0.3 * k) * t)
        a += np.where((ph % 1.0) < duty, 1.0, -1.0) - (2 * duty - 1)
    a += 0.8 * saw(f0 / 2 * glide, n)
    a = lp(a, 3200)
    return norm(a)


def cajon_bass():
    n = int(0.22 * FS)
    t = np.arange(n) / FS
    f = 68 + 50 * np.exp(-t / 0.02)
    a = np.sin(2 * np.pi * np.cumsum(f) / FS) * np.exp(-t / 0.09)
    knock = lp(np.random.default_rng(5).standard_normal(n), 900) * np.exp(-t / 0.012) * 0.5
    return fade_out(norm(np.tanh((a + knock) * 1.5)))


def cajon_slap():
    """Cajón-slap: hout (±230 Hz, kort) + de snaren achter de slagplank (ruis 1,5-6 kHz)."""
    n = int(0.16 * FS)
    t = np.arange(n) / FS
    rng = np.random.default_rng(7)
    body = np.sin(2 * np.pi * 230 * t) * np.exp(-t / 0.025)
    wires = bp(rng.standard_normal(n), 1500, 6000) * np.exp(-t / 0.045)
    click = rng.standard_normal(n) * np.exp(-t / 0.0015)
    return fade_out(norm(0.7 * body + 1.1 * norm(wires) + 0.3 * click))


def scratch():
    """DJ-scratch (Slipknot-achtig): een kort koor-'aah' heen en weer over de plaat (snelheid +/-)."""
    src = norm(note(52, 60, 0.6, 120))
    n = int(0.36 * FS)
    t = np.arange(n) / FS
    speed = 2.2 * np.sin(2 * np.pi * t / 0.18) * np.abs(np.sin(2 * np.pi * t / 0.36)) ** 0.3
    pos = np.clip(0.05 * FS + np.cumsum(speed), 0, len(src) - 2)
    a = np.interp(pos, np.arange(len(src)), src) * np.minimum(1, np.abs(speed) * 1.5)
    return fade_out(norm(hp(a, 200)))


# ---- GBA-samples (ronde 2) -----------------------------------------------------------------------------------------
def gba_load(name):
    """GBA-sample uit sound/direct_sound_samples/<name>.wav: (signaal -1..1, samplerate, loop (begin, eind) of None)."""
    path = 'sound/direct_sound_samples/%s.wav' % name
    w = wave.open(path)
    assert w.getsampwidth() == 1
    a = (np.frombuffer(w.readframes(w.getnframes()), np.uint8).astype(float) - 128) / 127
    d = open(path, 'rb').read()
    i = d.index(b'smpl')
    sm = struct.unpack('<9I', d[i + 8:i + 44])
    loop = None
    if sm[7]:
        lp_ = struct.unpack('<6I', d[i + 44:i + 68])
        loop = (lp_[2], lp_[3] + 1)
    return a, w.getframerate(), loop, sm[3]


# byte-kopie: naam -> (GBA-sample, label-toets). Het label zegt op welke MIDI-toets de sample zijn opgenomen
# toonhoogte speelt: de Gen 3-nylongitaar is een C3 die in de vanilla-voicegroups op toets 60 staat (klinkt een
# octaaf lager dan geschreven); met label 48 klinkt elke MIDI-noot op zijn eigen hoogte.
COPIES = {'gym_fla_gba_nylon': ('sc88pro_nylon_str_guitar', 48)}


def emerald_power(dur=1.3):
    """Drop-gestemde powerchord uit de Emerald-distortiongitaar (C3): dezelfde sample op halve snelheid (C2), x0,749
    (G2) en origineel (C3), gemengd en op 13.379 Hz gelaten (geen FluidR3, geen eigen versterker)."""
    a, rate, loop, key = gba_load('sd90_classical_distortion_guitar_low')
    n = int(dur * rate)
    body = list(a[:loop[1]])
    while len(body) < 2 * n + 10:                 # loop uitrollen
        body += list(a[loop[0]:loop[1]])
    body = np.array(body)
    out = np.zeros(n)
    for ratio, gain in ((0.5, 1.0), (0.5 * 2 ** (7 / 12), 0.75), (1.0, 0.5)):
        pos = np.arange(n) * ratio
        out += gain * np.interp(pos, np.arange(len(body)), body)
    out = hp(resample(out, rate, FS), 45)
    return norm(np.tanh(norm(out) * 1.6))


# ---- ronde 3 (anti-kermis) -------------------------------------------------------------------------------------------
GR = 13379                                       # samplerate van de Gen 3-samples


def gba_tone(name, m, dur, base=60, R=GR):
    """Een GBA-sample getransponeerd naar MIDI-toon m (base = de toon die de sample op zijn eigen samplerate
    speelt), aangehouden via zijn loop, op samplerate R."""
    a, rate, loop, _ = gba_load(name)
    eff = rate * 2 ** ((m - base) / 12.0)
    need = int(dur * eff) + 8
    if loop and len(a) < need:
        reps = (need - loop[0]) // (loop[1] - loop[0]) + 1
        a = np.concatenate([a[:loop[0]]] + [a[loop[0]:loop[1]]] * reps)
    a = resample(a[:need], eff, R)
    out = np.zeros(int(dur * R))
    out[:min(len(a), len(out))] = a[:len(out)]
    return out


VOICING = {'five': (45, 52, 57, 64), 'maj': (45, 52, 57, 61, 64)}   # A2-E3-A3-(C#4)-E4, open snaren


def nylon_strum(kind, quality):
    """Strum op de Emerald-nylongitaar (sc88pro_nylon_str_guitar, opgenomen als C3) als één sample = één kanaal:
    down (alle snaren laag -> hoog, 14 ms per snaar), up (hoge snaren hoog -> laag, zachter), golpe (gedempte slag +
    tik op het klankblad) en rasg (rasgueado: vier vingers e-a-m-i vlak na elkaar, dan de accentslag op 0,112 s;
    gym_remixes.py zet deze noot 0,112 s vóór de tel). Natuurlijke uitsterving, niets afgekapt."""
    v = VOICING[quality]
    dur = {'down': 1.2, 'up': 0.8, 'golpe': 0.3, 'rasg': 1.3}[kind]
    n = int(dur * GR)
    tt = np.arange(n) / GR
    tone = {m: gba_tone('sc88pro_nylon_str_guitar', m, dur, base=48) for m in v}

    def stroke(t0, keys, gap, gain, tau):
        out = np.zeros(n)
        for i, m in enumerate(keys):
            s = int((t0 + i * gap) * GR)
            if s >= n:
                break
            x = tone[m][:n - s] * np.exp(-np.arange(n - s) / GR / tau)
            out[s:] += x * gain * (1.0 - 0.06 * i)
        return out
    if kind == 'down':
        a = stroke(0, v, 0.014, 1.0, 0.55)
    elif kind == 'up':
        a = stroke(0, v[::-1][:4], 0.010, 0.75, 0.35)
    elif kind == 'golpe':
        a = stroke(0, v, 0.004, 0.9, 0.035)
        rng = np.random.default_rng(31)
        knock = lp(rng.standard_normal(n), 2200) * np.exp(-tt / 0.006) * 0.5
        thump = np.sin(2 * np.pi * 120 * tt) * np.exp(-tt / 0.02) * 0.6
        a = a / max(1e-9, np.abs(a).max()) + knock + thump
    else:
        a = np.zeros(n)
        for j, g in enumerate((0.45, 0.55, 0.65, 0.75)):
            a += stroke(j * 0.028, v, 0.005, g, 0.06)
        a += stroke(0.112, v, 0.008, 1.0, 0.55)
    a = resample(a, GR, FS)
    return fade_out(norm(a), 0.04)


def room(n, tau, lo, hi, seed, pre=0.006):
    """Natuurlijke naklink (geen gate): ruis door een bandfilter, exponentieel uitstervend, na een korte pre-delay."""
    rng = np.random.default_rng(seed)
    t = np.arange(n) / FS
    x = bp(rng.standard_normal(n), lo, hi) * np.exp(-np.maximum(0, t - pre) / tau) * (t >= pre)
    return x


def rock_snare():
    """Diepe, volle 80s rock-snare: FluidR3 Power-snare + een vel dat op ±190 Hz zakt + een natuurlijke kamer-
    naklink van ±0,8 s (geen gated reverb, geen tonale 'tonk': sd90_solo_snare ringt op 553 Hz, piek/mediaan 54)."""
    n = int(0.95 * FS)
    t = np.arange(n) / FS
    sn = np.zeros(n)
    s0 = drum(POWER, 38, 0.6, 127)
    sn[:len(s0)] = s0[:n]
    f = 185 + 60 * np.exp(-t / 0.012)
    body = np.sin(2 * np.pi * np.cumsum(f) / FS) * np.exp(-t / 0.09)
    tail = lp(room(n, 0.30, 250, 6000, 41), 4200) * 0.4 + lp(room(n, 0.45, 120, 2000, 43), 1500) * 0.6
    a = norm(sn) + 1.1 * body + tail
    a = np.tanh(norm(a) * 1.4)
    return fade_out(norm(a), 0.08)


def emerald_power_open(dur=1.6):
    """Langgerekte powerchord (I-V-I') uit de Emerald-distortiongitaar (sd90_classical_distortion_guitar_low, C3):
    de sample op C3, G3 en C4 opgeteld, op 13.379 Hz gelaten; label 48."""
    a = sum(g * gba_tone('sd90_classical_distortion_guitar_low', m, dur, base=48)
            for m, g in ((48, 1.0), (55, 0.8), (60, 0.55)))
    a = hp(resample(a, GR, FS), 60)
    return norm(np.tanh(norm(a) * 1.3))


def scratch2():
    """Tweede DJ-scratch (chirp): het koor-'aah' van scratch() één keer snel vooruit en terug, fader dicht op de
    terugweg-helft."""
    src = norm(note(52, 64, 0.6, 120))
    n = int(0.22 * FS)
    t = np.arange(n) / FS
    speed = 3.2 * np.sin(2 * np.pi * t / 0.22)
    pos = np.clip(0.06 * FS + np.cumsum(speed), 0, len(src) - 2)
    fader = np.where(t < 0.13, 1.0, np.clip((0.16 - t) / 0.03, 0, 1)) * np.minimum(1, np.abs(speed) * 1.2)
    a = np.interp(pos, np.arange(len(src)), src) * fader
    return fade_out(norm(hp(a, 250)))


def palmas(kind):
    """Palmas: clara (scherp: side stick + handklap, drie mensen net niet tegelijk) of sorda (holle handen,
    gedempt). Met een korte kamernaklink zodat niets afgekapt klinkt."""
    n = int((0.38 if kind == 'clara' else 0.28) * FS)
    out = np.zeros(n)
    st = drum(STANDARD, 37, 0.2, 120)
    cl = drum(STANDARD, 39, 0.25, 118)
    for off, sp, g in ((0, 1.0, 1.0), (0.008, 0.95, 0.8), (0.017, 1.06, 0.7)):
        x = cl if kind == 'sorda' else 0.7 * st[:min(len(st), len(cl))] + 0.6 * hp(cl[:min(len(st), len(cl))], 1200)
        x = resample(x, FS, FS / sp, antialias=False)
        s = int(off * FS)
        k = min(len(x), n - s)
        out[s:s + k] += g * x[:k]
    if kind == 'sorda':
        out = lp(out, 1100)
        out += room(n, 0.06, 300, 2500, 51) * 0.25
    else:
        out += room(n, 0.09, 900, 6500, 53) * 0.3
    return fade_out(norm(out), 0.05)


# ---- de lijst --------------------------------------------------------------------------------------------------------
def build():
    """naam -> (signaal op 44,1 kHz, samplerate, label-toets, loop?)"""
    S = {}

    def guitar(name, prog, keys, dur, rate, drive, loop=True, top=5500):
        for k in keys:
            S['%s_%d' % (name, k)] = (crunch(note(prog, k, dur, 118), drive, top=top), rate, k, loop)

    # Roxanne: hard rock power ballad
    S['gym_rox_power'] = (crunch(chord(30, (45, 52, 57), 1.6, 118), 3.0), 18000, 45, True)
    guitar('gym_rox_lead', 29, (60, 72, 84), 1.1, 18000, 3.0, top=6000)       # overdrive, zingend
    for k in (60, 72):
        S['gym_rox_clean_%d' % k] = (lp(note(27, k, 1.3, 100), 6000), 18000, k, False)
    S['gym_rox_kick'] = (drum(POWER, 36, 0.35), 16000, 60, False)
    sn = drum(POWER, 38, 0.30)
    tail = bp(np.random.default_rng(11).standard_normal(int(0.30 * FS)), 900, 7000) * 0.35
    tail *= np.where(np.arange(len(tail)) < 0.20 * FS, 1.0, 0.0) * env_exp(len(tail), 0.25)   # 'gated reverb' (jaren 80)
    S['gym_rox_snare'] = (fade_out(norm(sn[:len(tail)] + tail[:len(sn)])), 16000, 60, False)
    S['gym_rox_hat'] = (drum(STANDARD, 42, 0.12, 100), 16000, 60, False)
    S['gym_rox_crash'] = (drum(POWER, 49, 1.6), 16000, 60, False)
    for k in (41, 45, 48):
        S['gym_rox_tom_%d' % k] = (drum(POWER, k, 0.45), 16000, 60, False)

    # Brawly: nu-metal (drop-gestemd, C2-powerchords)
    pm = chord(30, (36, 43, 48), 0.30, 120)
    pm = pm * env_exp(len(pm), 0.06)
    S['gym_bra_chug'] = (fade_out(crunch(pm, 5.0, presence=900, top=4500) * env_exp(len(pm), 0.10)), 16000, 36, False)
    S['gym_bra_power'] = (crunch(chord(30, (36, 43, 48), 1.4, 120), 5.0, presence=900, top=4500), 16000, 36, True)
    guitar('gym_bra_lead', 30, (60, 72, 84), 1.0, 18000, 4.0)
    guitar('gym_bra_lead2', 29, (60, 72, 84), 1.0, 18000, 3.0, top=5000)
    S['gym_bra_bass'] = (np.tanh(norm(note(34, 36, 0.9, 120)) * 2.5), 16000, 36, True)
    kick = drum(STANDARD, 36, 0.25)
    S['gym_bra_kick'] = (norm(kick + 0.25 * hp(drum(STANDARD, 37, 0.25)[:len(kick)], 2000)), 16000, 60, False)
    S['gym_bra_snare'] = (norm(np.tanh(norm(drum(STANDARD, 40, 0.25)) * 2.0)), 16000, 60, False)
    S['gym_bra_hat'] = (drum(STANDARD, 42, 0.10, 100), 16000, 60, False)
    S['gym_bra_china'] = (drum(STANDARD, 52, 1.2), 16000, 60, False)
    S['gym_bra_crash'] = (drum(STANDARD, 57, 1.4), 16000, 60, False)
    for k in (41, 45, 48):
        S['gym_bra_tom_%d' % k] = (drum(STANDARD, k, 0.4), 16000, 60, False)
    S['gym_bra_scratch'] = (scratch(), 16000, 60, False)

    # Wattson: gabber / happy hardcore
    S['gym_wat_kick'] = (gabber_kick(), 18000, 60, False)
    S['gym_wat_snare'] = (drum(ELECTRONIC, 40, 0.18), 16000, 60, False)
    for k in (60, 72, 84):
        f0 = 440 * 2 ** ((k - 69) / 12)
        S['gym_wat_saw_%d' % k] = (lp(supersaw(f0, 1.2, seed=k), 7000), 22050, k, True)
    f0 = 440 * 2 ** ((55 - 69) / 12)              # G3: stoot grondtoon + kwint + octaaf, kort
    stab = sum(supersaw(f0 * r, 0.35, 5, 0.009, seed=i) for i, r in enumerate((1, 1.4983, 2)))
    stab = lp(stab, 6500) * np.minimum(1, np.arange(len(stab)) / FS / 0.003) * env_exp(len(stab), 0.10)
    S['gym_wat_stab'] = (fade_out(norm(stab)), 22050, 55, False)
    S['gym_wat_hoover'] = (hoover(440 * 2 ** ((48 - 69) / 12), 1.4), 18000, 48, True)
    bass = sum(saw(65.406 * (1 + d), int(0.30 * FS)) for d in (-0.006, 0.006))
    bass = lp(bass, 1400) * np.minimum(1, np.arange(len(bass)) / FS / 0.002) * env_exp(len(bass), 0.12)
    S['gym_wat_bass'] = (fade_out(norm(np.tanh(norm(bass) * 2))), 16000, 36, False)

    # Flannery: flamenco
    for k in (60, 72, 84):
        S['gym_fla_nylon_%d' % k] = (lp(note(24, k, 1.2, 110), 7000), 18000, k, False)
    for k in (60, 72):
        S['gym_fla_violin_%d' % k] = (lp(note(40, k, 1.1, 110), 7000), 18000, k, True)
    voicing = (45, 52, 57, 64)                     # A2 E3 A3 E4: open kwinten, geen terts
    strokes = [(s + i * 0.007, k, 118 - 6 * j, 0.9 - s) for j, s in enumerate((0, 0.032, 0.064, 0.096))
               for i, k in enumerate(voicing)]   # rasgueado: vier vingers na elkaar (e-a-m-i)
    S['gym_fla_rasg'] = (fade_out(lp(render(24, strokes, 1.0), 7000)), 18000, 45, False)
    S['gym_fla_strum'] = (fade_out(lp(chord(24, voicing, 0.8, 112, 0.009), 7000)), 18000, 45, False)
    g = chord(24, voicing, 0.20, 120, 0.004)
    knock = lp(np.random.default_rng(9).standard_normal(len(g)), 2500) * env_exp(len(g), 0.006)
    S['gym_fla_golpe'] = (fade_out(norm(g * env_exp(len(g), 0.035) + 0.5 * knock)), 18000, 45, False)
    c = drum(STANDARD, 39, 0.25, 120)
    claps = np.zeros(len(c) + 900)
    for off, sp, gain in ((0, 1.0, 1.0), (380, 0.93, 0.8), (760, 1.07, 0.7)):   # drie mensen klappen
        x = resample(c, FS, FS / sp, antialias=False)[:len(c)]
        claps[off:off + len(x)] += gain * x
    S['gym_fla_palmas'] = (fade_out(norm(claps)), 16000, 60, False)
    S['gym_fla_sorda'] = (fade_out(norm(lp(claps, 1300)) * 0.8), 16000, 60, False)     # palmas sordas (gedempt)
    S['gym_fla_cajon_bass'] = (cajon_bass(), 16000, 60, False)
    S['gym_fla_cajon_slap'] = (cajon_slap(), 16000, 60, False)
    S['gym_fla_castanets'] = (drum(STANDARD, 85, 0.15), 16000, 60, False)

    # ronde 2: Brawly drop-gestemd met de Emerald-distortiongitaar (C2 = toets 36)
    S['gym_bra_epower'] = (emerald_power(), 13379, 36, True)

    # ronde 3 (anti-kermis): Roxanne 80s hard rock, Brawly-scratch 2, Flannery rumba flamenca
    S['gym_rox_rsnare'] = (rock_snare(), 16000, 60, False)
    S['gym_rox_ride'] = (fade_out(hp(drum(STANDARD, 51, 1.1, 100), 300), 0.1), 16000, 60, False)
    S['gym_rox_open'] = (emerald_power_open(), GR, 48, True)
    S['gym_rox_pbass'] = (lp(np.tanh(norm(note(34, 36, 0.9, 120)) * 2.2), 2200), GR, 36, True)
    S['gym_bra_scratch2'] = (scratch2(), 16000, 60, False)
    for q in VOICING:
        for kind in ('down', 'up', 'golpe', 'rasg'):
            S['gym_fla_%s_%s' % (kind, q)] = (nylon_strum(kind, q), GR, 45, False)
    S['gym_fla_pclara'] = (palmas('clara'), 16000, 60, False)
    S['gym_fla_psorda'] = (palmas('sorda'), 16000, 60, False)
    return S


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    total = 0
    for name, (a, rate, key, loop) in build().items():
        a = resample(np.asarray(a, float), FS, rate)
        a = norm(a, 0.97)
        lpnt = None
        if loop:
            a, lpnt = auto_loop(a, rate)
        else:
            a = fade_out(a, 0.01 * rate / FS)
        write_wav(OUT + name + '.wav', a, rate, key, lpnt)
        total += len(a)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-22s %6d samples @ %5d Hz, toets %d, loop %s' % (name, len(a), rate, key, lpnt))
    for name, (src, key) in COPIES.items():          # byte-kopieën met een ander label
        a, rate, loop, _ = gba_load(src)
        write_wav(OUT + name + '.wav', a, rate, key, loop)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-22s kopie van %s, toets %d' % (name, src, key))
    open(DATA, 'w').write(inc)
    print('totaal %.0f KB' % (total / 1024))


if __name__ == '__main__':
    main()

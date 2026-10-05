#!/usr/bin/env python3
"""Project Grounded: de samples voor Battle! Genesect (genesect_theme.py): industrial / big beat à la The Prodigy met
hard-techno-delen. Eigen generator (gm_samples.py en de generatoren van andere thema's blijven ongemoeid; alleen de
gedeelde hulpjes uit sample_utils.py worden geïmporteerd). Alles met een lowpass rond 7-8 kHz (niet schel) en hard
verzadigd (gecomprimeerd), zodat het in de 8-bit-mix vet blijft zonder te snijden.

Gesynthetiseerd, met een exacte loop (M perioden van de grondtoon per loop; stem k heeft M + k trillingen, zodat de
zweving in de sample zit), vervormd op 8x de samplerate en daarna periodiek FFT-gefilterd (geen aliasing):
  genesect_bass      : distorted bas (twee ontstemde zaagtanden + blokgolf een octaaf lager), lowpass 2,6 kHz, op E2.
  genesect_bass_dark : dezelfde, dichter (lowpass 900 Hz) voor de intro en de stille stukken.
  genesect_lead      : de hook-lead: 'hoover'-achtige gescheurde synth (drie ontstemde zaagtanden + puls), lowpass
                       4,2 kHz, op C5.
Eenmalig (tijddomein):
  genesect_acid / _acc : 303-acid-pluk (zaagtand door een resonant lowpass met filterenvelope, verzadigd), op C3;
                       _acc = accent (filter verder open, meer resonantie).
  genesect_stab      : Prodigy-noisestoot: E-powerchord (E3-B3-E4) van zaagtanden + ruis, hard vervormd, op E3.
  genesect_ohit      : orchestra hit (FluidR3 GM 55, E-mineur) door de fuzz: de 'sample-hit' van big beat, op E4.
  genesect_cannon    : het kanon (Techno Blast): laserzap omlaag + dreun 120 -> 32 Hz + ruisexplosie.
Drums (eigen kit):
  genesect_kick      : harde big-beat/techno-kick (sinus 175 -> 46 Hz, klik, hard verzadigd = gecomprimeerd).
  genesect_rumble    : hard-techno-rumble: de kick door een galmstaart, vervormd en lowpass (k-r-r-r na elke kick).
  genesect_snare     : breakbeat-snare: FluidR3 (standard + room 38) + ruiscrack 1,5-7 kHz, hard gecomprimeerd.
  genesect_ghost     : dezelfde snare, kort (ghost notes, roffels).
  genesect_hat / _ohat : metalen hihat (zes blokgolven op de 808-verhoudingen + FluidR3 42/46), lowpass 8 kHz.
  genesect_anvil     : aambeeld (inharmonische partialen 1 / 2,32 / 4,25 / 6,63 / 9,38, elk met eigen uitsterftijd).
  genesect_pipe      : lage metalen buis/plaat (dezelfde opbouw op 190 Hz, langer).
  genesect_press     : machinepers: perslucht-'tssh' + dreun + metalen klank.
  genesect_revcym    : FluidR3-crash achterstevoren (aanloop naar een drop).
v2 (Jordi: 'klonk als een funk-groove' -> meedogenloze Prodigy big beat / hard techno):
  genesect_dbass     : overstuurde bas (zaagtand + blokgolf, tanh x6 + middenboost 1,2 kHz), lowpass 3,2 kHz, op E2.
  genesect_istab     : industriële stoot: tritonus-cluster E3-Bb3-E4 (zaagtanden) + metaalruis, tanh x5, op E3.
  genesect_kick2     : denderende kick (sinus 190 -> 44 Hz, langer lijf, tanh x5 = plat geslagen).
  genesect_snare2    : extreem agressieve snare: snare + 909-clap + ruiscrack 1,8-6,5 kHz, tanh x7.
  genesect_roll2     : dezelfde snare kort (70 ms) voor 16den/32sten-roffels.
Labels achteraan sound/direct_sound_data.inc (na .align 2).
Gebruik: python3 tools/grounded/genesect_samples.py"""
import os, subprocess, sys, tempfile, wave
import numpy as np
import mido
from scipy.signal import butter, sosfilt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import resample, write_wav

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'


def hz(note):
    return 440 * 2 ** ((note - 69) / 12)


def render(prog, notes, dur, kit=None, vel=110):
    """FluidR3: kit = drumkit-programma (0 standard, 8 room, 16 power, 24 electronic) op kanaal 10."""
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    ch = 9 if kit is not None else 0
    t.append(mido.Message('program_change', channel=ch, program=kit if kit is not None else prog, time=0))
    for n in notes:
        t.append(mido.Message('note_on', channel=ch, note=n, velocity=vel, time=0))
    for i, n in enumerate(notes):
        t.append(mido.Message('note_off', channel=ch, note=n, velocity=0, time=int(dur * 960) if i == 0 else 0))
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', '44100', '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    a = a / 32768.0
    s = np.argmax(np.abs(a) > 0.002)
    a = a[s:s + int(dur * 44100)]
    return np.pad(a, (0, int(dur * 44100) - len(a)))


def norm(a, peak=0.97):
    return a / max(1e-9, np.abs(a).max()) * peak


def fade_out(a, rate, sec):
    n = min(len(a), int(rate * sec))
    a = a.copy()
    a[-n:] *= np.linspace(1, 0, n) ** 2
    return a


def lp(a, rate, fc, order=4):
    return sosfilt(butter(order, min(fc, 0.45 * rate), 'lowpass', fs=rate, output='sos'), a)


def hp(a, rate, fc, order=2):
    return sosfilt(butter(order, fc, 'highpass', fs=rate, output='sos'), a)


def bp(a, rate, lo, hi, order=2):
    return sosfilt(butter(order, [lo, min(hi, 0.45 * rate)], 'bandpass', fs=rate, output='sos'), a)


# ---------------------------------------------------------------- aanhoudend (exacte loop)
def periodic(note, per, M, voices, drive, cut, over=8, sub_fund=1.0, mid_boost=None, seed=11):
    """voices: [(k, amp, vorm, octaaf)] met vorm 'saw' / 'sq' / 'pulse'; stem k heeft M + k trillingen per loop (x 2^oct).
    Vervormd (tanh) op `over` x de samplerate, dan een periodiek FFT-lowpass (24 dB/oct) terug naar per samples per
    periode: exacte loop, geen aliasing."""
    f0 = hz(note)
    n = per * M * over
    ph = np.arange(n) / n
    rng = np.random.default_rng(seed)
    a = np.zeros(n)
    for k, amp, shape, octv in voices:
        cyc = (M + k) * 2 ** octv
        p0 = rng.uniform(0, 2 * np.pi)
        for h in range(1, 80):
            if h * cyc * 2 > n * 0.45:
                break
            if shape == 'saw':
                g = 1 / h
            elif shape == 'sq':
                g = (1 / h) if h % 2 else 0
            else:                                    # puls 25%
                g = abs(np.sin(np.pi * h * 0.25)) / h
            a += amp * g * np.sin(2 * np.pi * h * cyc * ph + h * p0)
    a = np.tanh(drive * a / np.abs(a).max())
    F = np.fft.rfft(a)
    fr = np.arange(len(F)) * f0 / M
    F *= 1 / np.sqrt(1 + (fr / cut) ** 8)
    F[fr < 0.6 * f0] = 0
    F[fr < 1.5 * f0] *= sub_fund
    if mid_boost:
        c, gain = mid_boost
        F *= 1 + gain * np.exp(-((np.log2(np.maximum(fr, 1) / c)) / 0.6) ** 2)
    F = F[:per * M // 2 + 1]
    out = np.fft.irfft(F, per * M)
    return norm(out), int(round(f0 * per))


# ---------------------------------------------------------------- eenmalig
def svf(x, rate, fc, q):
    """Chamberlin state-variable lowpass met een cutoff per sample (resonant, 303-achtig)."""
    low = band = 0.0
    out = np.empty_like(x)
    damp = 1.0 / q
    for i in range(len(x)):
        f = 2 * np.sin(np.pi * min(fc[i], rate * 0.2) / rate)
        low += f * band
        high = x[i] - low - damp * band
        band += f * high
        out[i] = low
    return out


def acid(accent=False, rate=22050, dur=0.32):
    """303: zaagtand op C3, resonant lowpass met een snelle filterenvelope, verzadigd."""
    note = 48
    over = 2
    r2 = rate * over
    t = np.arange(int(r2 * dur)) / r2
    f = hz(note)
    x = np.zeros_like(t)
    for h in range(1, int(r2 * 0.45 / f)):
        x += np.sin(2 * np.pi * h * f * t) / h
    peak = 3600 if accent else 1700
    fc = 260 + peak * np.exp(-t / (0.09 if accent else 0.06))
    y = svf(x, r2, fc, 7.0 if accent else 4.5)
    y = np.tanh((3.2 if accent else 2.2) * norm(y))
    env = np.minimum(1, t / 0.002) * np.exp(-t / (0.22 if accent else 0.16))
    y = lp(y * env, r2, 6500)
    y = resample(y, r2, rate, antialias=True)
    return fade_out(norm(y), rate, 0.05), rate


def saw(f, t, phase=0.0, top_hz=7000):
    a = np.zeros_like(t)
    for h in range(1, int(top_hz / f) + 1):
        a += np.sin(2 * np.pi * h * f * t + h * phase) / h
    return a


def stab(rate=22050, dur=0.5):
    """Noisestoot: E-powerchord (E3 B3 E4), drie ontstemde zaagtanden per noot + ruis, filterenvelope, hard vervormd."""
    t = np.arange(int(rate * dur)) / rate
    rng = np.random.default_rng(3)
    a = np.zeros_like(t)
    for nt in (52, 59, 64):
        for c in (-14, 0, 13):
            a += saw(hz(nt) * 2 ** (c / 1200), t, rng.uniform(0, 6))
    a = norm(a) + 0.45 * rng.uniform(-1, 1, len(t)) * np.exp(-t / 0.05)
    fc = 700 + 5200 * np.exp(-t / 0.06)
    y = np.zeros_like(a)
    z = 0.0
    k = np.exp(-2 * np.pi * fc / rate)
    for _ in range(2):
        z = 0.0
        for i in range(len(a)):
            z = (1 - k[i]) * a[i] + k[i] * z
            y[i] = z
        a = y.copy()
    env = np.minimum(1, t / 0.002) * np.exp(-t / 0.16)
    a = np.tanh(3.0 * norm(a * env))
    a = lp(a, rate, 7000)
    return fade_out(norm(a), rate, 0.08), rate


def ohit(rate=22050):
    a = resample(render(55, [52, 59, 64, 67], 0.7, vel=127), 44100, rate, antialias=True)
    a = np.tanh(2.2 * norm(hp(a, rate, 90)))
    a = lp(a, rate, 6500)
    return fade_out(norm(a), rate, 0.2), rate


def cannon(rate=16000, dur=1.3):
    t = np.arange(int(rate * dur)) / rate
    rng = np.random.default_rng(21)
    # laserzap: zaagtand 2200 -> 160 Hz in 0,22 s
    fz = 160 + 2040 * np.exp(-t / 0.06)
    zap = np.sin(2 * np.pi * np.cumsum(fz) / rate)
    zap = np.sign(zap) * np.abs(zap) ** 0.3 * np.exp(-t / 0.09)
    # dreun 120 -> 32 Hz
    fb = 32 + 88 * np.exp(-t / 0.08)
    boom = np.sin(2 * np.pi * np.cumsum(fb) / rate) * np.exp(-t / 0.45)
    # explosie: ruis met dalend lowpass
    nz = rng.uniform(-1, 1, len(t))
    expl = lp(nz, rate, 2400) * np.exp(-t / 0.18) + 0.6 * lp(nz, rate, 500) * np.exp(-t / 0.5)
    a = 0.55 * zap + 1.3 * boom + 0.9 * norm(expl)
    a = np.tanh(2.5 * norm(a))
    a = lp(a, rate, 6000)
    return fade_out(norm(a), rate, 0.35), rate


# ---------------------------------------------------------------- drums
def kick(rate=16000, dur=0.3):
    n = int(rate * dur)
    t = np.arange(n) / rate
    f = 46 + 130 * np.exp(-t / 0.028)
    body = np.sin(2 * np.pi * np.cumsum(f) / rate) * np.exp(-t / 0.14)
    click = bp(np.random.default_rng(9).uniform(-1, 1, n), rate, 1500, 5000) * np.exp(-t / 0.004)
    fl = resample(render(0, [36], dur, kit=16, vel=127), 44100, rate, antialias=True)[:n]
    fl = np.pad(fl, (0, n - len(fl)))
    a = np.tanh(3.0 * (body + 1.1 * click + 0.3 * norm(fl)))      # hard: big beat = gecomprimeerd
    return fade_out(norm(a), rate, 0.05), rate


def rumble(rate=12000, dur=0.24):
    """Hard-techno-rumble: de kick door een galmstaart (ruisconvolutie), vervormd en lowpass; alleen de staart."""
    k, kr = kick(rate=rate, dur=0.3)
    rng = np.random.default_rng(17)
    tail = rng.uniform(-1, 1, int(rate * 0.7)) * np.exp(-np.arange(int(rate * 0.7)) / rate / 0.25)
    w = np.convolve(k, tail)[:int(rate * 0.9)]
    w = lp(w, rate, 180)
    w = np.tanh(4.0 * norm(w))
    w = lp(w, rate, 420)
    s = int(rate * 0.06)
    a = w[s:s + int(rate * dur)]
    t = np.arange(len(a)) / rate
    a = a * np.minimum(1, t / 0.006) * np.exp(-t / 0.09)
    return fade_out(norm(a), rate, 0.06), rate


def snare(rate=22050, dur=0.3, ghost=False):
    n = int(rate * dur)
    t = np.arange(n) / rate
    fl = resample(0.7 * render(0, [38], dur, kit=0, vel=127) + 0.6 * render(0, [38], dur, kit=8, vel=127)
                  + 0.4 * render(0, [40], dur, kit=0, vel=127), 44100, rate, antialias=True)[:n]
    fl = np.pad(fl, (0, n - len(fl)))
    nz = np.random.default_rng(5).uniform(-1, 1, n)
    crack = bp(nz, rate, 1500, 7000) * np.exp(-t / 0.07)
    body = np.sin(2 * np.pi * 185 * t) * np.exp(-t / 0.04)
    a = norm(fl) + 1.5 * norm(crack) + 0.5 * body
    a = hp(a, rate, 150)
    a = np.tanh(4.5 * norm(a))                     # hard gecomprimeerd (big beat)
    a = lp(a, rate, 7800)
    if ghost:
        a = a[:int(rate * 0.09)]
        return fade_out(norm(a), rate, 0.05), rate
    return fade_out(norm(a), rate, 0.1), rate


def hat(rate=18000, open_=False):
    dur = 0.3 if open_ else 0.055
    n = int(rate * dur)
    t = np.arange(n) / rate
    x = np.zeros(n)
    for f in (205.3, 304.4, 369.6, 522.7, 540.0, 800.0):          # 808-verhoudingen x2: metaal
        x += np.sign(np.sin(2 * np.pi * 2 * f * t + f))
    fl = resample(render(0, [46 if open_ else 42], dur, kit=0, vel=120), 44100, rate, antialias=True)[:n]
    fl = np.pad(fl, (0, n - len(fl)))
    a = 0.8 * norm(bp(x, rate, 5000, 8500)) + norm(hp(fl, rate, 4000))
    a = a * np.exp(-t / (0.1 if open_ else 0.016)) * np.minimum(1, t / 0.0008)
    a = lp(np.tanh(2.0 * norm(a)), rate, 8200)
    return fade_out(norm(a), rate, 0.08 if open_ else 0.012), rate


def metal(f0, dur, t60s, rate=22050, ratios=(1.0, 2.32, 4.25, 6.63, 9.38), seed=31):
    """Aambeeld/buis: inharmonische partialen met elk een eigen uitsterftijd + een harde aanslag."""
    t = np.arange(int(rate * dur)) / rate
    rng = np.random.default_rng(seed)
    a = np.zeros_like(t)
    for r, t60 in zip(ratios, t60s):
        if f0 * r > 0.42 * rate:
            continue
        for d in (1.0, 1.004):                                       # licht ontstemd paar: zweving
            a += np.sin(2 * np.pi * f0 * r * d * t + rng.uniform(0, 6)) * np.exp(-t * 6.9 / t60) / (r ** 0.35)
    hit = bp(rng.uniform(-1, 1, len(t)), rate, 1200, 6000) * np.exp(-t / 0.005)
    a = norm(a) + 0.7 * hit
    a = lp(np.tanh(1.6 * norm(a)), rate, 7800)
    return fade_out(norm(a), rate, 0.1), rate


def press(rate=16000, dur=0.42):
    """Machinepers: dreun + metalen klank + perslucht ('tssh') die erachteraan wegblaast."""
    t = np.arange(int(rate * dur)) / rate
    rng = np.random.default_rng(41)
    thud = np.sin(2 * np.pi * np.cumsum(70 + 60 * np.exp(-t / 0.02)) / rate) * np.exp(-t / 0.06)
    clank, _ = metal(330, dur, (0.25, 0.18, 0.12, 0.08, 0.05), rate=rate, seed=43)
    hiss = bp(rng.uniform(-1, 1, len(t)), rate, 1800, 6500)
    henv = np.clip((t - 0.05) / 0.02, 0, 1) * np.exp(-np.maximum(0, t - 0.07) / 0.09)
    a = 1.2 * thud + 0.8 * clank + 0.6 * norm(hiss) * henv
    a = lp(np.tanh(2.2 * norm(a)), rate, 7000)
    return fade_out(norm(a), rate, 0.08), rate


def revcym(rate=16000):
    a = resample(render(0, [49], 1.4, kit=0, vel=120), 44100, rate, antialias=True)
    a = lp(norm(a), rate, 7000)[::-1].copy()
    t = np.arange(len(a)) / rate
    a *= np.minimum(1, t / 0.2)
    a[-int(rate * 0.012):] *= np.linspace(1, 0, int(rate * 0.012))
    return norm(a), rate


# ---------------------------------------------------------------- v2
def istab(rate=22050, dur=0.42):
    """Industriële stoot: E3-Bb3-E4 (tritonus) van ontstemde zaagtanden + metaalruis, snelle filterenvelope, tanh x5."""
    t = np.arange(int(rate * dur)) / rate
    rng = np.random.default_rng(41)
    a = np.zeros_like(t)
    for nt in (52, 58, 64):
        for c in (-18, 0, 17):
            a += saw(hz(nt) * 2 ** (c / 1200), t, rng.uniform(0, 6))
    nz = bp(rng.uniform(-1, 1, len(t)), rate, 2500, 6500) * np.exp(-t / 0.03)
    a = norm(a) + 0.6 * norm(nz)
    a = 0.5 * lp(a, rate, 1200) + 0.5 * a * np.exp(-t / 0.05)          # filter klapt dicht na de aanslag
    env = np.minimum(1, t / 0.0015) * np.exp(-t / 0.11)
    a = np.tanh(5.0 * norm(a * env))
    a = lp(a, rate, 6500)
    return fade_out(norm(a), rate, 0.06), rate


def kick2(rate=16000, dur=0.34):
    n = int(rate * dur)
    t = np.arange(n) / rate
    f = 44 + 146 * np.exp(-t / 0.032)
    body = np.sin(2 * np.pi * np.cumsum(f) / rate) * np.exp(-t / 0.19)
    click = bp(np.random.default_rng(19).uniform(-1, 1, n), rate, 1800, 5500) * np.exp(-t / 0.005)
    a = np.tanh(5.0 * (body + 1.2 * click))
    a = lp(a, rate, 5000)
    return fade_out(norm(a), rate, 0.06), rate


def snare2(rate=22050, dur=0.26, short=False):
    n = int(rate * dur)
    t = np.arange(n) / rate
    fl = resample(0.7 * render(0, [38], dur, kit=16, vel=127) + 0.6 * render(0, [39], dur, kit=24, vel=127)
                  + 0.4 * render(0, [40], dur, kit=0, vel=127), 44100, rate, antialias=True)[:n]
    fl = np.pad(fl, (0, n - len(fl)))
    nz = np.random.default_rng(23).uniform(-1, 1, n)
    crack = bp(nz, rate, 1800, 6500) * np.exp(-t / 0.06)
    body = np.sin(2 * np.pi * 210 * t) * np.exp(-t / 0.03)
    a = norm(fl) + 1.8 * norm(crack) + 0.6 * body
    a = hp(a, rate, 160)
    a = np.tanh(7.0 * norm(a))
    a = lp(a, rate, 7500)
    if short:
        return fade_out(norm(a[:int(rate * 0.07)]), rate, 0.03), rate
    return fade_out(norm(a), rate, 0.08), rate


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    jobs = {}
    # bas op E2 (40): 128 samples per periode (10,5 kHz), 64 perioden per loop (±0,78 s, zweving ±1,3 Hz)
    bv = [(-1, 1.0, 'saw', 0), (1, 1.0, 'saw', 0), (0, 0.35, 'sq', -1)]
    a, r = periodic(40, 128, 64, bv, 3.0, 2800.0, sub_fund=0.5, mid_boost=(900, 0.9))
    jobs['genesect_bass'] = (a, r, 40, (0, len(a)))
    a, r = periodic(40, 128, 64, bv, 2.2, 900.0, sub_fund=0.6)
    jobs['genesect_bass_dark'] = (a, r, 40, (0, len(a)))
    # lead op C5 (72): 32 samples per periode (16,7 kHz), 128 perioden per loop
    a, r = periodic(72, 32, 128, [(-2, 0.9, 'saw', 0), (0, 0.8, 'pulse', 0), (2, 0.9, 'saw', 0), (0, 0.5, 'sq', -1)],
                    2.4, 5600.0)
    jobs['genesect_lead'] = (a, r, 72, (0, len(a)))
    a, r = acid(False); jobs['genesect_acid'] = (a, r, 48, None)
    a, r = acid(True); jobs['genesect_acid_acc'] = (a, r, 48, None)
    a, r = stab(); jobs['genesect_stab'] = (a, r, 52, None)
    a, r = ohit(); jobs['genesect_ohit'] = (a, r, 64, None)
    a, r = cannon(); jobs['genesect_cannon'] = (a, r, 60, None)
    a, r = kick(); jobs['genesect_kick'] = (a, r, 60, None)
    a, r = rumble(); jobs['genesect_rumble'] = (a, r, 60, None)
    a, r = snare(); jobs['genesect_snare'] = (a, r, 60, None)
    a, r = snare(ghost=True); jobs['genesect_ghost'] = (a, r, 60, None)
    a, r = hat(); jobs['genesect_hat'] = (a, r, 60, None)
    a, r = hat(open_=True); jobs['genesect_ohat'] = (a, r, 60, None)
    a, r = metal(620, 0.7, (0.7, 0.45, 0.3, 0.18, 0.1)); jobs['genesect_anvil'] = (a, r, 60, None)
    a, r = metal(190, 1.0, (1.0, 0.7, 0.45, 0.3, 0.2), rate=16000, ratios=(1.0, 2.76, 5.4, 8.93, 13.3), seed=37)
    jobs['genesect_pipe'] = (a, r, 60, None)
    a, r = press(); jobs['genesect_press'] = (a, r, 60, None)
    a, r = revcym(); jobs['genesect_revcym'] = (a, r, 60, None)
    # v2
    a, r = periodic(40, 128, 64, [(-1, 1.0, 'saw', 0), (1, 0.9, 'sq', 0), (0, 0.4, 'sq', -1)], 6.0, 3200.0,
                    sub_fund=0.45, mid_boost=(1200, 1.4), seed=29)
    jobs['genesect_dbass'] = (a, r, 40, (0, len(a)))
    a, r = istab(); jobs['genesect_istab'] = (a, r, 52, None)
    a, r = kick2(); jobs['genesect_kick2'] = (a, r, 60, None)
    a, r = snare2(); jobs['genesect_snare2'] = (a, r, 60, None)
    a, r = snare2(short=True); jobs['genesect_roll2'] = (a, r, 60, None)
    for name, (a, rate, key, loop) in jobs.items():
        write_wav(OUT + name + '.wav', a, rate, key, loop)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-20s %6d samples @ %5d Hz, grondtoon %d%s' % (name, len(a), rate, key, ', loop' if loop else ''))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()

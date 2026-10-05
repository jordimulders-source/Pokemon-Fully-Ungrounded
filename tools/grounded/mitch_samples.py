#!/usr/bin/env python3
"""Project Grounded: de Drum & Bass-samples voor Battle! Mitch (mitch_theme.py). Eigen generator (gm_samples.py en
heatran_samples.py blijven ongemoeid; alleen hulpfuncties worden geïmporteerd).

Gesynthetiseerd, met een exacte loop (M perioden van de grondtoon per loop; zaagtand k heeft precies M + k
trillingen per loop, zodat de zweving in de sample zit en hij naadloos rondloopt):
  mitch_reese_dark / _mid / _bright : reese = twee licht ontstemde zaagtanden + een beetje sub, door een resonant
      lowpassfilter (dicht -> open). Het spoor wisselt per noot van sample = filterbeweging, 'pratende' bas.
  mitch_growl  : dezelfde reese door twee formanten ('wow') en extra saturatie: het neurofunk-gegrom.
  mitch_wob_<noot> : wobble-bas: reese met een filter-LFO die in de sample zit, twee maten lang (op 174 bpm):
      maat 1 = kwarten, kwarten, achtsten, zestienden; maat 2 = halve noot open, achtsten, triolen. Per grondtoon
      een eigen sample, zodat de wobble precies op het tempo blijft (een getransponeerde sample zou versnellen).
  mitch_stab_min / _maj : synthstoot (drie ontstemde zaagtanden per akkoordnoot, filterenvelope), 1 kanaal/akkoord.
  mitch_lead   : twee ontstemde zaagtanden op C5 (32 samples per periode), voor de hook in de tweede helft.
  mitch_rewind : DJ-rewind: een stukje van de drop (kick, snare, reese, stoot) achterstevoren, eerst snel
      versnellend en dan uitlopend, eenmalig.
  mitch_airhorn: MC-luchthoorn (twee zaagtanden in een kleine secunde, bandpass, vervormd), eenmalig.
  mitch_reese_raw / _raw_dark (v2): rauwe distorted reese: vijf ontstemde zaagtanden, tanh-fuzz op 8x de samplerate,
      periodiek FFT-lowpass ±2,5 kHz (dark: 1,1 kHz), grondtoon zachter (de PSG-sub draagt het laag), +5 dB rond 1,1 kHz.
Drums v2 (Jordi: 'te recht/langzaam, mist de agressieve DnB-fundering'):
  mitch_kick   : sinus 190 -> 52 Hz (snelle val) + klik 2-5,5 kHz + een beetje FluidR3-elektronische kick, verzadigd.
  mitch_snare  : FluidR3 standard 38 + electric 40, ruisstoot 1,8-6,5 kHz (crack) + toon 190 Hz, hard verzadigd.
  mitch_ghost  : dezelfde snare, 90 ms (ghost notes en roffels).
  mitch_hat / mitch_ohat : FluidR3-hihat (42/46) + ruis > 6 kHz, gesloten 60 ms (16den op 174 bpm), open 0,32 s.
Uit FluidR3 (fluidsynth, kit/programma per sample) en daarna bewerkt:
  mitch_revcym : crash achterstevoren (aanloop naar een drop).
  mitch_ride   : ride (Standard-kit), voor de Pendulum-achtige ride in de drops.
  mitch_horn_min / _maj : brass section (GM 61) als akkoord in één sample (hoornstoot).
  mitch_pad_min / _maj  : warme pad (GM 89) als akkoord in één sample, gecrossfade loop.
v3 (Jordi: 'te veel drukke chiptune/happy hardcore; duistere Chase & Status-DnB, less is more', 172 bpm):
  mitch3_kick  : hele korte, felle punch: sinus 230 -> 58 Hz in ±20 ms (het laag-midden), dreun van 60 ms, klik.
  mitch3_snare : droge, keiharde klap: FluidR3-snare (38) + handklap (39) + ruisstoot 1,5-7 kHz, kort (0,19 s).
  mitch3_ghost : dezelfde snare, 70 ms (ghost notes).
  mitch3_brass_lo / _hi : koperstoot in octaven (FluidR3 brass section 61 + synth brass 62, twee noten in één
      sample = 1 kanaal), licht vervormd; lo op F3 (F2+F3), hi op Eb4 (Eb3+Eb4).
  mitch3_pluck : donkere synthpluk (twee ontstemde zaagtanden, filterenvelope dicht), voor de arpeggio's.
  mitch3_wob_<noot> : wobble op 172 bpm (de 'lagere synths' van v2 rond 1:00), trager en dreigender LFO-patroon.
Labels achteraan sound/direct_sound_data.inc (na .align 2).
Gebruik: python3 tools/grounded/mitch_samples.py"""
import os, subprocess, sys, tempfile, wave
import numpy as np
import mido
from scipy.signal import butter, sosfilt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import resample, auto_loop, write_wav

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
BPM = 174
BEAT = 60 / BPM


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
    return a[s:s + int(dur * 44100)]


def norm(a, peak=0.97):
    return a / max(1e-9, np.abs(a).max()) * peak


def fade_out(a, rate, sec):
    n = min(len(a), int(rate * sec))
    a = a.copy()
    a[-n:] *= np.linspace(1, 0, n) ** 2
    return a


# ---------------------------------------------------------------- bas (additief, exacte loop)
def lp_gain(h, fc, res=0.0, formants=()):
    """Resonant 4-polig-achtig lowpass in harmonischen + optionele formanten (h_center, breedte, versterking)."""
    if fc is None:
        g = 1.0
    else:
        g = 1 / np.sqrt(1 + (h / fc) ** 8) * (1 + res * np.exp(-((h - fc) / np.maximum(1.0, 0.25 * fc)) ** 2))
    for c, w, a in formants:
        g = g * (1 + a * np.exp(-((h - c) / w) ** 2))
    return g


def reese(note, per, M, fc, res=0.8, sub=0.15, drive=1.6, formants=(), top=48, detune=((-1, 1.0), (1, 1.0)), lfo=None,
          seed=7, fund=1.0):
    """lfo: functie fase (0..1 over de hele loop) -> filterfrequentie in harmonischen (voor de wobble)."""
    f0 = hz(note)
    rate = int(round(f0 * per))
    n = per * M
    ph = np.arange(n) / n                       # 0..1 over de loop
    rng = np.random.default_rng(seed)
    a = np.zeros(n)
    nyq = 0.45 * n
    fcs = lfo(ph) if lfo else None
    for k, amp in detune:
        cyc = M + k
        p0 = rng.uniform(0, 2 * np.pi)
        for h in range(1, top + 1):
            if h * cyc >= nyq:
                break
            g = lp_gain(h, fcs if lfo else fc, res, formants) * (fund if h == 1 else 1.0)
            a += amp * g * np.sin(2 * np.pi * h * cyc * ph + h * p0) / h
    if sub:
        a += sub * np.abs(a).max() * np.sin(2 * np.pi * M * ph)
    a = np.tanh(drive * a / np.abs(a).max())
    return norm(a), rate


def wob_lfo(bars=2):
    """Filterfrequentie (harmonischen) over twee maten: maat 1 kwart, kwart, 8sten, 16den; maat 2 half open, 8sten,
    triolen. Elke wobble begint dicht (geen klik bij de herhaling)."""
    segs = [(0, 1, 1), (1, 1, 1), (2, 1, 2), (3, 1, 4), (4, 2, 0.5), (6, 1, 2), (7, 1, 3)]   # (tel, tellen, per tel)
    beats = 4 * bars

    def f(ph):
        b = ph * beats
        out = np.full_like(ph, 1.5)
        for st, ln, r in segs:
            m = (b >= st) & (b < st + ln)
            x = (b[m] - st) * r
            out[m] = 1.5 + 22 * (0.5 - 0.5 * np.cos(2 * np.pi * x)) ** 1.5
        return out
    return f


# ---------------------------------------------------------------- stoten en lead (tijddomein)
def saw(f, t, phase=0.0, top_hz=6000):
    a = np.zeros_like(t)
    for h in range(1, int(top_hz / f) + 1):
        a += np.sin(2 * np.pi * h * f * t + h * phase) / h
    return a


def stab(notes, rate=22050, dur=0.42):
    t = np.arange(int(rate * dur)) / rate
    a = np.zeros_like(t)
    rng = np.random.default_rng(3)
    for n in notes:
        for c in (-12, 0, 11):                   # drie stemmen, ±12 cent
            a += saw(hz(n) * 2 ** (c / 1200), t, rng.uniform(0, 6), top_hz=7000)
    # filterenvelope: open -> dicht (tijdvariant eenpolig, twee keer)
    fc = 600 + 5200 * np.exp(-t / 0.07)
    y = np.zeros_like(a)
    for _ in range(2):
        z, out = 0.0, np.empty_like(a)
        k = np.exp(-2 * np.pi * fc / rate)
        for i in range(len(a)):
            z = (1 - k[i]) * a[i] + k[i] * z
            out[i] = z
        a = out
    env = np.minimum(1, t / 0.003) * np.exp(-t / 0.14)
    a = np.tanh(1.8 * norm(a * env))
    return fade_out(norm(a), rate, 0.06), rate


def rewind(parts, rate=16000):
    """parts: {naam: (signaal, samplerate)}. Twee tellen 'drop' mixen en die achterstevoren afspelen met een
    snelheid die snel oploopt (de hand trekt de plaat terug) en dan uitloopt."""
    beat = int(rate * BEAT)
    mix = np.zeros(beat * 4 + rate)

    def put(name, at, gain=1.0, ln=None):
        s, r = parts[name]
        s = resample(s, r, rate, antialias=True)
        if ln:
            s = s[:ln]
        mix[at:at + len(s)] += gain * s[:len(mix) - at]
    for k0 in (0, 2):
        put('kick', k0 * beat); put('snare', (k0 + 1) * beat, 0.9); put('kick', int((k0 + 1.5) * beat), 0.8)
    put('reese', 0, 0.8, beat * 4); put('stab', int(beat * 0.75), 0.6); put('stab', int(beat * 2.75), 0.6)
    mix = norm(mix[:beat * 4])
    dur = 1.05
    t = np.arange(int(rate * dur)) / rate
    speed = 0.15 + 2.6 * np.sin(np.pi * np.minimum(1, t / dur)) ** 1.3 * np.exp(-t / 1.2)       # ±1 maat materiaal
    pos = len(mix) - 1 - np.cumsum(speed)
    pos = np.clip(pos, 0, len(mix) - 1)
    a = np.interp(pos, np.arange(len(mix)), mix)
    a *= np.minimum(1, t / 0.01) * np.minimum(1, (dur - t) / 0.12)
    return norm(sosfilt(butter(2, 4500, 'lowpass', fs=rate, output='sos'), a)), rate


def airhorn(rate=22050, dur=0.7):
    t = np.arange(int(rate * dur)) / rate
    f = 460 * (1 - 0.03 * np.minimum(1, t / 0.25))
    ph = 2 * np.pi * np.cumsum(f) / rate
    a = np.zeros_like(t)
    for ratio in (1.0, 1.06, 1.5):
        for h in range(1, 14):
            a += np.sin(h * ratio * ph) / h ** 0.8
    a = sosfilt(butter(2, [450, 3200], 'bandpass', fs=rate, output='sos'), a)
    a = np.tanh(3 * norm(a))
    env = np.minimum(1, t / 0.008)
    return fade_out(norm(a * env), rate, 0.1), rate


# ---------------------------------------------------------------- drums (FluidR3 + bewerking)
def kick(rate=16000):
    a = resample(render(0, [36], 0.35, kit=16, vel=127), 44100, rate, antialias=True)
    t = np.arange(len(a)) / rate
    f = 48 + 62 * np.exp(-t / 0.03)
    thump = np.sin(2 * np.pi * np.cumsum(f) / rate) * np.exp(-t / 0.13)
    click = sosfilt(butter(2, [1800, 5000], 'bandpass', fs=rate, output='sos'),
                    np.random.default_rng(9).uniform(-1, 1, len(t))) * np.exp(-t / 0.006)
    a = np.tanh(2.0 * (0.8 * norm(a) + thump + 1.2 * click))
    return fade_out(norm(a), rate, 0.05), rate


def snare(rate=22050, dur=0.32, ghost=False):
    a = resample(render(0, [38], dur, kit=8, vel=127), 44100, rate, antialias=True)
    t = np.arange(len(a)) / rate
    a = norm(a) + 0.6 * np.random.default_rng(5).uniform(-1, 1, len(a)) * np.exp(-t / 0.03)
    a = sosfilt(butter(2, 230, 'highpass', fs=rate, output='sos'), a)
    a = np.tanh(3.0 * norm(a))
    if ghost:
        a = a[:int(rate * 0.13)]
        return fade_out(norm(a), rate, 0.07), rate
    return fade_out(norm(a), rate, 0.08), rate


def revcym(rate=16000):
    a = resample(render(0, [49], 1.6, kit=0, vel=120), 44100, rate, antialias=True)
    a = norm(a)[::-1].copy()
    t = np.arange(len(a)) / rate
    a *= np.minimum(1, t / 0.2)
    a[-int(rate * 0.012):] *= np.linspace(1, 0, int(rate * 0.012))
    return norm(a), rate


def gm_chord(prog, notes, dur, rate, loop):
    a = resample(render(prog, notes, dur + (0.6 if loop else 0), vel=118), 44100, rate, antialias=True)
    a = norm(sosfilt(butter(2, 140, 'highpass', fs=rate, output='sos'), a))
    if loop:
        a, lp = auto_loop(a, rate)
        return norm(a), rate, lp
    return fade_out(a, rate, 0.08), rate, None


# ---------------------------------------------------------------- v2: rauwe reese, punchy kit
def reese_raw(note=36, per=128, M=128, cut=2500.0, drive=3.2, saws=((-2, 0.7), (-1, 1.0), (0, 0.8), (1, 1.0), (2, 0.7)),
              fund=0.55, over=8):
    """Rauwe distorted reese: vijf licht ontstemde zaagtanden (M + k trillingen per loop: zweving 0,5-1 Hz in de
    sample), vervormd (tanh) op 8x de samplerate en daarna met een periodiek FFT-lowpass (±cut Hz, 24 dB/oct)
    teruggebracht naar `per` samples per periode: geen aliasing en een exacte loop."""
    f0 = hz(note)
    n = per * M * over
    ph = np.arange(n) / n
    rng = np.random.default_rng(11)
    a = np.zeros(n)
    for k, amp in saws:
        cyc = M + k
        p0 = rng.uniform(0, 2 * np.pi)
        for h in range(1, 60):
            g = fund if h == 1 else 1.0
            a += amp * g * np.sin(2 * np.pi * h * cyc * ph + h * p0) / h
    a = np.tanh(drive * a / np.abs(a).max())
    F = np.fft.rfft(a)
    fr = np.arange(len(F)) * f0 / M                    # bin k = k / M x f0
    F *= 1 / np.sqrt(1 + (fr / cut) ** 8)
    F[fr < 0.6 * f0] = 0                               # geen DC/infrasoon
    F[fr < 1.5 * f0] *= 0.4                            # grondtoon zachter: de PSG-sub draagt het laag
    F *= 1 + 0.8 * np.exp(-((np.log2(np.maximum(fr, 1) / 1100)) / 0.6) ** 2)    # +5 dB rond 1,1 kHz: grit
    F = F[:per * M // 2 + 1]
    out = np.fft.irfft(F, per * M)
    return norm(out), int(round(f0 * per))


def kick2(rate=16000):
    """Strakke DnB-kick: sinus met snelle toonhoogteval (190 -> 52 Hz), korte dreun, klik 2-5 kHz, verzadigd."""
    n = int(rate * 0.24)
    t = np.arange(n) / rate
    f = 52 + 138 * np.exp(-t / 0.022)
    body = np.sin(2 * np.pi * np.cumsum(f) / rate) * np.exp(-t / 0.10)
    click = sosfilt(butter(2, [2000, 5500], 'bandpass', fs=rate, output='sos'),
                    np.random.default_rng(9).uniform(-1, 1, n)) * np.exp(-t / 0.004)
    fl = resample(render(0, [36], 0.24, kit=24, vel=127), 44100, rate, antialias=True)[:n]
    fl = np.pad(fl, (0, n - len(fl)))
    a = np.tanh(2.4 * (body + 1.4 * click + 0.35 * norm(fl)))
    return fade_out(norm(a), rate, 0.04), rate


def snare2(rate=22050, dur=0.24, ghost=False):
    """Snare met crack: FluidR3 (standard-kit 38 + electric 40) + ruisstoot 1,8-6 kHz + toon 190 Hz, hooggefilterd."""
    n = int(rate * dur)
    t = np.arange(n) / rate
    m = int(dur * 44100)
    two = [np.pad(x[:m], (0, m - len(x[:m]))) for x in (render(0, [38], dur, kit=0, vel=127), render(0, [40], dur, kit=0, vel=127))]
    fl = resample(0.6 * two[0] + 0.6 * two[1], 44100, rate, antialias=True)[:n]
    fl = np.pad(fl, (0, n - len(fl)))
    noise = np.random.default_rng(5).uniform(-1, 1, n)
    crack = sosfilt(butter(2, [1800, 6500], 'bandpass', fs=rate, output='sos'), noise) * np.exp(-t / 0.045)
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.035)
    a = norm(fl) + 1.3 * norm(crack) + 0.5 * body
    a = sosfilt(butter(2, 160, 'highpass', fs=rate, output='sos'), a)
    a = np.tanh(4.0 * norm(a))                         # hard: de crack moet boven de trompet uit
    if ghost:
        a = a[:int(rate * 0.09)]
        return fade_out(norm(a), rate, 0.05), rate
    return fade_out(norm(a), rate, 0.07), rate


def hat(rate=22050, open_=False):
    """Hihat: FluidR3 (gesloten 42 / open 46) + ruis boven 6 kHz; kort en helder (16den op 174 bpm = 86 ms)."""
    dur = 0.32 if open_ else 0.06
    n = int(rate * dur)
    t = np.arange(n) / rate
    fl = resample(render(0, [46 if open_ else 42], dur, kit=0, vel=120), 44100, rate, antialias=True)[:n]
    fl = np.pad(fl, (0, n - len(fl)))
    nz = sosfilt(butter(2, 6500, 'highpass', fs=rate, output='sos'), np.random.default_rng(13).uniform(-1, 1, n))
    a = norm(fl) + 0.8 * norm(nz) * np.exp(-t / (0.12 if open_ else 0.018))
    a = sosfilt(butter(2, 4500, 'highpass', fs=rate, output='sos'), a)
    a = np.tanh(2.5 * norm(a))
    return fade_out(norm(a), rate, 0.1 if open_ else 0.015), rate


# ---------------------------------------------------------------- v3: droog, laag, duister (172 bpm)
BPM3 = 172
BEAT3 = 60 / BPM3


def wob_lfo3(bars=2):
    """v3: dreigender: maat 1 halve noot (langzaam open), kwart, achtsten; maat 2 kwarten, achtsten, triolen."""
    segs = [(0, 2, 0.5), (2, 1, 1), (3, 1, 2), (4, 1, 1), (5, 1, 1), (6, 1, 2), (7, 1, 3)]
    beats = 4 * bars

    def f(ph):
        b = ph * beats
        out = np.full_like(ph, 1.5)
        for st, ln, r in segs:
            m = (b >= st) & (b < st + ln)
            x = (b[m] - st) * r
            out[m] = 1.5 + 16 * (0.5 - 0.5 * np.cos(2 * np.pi * x)) ** 1.6
        return out
    return f


def kick3(rate=16000):
    """Korte, felle DnB-kick: de punch zit in de snelle toonhoogteval 230 -> 58 Hz (laag-midden), korte dreun."""
    n = int(rate * 0.16)
    t = np.arange(n) / rate
    f = 58 + 172 * np.exp(-t / 0.016)
    body = np.sin(2 * np.pi * np.cumsum(f) / rate) * np.exp(-t / 0.06)
    click = sosfilt(butter(2, [1500, 5000], 'bandpass', fs=rate, output='sos'),
                    np.random.default_rng(19).uniform(-1, 1, n)) * np.exp(-t / 0.003)
    a = np.tanh(2.8 * (body + 1.0 * click))
    return fade_out(norm(a), rate, 0.03), rate


def snare3(rate=22050, dur=0.19, ghost=False):
    """Droge, harde klap: FluidR3-snare + handklap, ruisstoot 1,5-7 kHz, toon 185 Hz, hard verzadigd en kort."""
    n = int(rate * dur)
    t = np.arange(n) / rate
    m = int(dur * 44100)
    two = [np.pad(x[:m], (0, m - len(x[:m]))) for x in (render(0, [38], dur, kit=0, vel=127), render(0, [39], dur, kit=0, vel=127))]
    fl = resample(0.7 * two[0] + 0.6 * two[1], 44100, rate, antialias=True)[:n]
    fl = np.pad(fl, (0, n - len(fl)))
    noise = np.random.default_rng(23).uniform(-1, 1, n)
    crack = sosfilt(butter(2, [1500, 7000], 'bandpass', fs=rate, output='sos'), noise) * np.exp(-t / 0.035)
    body = np.sin(2 * np.pi * 185 * t) * np.exp(-t / 0.028)
    a = norm(fl) + 1.4 * norm(crack) + 0.6 * body
    a = sosfilt(butter(2, 170, 'highpass', fs=rate, output='sos'), a)
    a = np.tanh(4.5 * norm(a)) * np.exp(-np.maximum(0, t - 0.06) / 0.05)      # droog: na 60 ms snel weg
    if ghost:
        a = a[:int(rate * 0.07)]
        return fade_out(norm(a), rate, 0.04), rate
    return fade_out(norm(a), rate, 0.05), rate


def brass3(notes, key, rate=22050, dur=0.34):
    """Koperstoot in octaven: brass section (61) + synth brass (62) samen, licht vervormd, korte staart."""
    m = int(dur * 44100)
    parts = [render(p, notes, dur, vel=124) for p in (61, 62)]
    a = sum(np.pad(x[:m], (0, m - len(x[:m]))) * g for x, g in zip(parts, (1.0, 0.6)))
    a = resample(a, 44100, rate, antialias=True)
    a = sosfilt(butter(2, 110, 'highpass', fs=rate, output='sos'), a)
    a = np.tanh(1.8 * norm(a))
    t = np.arange(len(a)) / rate
    a *= np.exp(-np.maximum(0, t - 0.12) / 0.09)
    return fade_out(norm(a), rate, 0.05), rate


def pluck3(rate=22050, dur=0.3):
    """Donkere pluk op C4: twee ontstemde zaagtanden, lowpass-envelope 2,4 kHz -> 350 Hz."""
    t = np.arange(int(rate * dur)) / rate
    a = saw(hz(60) * 2 ** (-8 / 1200), t, 0.3, 6000) + saw(hz(60) * 2 ** (8 / 1200), t, 2.1, 6000)
    fc = 350 + 2100 * np.exp(-t / 0.045)
    for _ in range(2):
        z, out = 0.0, np.empty_like(a)
        k = np.exp(-2 * np.pi * fc / rate)
        for i in range(len(a)):
            z = (1 - k[i]) * a[i] + k[i] * z
            out[i] = z
        a = out
    a = np.tanh(1.5 * norm(a * np.minimum(1, t / 0.002) * np.exp(-t / 0.11)))
    return fade_out(norm(a), rate, 0.05), rate


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    jobs = {}           # naam -> (signaal, rate, grondtoon, loop)
    # reese: grondtoon C2 (36), 128 samples per periode (8372 Hz), loop 128 perioden (±1,96 s, zweving ±0,5 Hz)
    for name, fc, res, fm in (('dark', 4.0, 0.6, ()), ('mid', 9.0, 0.9, ((7, 3, 1.5),)), ('bright', 20.0, 0.7, ((9, 4, 2.0),))):
        a, r = reese(36, 128, 128, fc, res, formants=fm, sub=0.15 if name == 'dark' else 0.0, fund=1.0 if name == 'dark' else 0.45)
        jobs['mitch_reese_' + name] = (a, r, 36, (0, len(a)))
    a, r = reese(36, 128, 128, 14.0, 0.5, drive=2.6, formants=((10, 3, 4.0), (19, 4, 3.0)), detune=((-1, 1.0), (2, 0.9)), sub=0.0, fund=0.45)
    jobs['mitch_growl'] = (a, r, 36, (0, len(a)))
    # wobble: twee maten per loop; M = aantal perioden in twee maten (afgerond: < 0,4% tempoverschil)
    for nm, note in (('f1', 29), ('ab1', 32), ('c2', 36), ('db2', 37), ('eb2', 39)):
        M = int(round(8 * BEAT * hz(note)))
        per = 96 if note >= 36 else 128
        a, r = reese(note, per, M, None, 0.9, sub=0.0, fund=0.5, drive=2.0, lfo=wob_lfo(), top=40, formants=((8, 4, 3.5),))
        jobs['mitch_wob_' + nm] = (a, r, note, (0, len(a)))
    a, r = reese(72, 32, 128, None, 0, sub=0, drive=1.2, top=13, detune=((-1, 1.0), (1, 0.9)))
    jobs['mitch_lead'] = (a, r, 72, (0, len(a)))
    a, r = stab([60, 63, 67, 72])
    jobs['mitch_stab_min'] = (a, r, 60, None)
    a, r = stab([60, 64, 67, 72])
    jobs['mitch_stab_maj'] = (a, r, 60, None)
    for nm, notes in (('min', [60, 63, 67]), ('maj', [60, 64, 67])):
        a, r, lp = gm_chord(61, notes, 0.5, 22050, False)
        jobs['mitch_horn_' + nm] = (a, r, 60, lp)
        a, r, lp = gm_chord(89, notes, 2.0, 16000, True)
        jobs['mitch_pad_' + nm] = (a, r, 60, lp)
    k, kr = kick2()
    s, sr = snare2()
    jobs['mitch_kick'] = (k, kr, 60, None)
    jobs['mitch_snare'] = (s, sr, 60, None)
    g, gr = snare2(ghost=True)
    jobs['mitch_ghost'] = (g, gr, 60, None)
    a, r = hat()
    jobs['mitch_hat'] = (a, r, 60, None)
    a, r = hat(open_=True)
    jobs['mitch_ohat'] = (a, r, 60, None)
    a, r = reese_raw()
    jobs['mitch_reese_raw'] = (a, r, 36, (0, len(a)))
    a, r = reese_raw(cut=1100.0, drive=4.5, saws=((-2, 0.8), (-1, 1.0), (1, 1.0), (3, 0.8)))
    jobs['mitch_reese_raw_dark'] = (a, r, 36, (0, len(a)))
    a, r = revcym()
    jobs['mitch_revcym'] = (a, r, 60, None)
    a = norm(resample(render(0, [51], 0.9, kit=0, vel=112), 44100, 22050, antialias=True))
    jobs['mitch_ride'] = (fade_out(a, 22050, 0.3), 22050, 60, None)
    rb, rr = jobs['mitch_reese_mid'][:2]
    a, r = rewind({'kick': (k, kr), 'snare': (s, sr), 'reese': (np.tile(rb, 4), rr * 2 ** (-7 / 12)),
                   'stab': jobs['mitch_stab_min'][:2]})
    jobs['mitch_rewind'] = (a, r, 60, None)
    a, r = airhorn()
    jobs['mitch_airhorn'] = (a, r, 60, None)
    # ---- v3
    a, r = kick3(); jobs['mitch3_kick'] = (a, r, 60, None)
    a, r = snare3(); jobs['mitch3_snare'] = (a, r, 60, None)
    a, r = snare3(ghost=True); jobs['mitch3_ghost'] = (a, r, 60, None)
    a, r = brass3([41, 53], 53); jobs['mitch3_brass_lo'] = (a, r, 53, None)
    a, r = brass3([51, 63], 63); jobs['mitch3_brass_hi'] = (a, r, 63, None)
    a, r = pluck3(); jobs['mitch3_pluck'] = (a, r, 60, None)
    for nm, note in (('f1', 29), ('c2', 36), ('db2', 37), ('eb2', 39)):
        M = int(round(8 * BEAT3 * hz(note)))
        per = 96 if note >= 36 else 128
        a, r = reese(note, per, M, None, 0.9, sub=0.0, fund=0.45, drive=2.4, lfo=wob_lfo3(), top=40,
                     formants=((8, 4, 3.0),), detune=((-2, 0.8), (-1, 1.0), (1, 1.0), (2, 0.8)))
        jobs['mitch3_wob_' + nm] = (a, r, note, (0, len(a)))
    for name, (a, rate, key, loop) in jobs.items():
        write_wav(OUT + name + '.wav', a, rate, key, loop)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-18s %6d samples @ %5d Hz, grondtoon %d%s' % (name, len(a), rate, key, ', loop' if loop else ''))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()

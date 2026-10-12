#!/usr/bin/env python3
"""Project Grounded: eigen samples voor Battle! Hoopa (hoopa_theme.py), voorvoegsel hoopa_*.

Emerald heeft geen oud, geen dubbelriet (mizmar/zurna) en geen darbuka; die klanken zijn hier gemaakt, één sample per
±7 halve tonen (keysplit), zodat niets ver getransponeerd wordt en niets boven ±4 kHz uitkomt (Jordi: geen schelle
fluitjes):
  hoopa_oud_50/57/64/71   oud: FluidR3 Nylon (GM 24) als lijf + tweede koor +7 cent (de dubbele snaren van de oud),
                          risha-aanslag (veerplectrum: korte tik + 'tjak'), houten klankkast (bult rond 200-300 Hz),
                          fretloos dus geen boventoonglans: lowpass 3,4 kHz, korte uitklank
  hoopa_mizmar_57/64/71   mizmar/zurna (slangenbezweerder): FluidR3 Shanai (GM 111) in de MIDDENligging, nasaal
                          (bult 1-1,6 kHz) maar hard afgesneden boven 3 kHz; gelust
  hoopa_dum               darbuka 'dum' (midden van het vel): 128 -> 96 Hz, holle kelk-resonantie, ±0,4 s
  hoopa_tek               darbuka 'tek' (rand, rechterhand): droge klap + korte keramische ring (680/1350 Hz)
  hoopa_bendir            lijsttrom met snaarmat: diepe 'doem' 78 -> 60 Hz + zoemende snaren (ruis 300-2500 Hz)
  hoopa_zill              vingerbekkens: twee licht ontstemde bronzen bekkentjes (deelt. 1,5-3,2 kHz), zacht gefilterd
Gebruik: python3 tools/grounded/hoopa_samples.py [naam ...]"""
import os, subprocess, sys, tempfile, wave
import numpy as np
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import resample, auto_loop, write_wav

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
SR = 44100
RATE = 13379
RNG = np.random.default_rng(662)

OUD_KEYS = (50, 57, 64, 71)
MIZ_KEYS = (57, 64, 71)


def render(prog, note, dur, vel=110):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    t.append(mido.Message('program_change', channel=0, program=prog))
    t.append(mido.Message('note_on', channel=0, note=note, velocity=vel, time=0))
    t.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=int(dur * 960)))
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', str(SR), '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1) / 32768.0
    s = int(np.argmax(np.abs(a) > 0.003))
    return a[s:]


def band(x, lo, hi, sr=SR):
    f = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / sr)
    f[(fr < lo) | (fr > hi)] = 0
    return np.fft.irfft(f, len(x))


def soft_lowpass(x, hi, slope=500, sr=SR):
    f = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / sr)
    m = fr > hi
    f[m] *= np.exp(-(fr[m] - hi) / slope)
    return np.fft.irfft(f, len(x))


def peak_eq(x, fc, q, gain_db, sr=SR):
    """zachte bult (of dal) in het spectrum: gaussisch op een log-frequentie-as."""
    f = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / sr)
    w = np.log2(np.maximum(fr, 1) / fc) * q
    f *= 10 ** (gain_db / 20 * np.exp(-w * w))
    return np.fft.irfft(f, len(x))


def shape(x, f0, target_db, sr=SR, lim=15.0):
    """harmonischenprofiel naar een doel (dB per harmonische t.o.v. de sterkste): zo klinken alle keysplit-samples
    van één instrument even rond, hoe FluidR3 per noot ook uitvalt. Statische EQ, de envelop blijft."""
    seg = x[len(x) // 6:]
    F = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))); fr = np.fft.rfftfreq(len(seg), 1 / sr)
    hs, cur = [], []
    for m, tgt in enumerate(target_db, 1):
        if f0 * m > 4500:
            break
        sel = (fr > f0 * m * 0.97) & (fr < f0 * m * 1.03)
        hs.append(f0 * m); cur.append(20 * np.log10(F[sel].max() + 1e-12))
    cur = np.array(cur) - max(cur)
    corr = np.clip(np.array(target_db[:len(hs)]) - cur, -lim, lim)
    X = np.fft.rfft(x); fx = np.fft.rfftfreq(len(x), 1 / sr)
    g = np.interp(np.log2(np.maximum(fx, 20)), np.log2(hs), corr)
    return np.fft.irfft(X * 10 ** (g / 20), len(x))


def hz(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def norm(x, peak=0.97):
    return x / (np.abs(x).max() + 1e-12) * peak


def tail_fade(x, sec):
    n = int(sec * SR); x = x.copy(); x[-n:] *= np.linspace(1, 0, n) ** 1.5
    return x


def fit(x, n):
    return np.concatenate([x, np.zeros(max(0, n - len(x)))])[:n]


def membrane(f_hi, f_lo, sweep, decay, dur, modes=((1.0, 1.0, 1.0), (1.59, 0.45, 0.45), (2.14, 0.25, 0.25))):
    t = np.arange(int(dur * SR)) / SR
    f = f_lo + (f_hi - f_lo) * np.exp(-t / sweep)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.zeros_like(t)
    for ratio, amp, dec in modes:
        x += amp * np.sin(ph * ratio) * np.exp(-t / (decay * dec))
    return x


# ------------------------------------------------------------------------------------------------ oud -------------
def oud(key, dur=0.62):
    n = int(dur * SR); t = np.arange(n) / SR
    a = norm(fit(render(24, key, dur + 0.2, 118), n))
    # tweede koor: dezelfde noot een fractie hoger (oud = dubbele snaren), via resampling van de render
    b = norm(fit(np.interp(np.arange(n) * 2 ** (7 / 1200), np.arange(len(a)), a), n))
    x = 0.6 * a + 0.5 * np.roll(b, int(0.004 * SR))
    # de grondtoon is bij een oud sterk en rond: sinus erbij die snel wegsterft
    f0 = hz(key)
    x += (0.45 if key < 60 else 0.25) * np.sin(2 * np.pi * f0 * t) * np.exp(-t / 0.22) * np.minimum(1, t / 0.002)
    # klankkast (bult) en fretloos/zacht: geen glans boven 3,4 kHz; per sample hetzelfde harmonischenprofiel
    x = shape(x, f0, (0, -2, -6, -9, -13, -17, -21, -25, -28))
    x = peak_eq(x, 250, 1.6, 4.0)
    x = peak_eq(x, 1100, 1.2, 2.0)
    # risha: veerplectrum op de snaar = korte heldere tik + 'tjak' van het hout
    m = int(0.03 * SR); tt = np.arange(m) / SR
    tick = band(RNG.standard_normal(m), 1500, 3600) * np.exp(-tt / 0.003)
    wood = band(RNG.standard_normal(m), 250, 1100) * np.exp(-tt / 0.008)
    x = norm(x)
    x[:m] += 0.30 * norm(tick) + 0.22 * norm(wood)
    x = soft_lowpass(x, 3400, 380)
    x *= np.exp(-t / 0.42)
    return norm(tail_fade(x, 0.1)), None


# --------------------------------------------------------------------------------------------- mizmar -------------
def mizmar(key, dur=0.9):
    n = int(dur * SR); t = np.arange(n) / SR
    x = norm(fit(render(111, key, dur + 0.3, 112), n))
    # nasaal riet, maar met lijf: FluidR3 Shanai heeft een zwakke grondtoon (-9..-17 dB) en zijn energie op de
    # 5e-7e harmonische; per sample naar hetzelfde profiel (grondtoon sterk, bult op 3-5, daarna snel weg), dan
    # alles boven 2,8 kHz eraf (niet schel)
    x = shape(x, hz(key), (0, -1, -3, -4, -5, -9, -13, -18, -24, -30))
    x = soft_lowpass(x, 2800, 300)
    x = norm(x) * np.minimum(1, t / 0.015)
    a = resample(x, SR, RATE)
    a, lp = auto_loop(a, RATE)
    return norm(a), lp


# --------------------------------------------------------------------------------------------- trommen ------------
def drum(name):
    if name == 'dum':
        dur = 0.42
        syn = membrane(128, 96, 0.03, 0.16, dur, modes=((1.0, 1.0, 1.0), (1.58, 0.35, 0.5), (2.3, 0.18, 0.3)))
        t = np.arange(len(syn)) / SR
        hollow = np.sin(2 * np.pi * 225 * t) * np.exp(-t / 0.05) * 0.35         # de kelk resoneert mee
        m = int(0.025 * SR)
        slap = band(RNG.standard_normal(m), 200, 1400) * np.exp(-np.arange(m) / SR / 0.006)
        x = norm(syn) + hollow
        x[:m] += 0.45 * norm(slap)
        x = np.tanh(1.6 * norm(x)) / np.tanh(1.6)
        x = band(x, 60, 20000)
    elif name == 'tek':
        dur = 0.16
        n = int(dur * SR); t = np.arange(n) / SR
        crack = band(RNG.standard_normal(n), 1200, 4200) * np.exp(-t / 0.0035)
        ring = (np.sin(2 * np.pi * 680 * t) * np.exp(-t / 0.035) + 0.55 * np.sin(2 * np.pi * 1350 * t) * np.exp(-t / 0.022)
                + 0.3 * np.sin(2 * np.pi * 2210 * t) * np.exp(-t / 0.012))
        snap = band(RNG.standard_normal(n), 400, 1500) * np.exp(-t / 0.01)
        x = 0.9 * norm(crack) + 0.75 * norm(ring) + 0.4 * norm(snap)
    elif name == 'bendir':
        dur = 0.75
        syn = membrane(78, 60, 0.04, 0.3, dur, modes=((1.0, 1.0, 1.0), (1.52, 0.4, 0.5), (2.0, 0.2, 0.3)))
        n = len(syn); t = np.arange(n) / SR
        buzz = band(RNG.standard_normal(n), 300, 2500) * np.exp(-t / 0.13) * (1 + 0.6 * np.sin(2 * np.pi * 70 * t))
        m = int(0.03 * SR)
        thump = band(RNG.standard_normal(m), 120, 700) * np.exp(-np.arange(m) / SR / 0.01)
        x = norm(syn) + 0.32 * norm(buzz)
        x[:m] += 0.4 * norm(thump)
        x = np.tanh(1.4 * norm(x)) / np.tanh(1.4)
        x = band(x, 48, 20000)
    elif name == 'zill':
        dur = 0.55
        n = int(dur * SR); t = np.arange(n) / SR
        x = np.zeros(n)
        for det in (1.0, 1.013):                    # twee bekkentjes tegen elkaar: zweving
            for f, a, d in ((1520, 1.0, 0.30), (2280, 0.55, 0.20), (3150, 0.3, 0.12), (3870, 0.12, 0.08)):
                x += a * np.sin(2 * np.pi * f * det * t + RNG.uniform(0, 6.3)) * np.exp(-t / d)
        clash = band(RNG.standard_normal(n), 1500, 4500) * np.exp(-t / 0.006)
        x = norm(x) + 0.35 * norm(clash)
    x = x[:int(dur * SR)]
    x = soft_lowpass(x, 4200, 450)
    return norm(tail_fade(x, min(0.06, dur / 4))), None


# naam: (functie, grondtoon)
SAMPLES = {}
for k in OUD_KEYS:
    SAMPLES['hoopa_oud_%d' % k] = (lambda k=k: oud(k), k)
for k in MIZ_KEYS:
    SAMPLES['hoopa_mizmar_%d' % k] = (lambda k=k: mizmar(k), k)
for d in ('dum', 'tek', 'bendir', 'zill'):
    SAMPLES['hoopa_' + d] = (lambda d=d: drum(d), 60)


def main(only=None):
    global RNG
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    total = 0
    for name, (fn, key) in SAMPLES.items():
        if only and name not in only:
            continue
        RNG = np.random.default_rng(662 + sum(name.encode()))     # vaste seed per sample: los of samen = identiek
        a, lp = fn()
        if lp is None:                                # nog op 44,1 kHz
            a = norm(resample(a, SR, RATE))
        write_wav(OUT + name + '.wav', a, RATE, key, lp)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (
                label, name)
        total += len(a) + 16
        sp = np.abs(np.fft.rfft(a)) ** 2; fr = np.fft.rfftfreq(len(a), 1 / RATE)
        print('%-18s %5d samples (%.2f s), grondtoon %d%s, >2k %4.1f%%, >4k %4.1f%%' % (
            name, len(a), len(a) / RATE, key, ', loop %d-%d' % lp if lp else '', 100 * sp[fr > 2000].sum() / sp.sum(),
            100 * sp[fr > 4000].sum() / sp.sum()))
    open(DATA, 'w').write(inc)
    print('totaal %.1f KB' % (total / 1024))


if __name__ == '__main__':
    main(sys.argv[1:] or None)

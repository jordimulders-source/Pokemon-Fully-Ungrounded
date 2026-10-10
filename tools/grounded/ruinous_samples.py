#!/usr/bin/env python3
"""Project Grounded: eigen samples voor Battle! Treasures of Ruin (ruinous_theme.py), voorvoegsel ruinous_*.

Gemeten aan de drumstem van het origineel (Spleeter, maat 17-32): de 'snare op elke tel' is eigenlijk een grote trom
(51% van de energie in 90-130 Hz, 23% in 130-200 Hz, ring tot -12 dB na ±250 ms, een korte tik erop); tussen de
tellen (de achtste 'en') valt een lage, korte dreun (30-90 Hz, -12 dB na ±90 ms). Hoog (> 3 kHz) maar 1-2%.
Op de GBA en Jordi's speakers geeft een luid laag onder ±60 Hz 'overload': de dreun ligt hier op 72 -> 62 Hz.
  ruinous_taiko   grote trom op de tel: vel 128 -> 104 Hz, twee hogere modi, korte vel-tik + houten rand, kamergalm
  ruinous_boom    lage dreun op de 'en': 78 -> 62 Hz, kort (±0,2 s), zachte klik (anders hoor je hem niet in 8 bit)
  ruinous_ka      de rand van de taiko (ka): droge tik voor roffels en opmaten
  ruinous_impact  de inslag (maat 5 en 65): lage trom + ruisuitbarsting + metalen naklank, ±1,1 s
  ruinous_ost     het elektronische ostinato (v2): bijna zuivere B3 + kwint als één sample, zachte puls
  ruinous_pluck_* (v2) het lage, zware Aziatische tokkelinstrument van de intro en de lijn vanaf maat 21 (Jordi:
                  'vrij laag Aziatisch klinkend pluk instrument, zwaarder dan een sitar'), één sample per 7 halve tonen
                  (E2 B2 F#3 C#4 G#4), FluidR3 koto + shamisen-zoem
(v1 had een zaagtand-synth en de stock-koto; Jordi: 'voor de rest alles niet'.)
Gebruik: python3 tools/grounded/ruinous_samples.py [naam ...]   (daarna: python3 tools/grounded/resample_wav.py --all)"""
import os, subprocess, sys, tempfile, wave
import numpy as np
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import resample, write_wav

OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
SR = 44100
SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
RATE = 11025
RNG = np.random.default_rng(683)


def band(x, lo, hi, sr=SR):
    f = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / sr)
    f[(fr < lo) | (fr > hi)] = 0
    return np.fft.irfft(f, len(x))


def soft_lowpass(x, hi, slope=500, sr=SR):
    f = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / sr)
    m = fr > hi
    f[m] *= np.exp(-(fr[m] - hi) / slope)
    return np.fft.irfft(f, len(x))


def norm(x, peak=0.97):
    return x / (np.abs(x).max() + 1e-12) * peak


def tail_fade(x, sec):
    n = int(sec * SR); x = x.copy(); x[-n:] *= np.linspace(1, 0, n) ** 1.5
    return x


def membrane(f_hi, f_lo, sweep, decay, dur, modes):
    t = np.arange(int(dur * SR)) / SR
    f = f_lo + (f_hi - f_lo) * np.exp(-t / sweep)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.zeros_like(t)
    for ratio, amp, dec in modes:
        x += amp * np.sin(ph * ratio) * np.exp(-t / (decay * dec))
    return x


def room(x, rt=0.18, mix=0.18):
    """korte kamergalm: ruis-impulsrespons met exponentiële staart (lowpass), zodat de trom 'groot' klinkt."""
    n = int(rt * 2.5 * SR)
    t = np.arange(n) / SR
    ir = band(RNG.standard_normal(n), 80, 3500) * np.exp(-t / (rt / 3))
    ir[0] = 0
    y = np.convolve(x, ir)[:len(x)]
    return x + mix * norm(y) * np.abs(x).max()


def taiko():
    dur = 0.5
    x = membrane(128, 104, 0.025, 0.14, dur, ((1.0, 1.0, 1.0), (1.5, 0.35, 0.55), (2.05, 0.18, 0.35)))
    n = len(x); t = np.arange(n) / SR
    m = int(0.02 * SR); tt = np.arange(m) / SR
    skin = band(RNG.standard_normal(m), 300, 2500) * np.exp(-tt / 0.004)       # bachi op het vel
    wood = band(RNG.standard_normal(m), 1200, 4500) * np.exp(-tt / 0.0015)     # tik
    x = norm(x)
    x[:m] += 0.42 * norm(skin) + 0.22 * norm(wood)
    x = np.tanh(1.5 * x) / np.tanh(1.5)
    x = room(x, 0.2, 0.16)
    x = band(x, 55, 20000)
    x = soft_lowpass(x, 3500, 600)
    return norm(tail_fade(x, 0.08))


def boom():
    dur = 0.24
    x = membrane(78, 62, 0.02, 0.07, dur, ((1.0, 1.0, 1.0), (1.6, 0.25, 0.5)))
    t = np.arange(len(x)) / SR
    m = int(0.012 * SR)
    click = band(RNG.standard_normal(m), 600, 2500) * np.exp(-np.arange(m) / SR / 0.002)
    x = norm(x)
    x[:m] += 0.16 * norm(click)
    # een tweede, hogere boventoon (2x) maakt hem op kleine speakers hoorbaar zonder meer sub
    x += 0.22 * np.sin(2 * np.pi * 2 * 64 * t) * np.exp(-t / 0.04)
    x = np.tanh(1.3 * norm(x)) / np.tanh(1.3)
    x = band(x, 50, 6000)
    return norm(tail_fade(x, 0.05))


def ka():
    dur = 0.1
    n = int(dur * SR); t = np.arange(n) / SR
    crack = band(RNG.standard_normal(n), 1200, 4500) * np.exp(-t / 0.004)
    body = np.sin(2 * np.pi * 820 * t) * np.exp(-t / 0.018) + 0.5 * np.sin(2 * np.pi * 1510 * t) * np.exp(-t / 0.01)
    low = np.sin(2 * np.pi * 180 * t) * np.exp(-t / 0.025)
    x = norm(crack) + 0.6 * norm(body) + 0.35 * low
    x = soft_lowpass(x, 4200, 500)
    return norm(tail_fade(x, 0.02))


def impact():
    dur = 1.1
    lo = membrane(96, 62, 0.06, 0.32, dur, ((1.0, 1.0, 1.0), (1.47, 0.4, 0.5), (2.1, 0.2, 0.3)))
    n = len(lo); t = np.arange(n) / SR
    burst = band(RNG.standard_normal(n), 300, 5000) * np.exp(-t / 0.09)
    metal = np.zeros(n)
    for f, a, d in ((410, 1.0, 0.5), (623, 0.7, 0.4), (887, 0.5, 0.33), (1270, 0.35, 0.25), (1730, 0.25, 0.2)):
        metal += a * np.sin(2 * np.pi * f * t + RNG.uniform(0, 6.3)) * np.exp(-t / d)
    metal = band(metal * (1 + 0.3 * band(RNG.standard_normal(n), 2, 30)), 300, 5000)
    x = 0.9 * norm(lo) + 0.55 * norm(burst) + 0.28 * norm(metal)
    x = np.tanh(1.6 * norm(x)) / np.tanh(1.6)
    x = room(x, 0.35, 0.22)
    x = band(x, 50, 20000)
    x = soft_lowpass(x, 4000, 600)
    return norm(tail_fade(x, 0.25))


def render(prog, note, dur, vel=112):
    """één noot uit FluidR3 (GM-programma prog), mono, vanaf de eerste aanzet"""
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


def shape(x, f0, target_db, sr=SR, lim=15.0):
    """harmonischenprofiel naar een doel (dB per harmonische t.o.v. de sterkste); statische EQ, envelop blijft."""
    seg = x[len(x) // 8:]
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
    g[fx > hs[-1]] = min(corr[-1], 0.0)          # boven de laatste harmonische niets oppompen
    return np.fft.irfft(X * 10 ** (g / 20), len(x))


def fit(x, n):
    return np.concatenate([x, np.zeros(max(0, n - len(x)))])[:n]


def pluck(key, dur=0.55):
    """laag, zwaar Aziatisch tokkelinstrument (biwa/lage koto). Gemeten in de stem 'piano' (maat 1-8, E2/F#2/B2):
    sterke grondtoon, h2-h5 -11..-27 dB, een felle 6e harmonische (-4 dB: de sawari-zoem), heraanslagen in 16en.
    FluidR3 Koto (107) heeft de grondtoon (-3) maar geen zoem, Shamisen (106) de zoem (h4/h5/h8) maar geen grondtoon:
    koto als lijf + 30% shamisen + een sinus op de grondtoon, plectrumtik, lowpass 3,6 kHz."""
    n = int(dur * SR); t = np.arange(n) / SR
    f0 = 440.0 * 2 ** ((key - 69) / 12)
    k = norm(fit(render(107, key, dur + 0.2), n))
    sh = norm(fit(render(106, key, dur + 0.2), n))
    x = k + 0.3 * sh
    x += 0.55 * np.sin(2 * np.pi * f0 * t) * np.exp(-t / 0.28) * np.minimum(1, t / 0.003)
    m = int(0.012 * SR); tt = np.arange(m) / SR
    x = norm(x)
    x[:m] += 0.25 * norm(band(RNG.standard_normal(m), 900, 3500) * np.exp(-tt / 0.002))
    prof = (0, -10, -13, -21, -22, -6, -11, -14) if key < 60 else (0, -8, -12, -20, -22, -16, -20, -24)
    x = shape(x, f0, prof)     # het gemeten profiel (E2, maat 1); hoog zonder felle zoem boven 2 kHz (niet schel)
    x = soft_lowpass(x, 3600, 450)
    x *= np.exp(-t / 0.38)
    return norm(tail_fade(x, 0.12))


def ost(key=59, dur=0.4):
    """het elektronische ostinato: gemeten (maat 66-67, stem 'other') bijna zuiver (h2 -26 dB), de kwint (F#4)
    pulseert mee. Dus grondtoon + kwint als één sample (sinus + 15% 3e harmonische, twee stemmen 6 cent uit elkaar),
    zachte aanzet (8 ms) en een korte pulserende uitklank; 1 kanaal per aanslag."""
    n = int(dur * SR); t = np.arange(n) / SR
    f0 = 440.0 * 2 ** ((key - 69) / 12)
    x = np.zeros(n)
    for f, a in ((f0, 1.0), (f0 * 1.4983, 0.62)):
        for det in (-3, 3):
            ff = f * 2 ** (det / 1200)
            x += a * (np.sin(2 * np.pi * ff * t) + 0.15 * np.sin(2 * np.pi * 3 * ff * t))
    env = np.minimum(1, t / 0.008) * (0.35 + 0.65 * np.exp(-t / 0.07)) * np.exp(-t / 0.35)
    return norm(tail_fade(x * env, 0.06))


SAMPLES = {   # naam: (functie, grondtoon)
    'ruinous_taiko': (taiko, 60), 'ruinous_boom': (boom, 60), 'ruinous_ka': (ka, 60),
    'ruinous_impact': (impact, 60), 'ruinous_ost': (ost, 59),
}
PLUCK_KEYS = (40, 47, 54, 61, 68)
for _k in PLUCK_KEYS:
    SAMPLES['ruinous_pluck_%d' % _k] = (lambda k=_k: pluck(k), _k)


def main(only=None):
    global RNG
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    total = 0
    for name, (fn, key) in SAMPLES.items():
        if only and name not in only:
            continue
        RNG = np.random.default_rng(683 + sum(name.encode()))     # vaste seed per sample: los of samen = identiek
        a = norm(resample(fn(), SR, RATE))
        write_wav(OUT + name + '.wav', a, RATE, key, None)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (
                label, name)
        total += len(a) + 16
        sp = np.abs(np.fft.rfft(a)) ** 2; fr = np.fft.rfftfreq(len(a), 1 / RATE)
        print('%-16s %5d samples (%.2f s), < 60 Hz %4.1f%%, < 150 Hz %4.1f%%, > 2k %4.1f%%' % (
            name, len(a), len(a) / RATE, 100 * sp[fr < 60].sum() / sp.sum(), 100 * sp[fr < 150].sum() / sp.sum(),
            100 * sp[fr > 2000].sum() / sp.sum()))
    open(DATA, 'w').write(inc)
    print('totaal %.1f KB' % (total / 1024))


if __name__ == '__main__':
    main(sys.argv[1:] or None)

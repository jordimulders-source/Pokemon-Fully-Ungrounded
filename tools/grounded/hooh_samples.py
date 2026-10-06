#!/usr/bin/env python3
"""Project Grounded: eigen samples voor Battle! Ho-Oh v2 (hooh_theme.py), voorvoegsel hooh_*.

Waarom (Jordi over v1: 'te vrolijk, trompetten/fluiten voeren de boventoon en zijn schel, nog niet Japans genoeg'):
de stock-'Japanse' klanken zijn dun of fout (whistle = schel fluitje, koto_low als shamisen = geen bachi-tik,
sd90-shakuhachi in de hoge ligging). Hier per instrument een eigen sample, één per ±7 halve tonen (keysplit), zodat
niets ver getransponeerd wordt en niets boven ±4 kHz uitkomt:
  hooh_shami_52/59/66/73  tsugaru-shamisen: FluidR3 Shamisen (GM 106) + bachi-slag op het vel (korte 'tak' + doffe
                          vellaag) + sawari (zachte asymmetrische vervorming = het zoemende 'bzz' van de snaar)
  hooh_koto_57/64/71/78   koto: FluidR3 Koto (GM 107), lowpass 4 kHz, natuurlijk uitklinkend
  hooh_shaku_62/69/76     shakuhachi: FluidR3 Shakuhachi (GM 77; bijna een sinus) + 2e/3e harmonische en ademruis
                          (muraiki) rond de grondtoon, aanblaas-'chiff', lowpass 3,2 kHz; gelust
  hooh_sho                sho: clusterakkoord (aitake-achtig: grondtoon-secunde-kwint-octaaf-none, A4 B4 E5 A5 B5; zonder terts of sext,
                          dus mineur- én majeurvrij),
                          rietorgel additief met lichte zweving, gelust; grondtoon A4
  hooh_odaiko             grote trom: FluidR3 Taiko (GM 116) + gesynthetiseerd vel (130 -> 58 Hz) + galm
  hooh_nagado             nagado-daiko (middelste trom): idem, hoger en korter
  hooh_shime              shime-daiko: strak gespannen hoge trom (430 -> 360 Hz), droge 'tsu'
  hooh_ka                 stok op de rand ('ka')
  hooh_kiai               kiai-roep 'HA!' van een mannengroep (formantsynthese, geen opname)
Gebruik: python3 tools/grounded/hooh_samples.py [naam ...]"""
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
RNG = np.random.default_rng(250)

SHAMI_KEYS = (52, 59, 66, 73)
KOTO_KEYS = (57, 64, 71, 78)
SHAKU_KEYS = (62, 69, 76)


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


def hz(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def norm(x, peak=0.97):
    return x / (np.abs(x).max() + 1e-12) * peak


def tail_fade(x, sec):
    n = int(sec * SR); x = x.copy(); x[-n:] *= np.linspace(1, 0, n) ** 1.5
    return x


def room(x, length, decay, hi=2500, mix=0.35):
    n = int(length * SR)
    ir = RNG.standard_normal(n) * np.exp(-np.arange(n) / SR / decay)
    ir = soft_lowpass(ir, hi); ir[:int(0.012 * SR)] = 0
    ir /= np.sqrt((ir ** 2).sum())
    wet = np.concatenate([np.convolve(x, ir), [0.0]])[:len(x) + n]
    dry = np.concatenate([x, np.zeros(n)])
    return dry + mix * wet / (np.abs(wet).max() + 1e-9) * np.abs(x).max()


def membrane(f_hi, f_lo, sweep, decay, dur, modes=((1.0, 1.0, 1.0), (1.59, 0.45, 0.45), (2.14, 0.25, 0.25))):
    t = np.arange(int(dur * SR)) / SR
    f = f_lo + (f_hi - f_lo) * np.exp(-t / sweep)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.zeros_like(t)
    for ratio, amp, dec in modes:
        x += amp * np.sin(ph * ratio) * np.exp(-t / (decay * dec))
    return x


# ------------------------------------------------------------------------------------------- tokkels ---------------
def shamisen(key, dur=0.5):
    body = render(106, key, dur + 0.2, 118)[:int(dur * SR)]
    body = np.concatenate([body, np.zeros(max(0, int(dur * SR) - len(body)))])
    body = norm(body)
    t = np.arange(len(body)) / SR
    # sawari: asymmetrische zachte vervorming die met de uitklank afneemt (het 'bzz' van de eerste snaar)
    saw = np.tanh(2.6 * body + 0.35 * body ** 2) - np.tanh(0.0)
    x = 0.55 * body + 0.45 * norm(saw) * np.exp(-t / 0.18)
    # FluidR3 mist in de lage ligging de grondtoon (gemeten: E3 begint bij de 3e harmonische): 1e/2e erbij,
    # zodat de toonhoogte en het 'lijf' (biwa-achtig in de lage noten) duidelijk zijn
    f0 = hz(key)
    low = np.sin(2 * np.pi * f0 * t) * 0.5 * np.exp(-t / 0.16) + np.sin(2 * np.pi * 2 * f0 * t + 1) * 0.35 * np.exp(-t / 0.12)
    x += low * np.minimum(1, t / 0.002) * (1.0 if key < 62 else 0.5)
    # bachi: de plectrumslag op het kattenvel = korte, doffe 'tak' (vel 180-900 Hz) + harde tik (1,2-3 kHz)
    n = int(0.06 * SR); tt = np.arange(n) / SR
    skin = band(RNG.standard_normal(n), 180, 900) * np.exp(-tt / 0.012)
    tick = band(RNG.standard_normal(n), 1200, 3000) * np.exp(-tt / 0.004)
    x[:n] += 0.55 * norm(skin) + 0.25 * norm(tick)
    x = soft_lowpass(x, 3800, 400)
    x *= np.exp(-t / 0.35)                           # strak: tsugaru-shamisen klinkt kort
    return norm(tail_fade(x, 0.08)), None


def koto(key, dur=0.75):
    x = render(107, key, dur + 0.2, 116)[:int(dur * SR)]
    x = soft_lowpass(x, 3600, 450)
    t = np.arange(len(x)) / SR
    x *= np.exp(-t / 0.9)
    return norm(tail_fade(x, 0.12)), None


def shakuhachi(key, dur=0.75):
    f0 = hz(key)
    body = render(77, key, dur + 0.3, 112)[:int(dur * SR)]
    body = norm(body)
    n = len(body); t = np.arange(n) / SR
    env = np.clip(t / 0.05, 0, 1)
    # boventonen (de FluidR3-sample is bijna een sinus): 2e en 3e harmonische via een fasecopie van de grondtoon
    ana = np.fft.ifft(np.fft.fft(body) * (np.arange(n) < n // 2) * 2)
    amp, ph = np.abs(ana), np.unwrap(np.angle(ana))
    harm = amp * (0.32 * np.sin(2 * ph) + 0.16 * np.sin(3 * ph + 0.7) + 0.05 * np.sin(4 * ph))
    tone = body + harm * env
    # ademruis: smalle banden rond grondtoon en 2e harmonische + breed 'hhh' (muraiki), zwak gemoduleerd
    nz = RNG.standard_normal(n)
    breath = 0.6 * band(nz, f0 * 0.85, f0 * 1.2) + 0.35 * band(nz, f0 * 1.8, f0 * 2.3) + 0.25 * band(nz, 900, 2600)
    breath = norm(breath) * (0.22 + 0.05 * np.sin(2 * np.pi * 3.1 * t))
    # aanblazen: korte ruisstoot
    m = int(0.07 * SR)
    chiff = np.zeros(n); chiff[:m] = norm(band(RNG.standard_normal(m), 600, 2800)) * np.exp(-np.arange(m) / SR / 0.02)
    x = norm(tone) * 0.85 + breath + 0.45 * chiff
    x = soft_lowpass(x, 3200, 350)
    x *= np.minimum(1, t / 0.012)
    x = norm(x)
    a = resample(x, SR, RATE)
    a, lp = auto_loop(a, RATE)
    return norm(a), lp


def sho(dur=0.9):
    """aitake-achtige cluster: A4 B4 E5 A5 B5 (grondtoon-secunde-kwint-octaaf-none, geen terts/sext), riet (harmonischen 1/k^1.4, oneven iets
    sterker), elke toon met een kleine zweving; gelust."""
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.zeros(n)
    for semi, amp in ((0, 1.0), (2, 0.7), (7, 0.85), (12, 0.6), (14, 0.45)):
        f = hz(69 + semi)
        for det in (-0.6, 0.6):
            ff = f * 2 ** (det / 1200)
            ph = RNG.uniform(0, 6.28)
            for k in range(1, 9):
                if k * ff > 3400:
                    break
                g = (1.25 if k % 2 else 0.8) / k ** 1.4
                x += amp * g * np.sin(2 * np.pi * k * ff * t + ph * k)
    x += 0.05 * norm(band(RNG.standard_normal(n), 500, 2500))
    x = soft_lowpass(x, 3000, 400)
    a = resample(norm(x), SR, RATE)
    a, lp = auto_loop(a, RATE)
    return norm(a, 0.9), lp


# ------------------------------------------------------------------------------------------- trommen ---------------
def drum(name):
    if name == 'odaiko':
        dur = 1.05
        body = render(116, 47, 1.2, 127)[:int(dur * SR)]
        syn = membrane(135, 66, 0.04, 0.45, dur)
        m = int(0.1 * SR)
        slap = band(RNG.standard_normal(m), 250, 1500) * np.exp(-np.arange(m) / SR / 0.03)
        x = np.zeros(int(dur * SR))
        x[:len(body)] += 0.8 * norm(body)
        x += 0.95 * syn
        x[:m] += 0.8 * norm(slap)
        x = room(x, 0.8, 0.25, 2000, 0.4)
    elif name == 'nagado':
        dur = 0.6
        body = render(116, 52, 0.8, 120)[:int(dur * SR)]
        syn = membrane(170, 100, 0.025, 0.22, dur)
        m = int(0.05 * SR)
        slap = band(RNG.standard_normal(m), 400, 2400) * np.exp(-np.arange(m) / SR / 0.012)
        x = np.zeros(int(dur * SR))
        x[:len(body)] += 0.75 * norm(body)
        x += 0.8 * syn
        x[:m] += 0.6 * norm(slap)
        x = room(x, 0.4, 0.12, 2400, 0.3)
    elif name == 'shime':
        dur = 0.22
        syn = membrane(430, 360, 0.01, 0.06, dur, modes=((1.0, 1.0, 1.0), (1.5, 0.5, 0.6), (2.3, 0.3, 0.4)))
        m = int(0.03 * SR)
        crack = band(RNG.standard_normal(m), 900, 3500) * np.exp(-np.arange(m) / SR / 0.005)
        x = norm(syn); x[:m] += 0.7 * norm(crack)
        x = room(x, 0.15, 0.04, 3000, 0.2)
    elif name == 'ka':
        dur = 0.12
        n = int(dur * SR); t = np.arange(n) / SR
        click = band(RNG.standard_normal(n), 1500, 4500) * np.exp(-t / 0.005)
        wood = np.sin(2 * np.pi * 1050 * t) * np.exp(-t / 0.03) + 0.4 * np.sin(2 * np.pi * 2450 * t) * np.exp(-t / 0.015)
        x = norm(click) + 0.9 * wood
    if name in ('odaiko', 'nagado'):
        x = np.tanh(2.0 * norm(x)) / np.tanh(2.0)
        x = band(x, 58, 20000)                      # v2-meting: 40-70 Hz was 42-65% van de drumenergie (brom)
    x = x[:int(dur * SR)]
    x = soft_lowpass(x, 4200, 500)
    return norm(tail_fade(x, min(0.08, dur / 4))), None


# --------------------------------------------------------------------------------- kiai (formantsynthese) ---------
VOWELS = {'a': ((730, 1090, 2440, 3400), (90, 110, 160, 250)), 'o': ((520, 860, 2410, 3300), (80, 100, 150, 250))}


def formant_gain(freq, F, B):
    g = np.ones_like(freq)
    for f, b in zip(F, B):
        g *= f * f / np.sqrt((f * f - freq * freq) ** 2 + (b * freq) ** 2)
    return g


def one_voice(f0, mix, fshift):
    n = len(f0)
    ph = 2 * np.pi * np.cumsum(f0) / SR
    Fa, Ba = VOWELS['a']; Fo, Bo = VOWELS['o']
    x = np.zeros(n)
    for k in range(1, int(SR * 0.45 / f0.min())):
        fk = k * f0
        g = formant_gain(fk, [f * fshift for f in Fa], Ba) * (1 - mix) + formant_gain(fk, [f * fshift for f in Fo], Bo) * mix
        x += g * (fk < 4200) * np.sin(k * ph) / k ** 0.9
    return norm(x)


def kiai():
    dur = 0.42
    n = int(dur * SR); t = np.arange(n) / SR
    out = np.zeros(n + 600)
    for v in range(6):                                # mannengroep: 6 stemmen, licht ontstemd en verschoven
        semis = -3 * np.exp(-t / 0.03) - 2.5 * np.clip((t - 0.2) / 0.22, 0, 1) ** 2
        f0 = hz(57 + RNG.uniform(-0.25, 0.25)) * 2 ** (semis / 12)
        x = one_voice(f0, np.clip((t - 0.12) / 0.25, 0, 1) * 0.5, RNG.uniform(0.95, 1.06))
        off = int(RNG.uniform(0, 0.012) * SR)
        out[off:off + n] += x * RNG.uniform(0.75, 1.0)
    x = out[:n]
    h = band(RNG.standard_normal(n), 500, 3500) * np.exp(-t / 0.02)
    x = norm(x) + 0.7 * norm(h) * (t < 0.06)
    x = np.tanh(2.0 * x) / np.tanh(2.0)
    x *= np.minimum(1, t / 0.01) * np.where(t > 0.16, np.exp(-(t - 0.16) / 0.09), 1.0)
    x = soft_lowpass(x, 3800, 400)
    return norm(x), None


# naam: (functie, grondtoon)
SAMPLES = {}
for k in SHAMI_KEYS:
    SAMPLES['hooh_shami_%d' % k] = (lambda k=k: shamisen(k), k)
for k in KOTO_KEYS:
    SAMPLES['hooh_koto_%d' % k] = (lambda k=k: koto(k), k)
for k in SHAKU_KEYS:
    SAMPLES['hooh_shaku_%d' % k] = (lambda k=k: shakuhachi(k), k)
SAMPLES['hooh_sho'] = (sho, 69)
for d in ('odaiko', 'nagado', 'shime', 'ka'):
    SAMPLES['hooh_' + d] = (lambda d=d: drum(d), 60)
SAMPLES['hooh_kiai'] = (kiai, 57)


def main(only=None):
    global RNG
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    total = 0
    for name, (fn, key) in SAMPLES.items():
        if only and name not in only:
            continue
        RNG = np.random.default_rng(250 + sum(name.encode()))     # vaste seed per sample: los of samen = identiek
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
        print('%-16s %5d samples (%.2f s), grondtoon %d%s, >2k %4.1f%%, >4k %4.1f%%' % (
            name, len(a), len(a) / RATE, key, ', loop %d-%d' % lp if lp else '', 100 * sp[fr > 2000].sum() / sp.sum(),
            100 * sp[fr > 4000].sum() / sp.sum()))
    open(DATA, 'w').write(inc)
    print('totaal %.1f KB' % (total / 1024))


if __name__ == '__main__':
    main(sys.argv[1:] or None)

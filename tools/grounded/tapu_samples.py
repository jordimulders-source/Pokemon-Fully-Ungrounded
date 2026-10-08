#!/usr/bin/env python3
"""Project Grounded: eigen samples voor Battle! Tapu v2 (tapu_theme.py), voorvoegsel tapu_*.

Waarom (gemeten, v1 = alleen stock): de stock-trommen (sc88pro_taiko 0,42 s, ambient tom 0,63 s, Indiase trom 0,28 s)
zijn kort en dun, en de MIDI kapte ze na 2-3 zestienden af met release 140: in de game klonken de slagen als
korte tikjes (drumsolo maat 1-8 gemiddeld 3-25 dB, de drumstem van het origineel 26-32 dB; in de stem zit de energie
op 60-120 Hz en klinkt een slag ±1 s na). Daarom:
  tapu_odaiko  grote trom (DUUUU): FluidR3 Taiko (GM 116) + een gesynthetiseerd vel (toonhoogte zakt 110 -> 52 Hz)
               + een velslag (ruis 300-1500 Hz) + een ruimte-galm van ±1 s (geen samples uit de opname)
  tapu_taiko   middelste taiko (de 'du's): zelfde opbouw, hoger (150 -> 82 Hz), korter
  tapu_ka      stok op de rand ('ka'): korte, droge tik
  tapu_crash   FluidR3 crash (GM-drum 57) met lange uitklank, voor de HIT
  tapu_impact  v4: de HIT zelf: lage odaiko + sub-val (125 -> 46 Hz) + velslag + orkesthit (E3+B3) + zaal, 1,8 s
Stemmen (formantsynthese, additief: elke harmonische van een stembandpuls gewogen met de formanten van een klinker,
een groep van 4-6 licht ontstemde stemmen met ademruis; geen audio uit de opname):
  tapu_vox_a   chant-klinker 'aa' (A4, met loop, legato): de bovenstem van het herhalende chant-thema
  tapu_vox_hu  lage 'hu' van een mannengroep (F#3, met loop): de lage tussenroepen
  (v3: de 'HOO!'-kreet tapu_shout is weg, Jordi: 'klinkt erg wimpy')
Synth (v3):
  tapu_synth   brede zaagtand-synth (twee ontstemde zaagtanden + blokgolf, exacte loop): synthbas (v3/v4 ook de lead)
Synth-brass (v5):
  tapu_brass / tapu_brass_hi  lead van maat 9-12: vijf ontstemde stemmen met het gemeten koperprofiel (zie brass())
Climax-lead (v6):
  tapu_lead    de snelle figuur van maat 11-12 (D#5-E5 A#5-B5 E6 F6): zachte synth-lead, sterke grondtoon (zie lead())
Gebruik: python3 tools/grounded/tapu_samples.py"""
import os, subprocess, sys, tempfile, wave
import numpy as np
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import resample, auto_loop, write_wav

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
SR = 44100
RNG = np.random.default_rng(1756)


def render(prog, note, dur, vel=120, drum=False):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    ch = 9 if drum else 0
    if not drum:
        t.append(mido.Message('program_change', channel=ch, program=prog))
    t.append(mido.Message('note_on', channel=ch, note=note, velocity=vel, time=0))
    t.append(mido.Message('note_off', channel=ch, note=note, velocity=0, time=int(dur * 960)))
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', str(SR), '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1) / 32768.0
    s = int(np.argmax(np.abs(a) > 0.003))
    return a[s:]


def band(x, lo, hi):
    f = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
    f[(fr < lo) | (fr > hi)] = 0
    return np.fft.irfft(f, len(x))


def lowpass(x, hi):
    return band(x, 0, hi)


def room(x, length, decay, hi=2500, mix=0.35):
    """eenvoudige galm: convolutie met exponentieel uitstervende ruis (lowpass)"""
    n = int(length * SR)
    ir = RNG.standard_normal(n) * np.exp(-np.arange(n) / SR / decay)
    ir = lowpass(ir, hi); ir[:int(0.012 * SR)] = 0                    # 12 ms predelay
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


def drum(name, dur):
    global RNG
    if name == 'odaiko':
        body = render(116, 48, 1.2, 127)[:int(dur * SR)]
        syn = membrane(150, 68, 0.035, 0.55, dur)
        slap = band(RNG.standard_normal(int(0.12 * SR)), 250, 1800) * np.exp(-np.arange(int(0.12 * SR)) / SR / 0.035)
        x = np.zeros(int(dur * SR))
        x[:len(body)] += 0.8 * body / np.abs(body).max()
        x += 0.9 * syn
        x[:len(slap)] += 1.0 * slap / np.abs(slap).max()
        x = room(x, 0.9, 0.28, 2200, 0.45)
    elif name == 'taiko':
        body = render(116, 52, 0.8, 120)[:int(dur * SR)]
        syn = membrane(150, 82, 0.025, 0.28, dur)
        slap = band(RNG.standard_normal(int(0.05 * SR)), 400, 2500) * np.exp(-np.arange(int(0.05 * SR)) / SR / 0.012)
        x = np.zeros(int(dur * SR))
        x[:len(body)] += 0.8 * body / np.abs(body).max()
        x += 0.8 * syn
        x[:len(slap)] += 0.6 * slap / np.abs(slap).max()
        x = room(x, 0.5, 0.15, 2500, 0.35)
    elif name == 'ka':
        n = int(dur * SR); t = np.arange(n) / SR
        click = band(RNG.standard_normal(n), 1800, 6000) * np.exp(-t / 0.006)
        wood = np.sin(2 * np.pi * 1150 * t) * np.exp(-t / 0.035) + 0.5 * np.sin(2 * np.pi * 2630 * t) * np.exp(-t / 0.02)
        x = click / np.abs(click).max() + 0.8 * wood
        x = room(x, 0.15, 0.04, 4000, 0.25)
    elif name == 'impact':                            # v4: de HIT (Jordi: 'moet meer impact'): lage odaiko + sub-val
        RNG = np.random.default_rng(5542)
        n = int(dur * SR)                              # + velslag + orkesthit (FluidR3 GM 55, E3+B3) + grote zaal
        body = render(116, 40, 1.6, 127)[:n]
        syn = membrane(125, 46, 0.06, 0.75, dur, modes=((1.0, 1.0, 1.0), (1.51, 0.5, 0.5), (2.3, 0.2, 0.3)))
        slap = band(RNG.standard_normal(int(0.2 * SR)), 200, 3000) * np.exp(-np.arange(int(0.2 * SR)) / SR / 0.05)
        orch = render(55, 52, 0.7, 127)[:n] + 0.7 * render(55, 59, 0.7, 120)[:n]
        x = np.zeros(n)
        x[:len(body)] += 0.9 * body / np.abs(body).max()
        x += 1.0 * syn
        x[:len(slap)] += 0.8 * slap / np.abs(slap).max()
        x[:len(orch)] += 0.55 * orch / np.abs(orch).max()
        x = room(x, 1.4, 0.45, 2500, 0.5)
    elif name == 'crash':
        x = render(None, 57, dur, 120, drum=True)[:int(dur * SR)]
        x = lowpass(x, 6000)
    if name in ('odaiko', 'taiko', 'impact'):
        x = np.tanh(2.2 * x / np.abs(x).max()) / np.tanh(2.2)
        x = band(x, 48, 20000)                       # geen sub onder 48 Hz (audiocheck: brom 37-61 Hz in de groove)
    x = x[:int(dur * SR)]
    fade = int(SR * 0.08); x[-fade:] *= np.linspace(1, 0, fade)
    return x / np.abs(x).max() * 0.97


# --------------------------------------------------------------------------------------------- formantsynthese -------
VOWELS = {   # (F1, F2, F3, F4) Hz en bandbreedtes, mannenstem (Peterson & Barney, afgerond)
    'a': ((730, 1090, 2440, 3400), (90, 110, 160, 250)),
    'o': ((520, 860, 2410, 3300), (80, 100, 150, 250)),
    'u': ((330, 800, 2240, 3200), (70, 100, 150, 250)),
    'e': ((530, 1840, 2480, 3500), (80, 120, 160, 250)),
}


def formant_gain(freq, F, B):
    g = np.ones_like(freq)
    for f, b in zip(F, B):
        g *= f * f / np.sqrt((f * f - freq * freq) ** 2 + (b * freq) ** 2)
    return g


def smooth_noise(n, rate_hz, sr):
    k = max(2, int(n * rate_hz / sr) + 2)
    pts = RNG.standard_normal(k)
    return np.interp(np.arange(n), np.linspace(0, n, k), pts)


def voice(f0_curve, vowel_curve, sr, tilt=1.1, breath=0.08, vib=(5.3, 0.012), jitter=0.005, fshift=1.0):
    """f0_curve: array Hz per sample; vowel_curve: array 0..1 tussen twee klinkers (tuple), of één klinker."""
    n = len(f0_curve)
    f0 = f0_curve * (1 + vib[1] * np.sin(2 * np.pi * vib[0] * np.arange(n) / sr + RNG.uniform(0, 6.28)))
    f0 *= 1 + jitter * smooth_noise(n, 12, sr)
    ph = 2 * np.pi * np.cumsum(f0) / sr
    va, vb, mix = vowel_curve
    Fa, Ba = VOWELS[va]; Fb, Bb = VOWELS[vb]
    x = np.zeros(n)
    kmax = int(sr * 0.47 / f0.min())
    for k in range(1, kmax + 1):
        fk = k * f0
        ga = formant_gain(fk, [f * fshift for f in Fa], Ba)
        gb = formant_gain(fk, [f * fshift for f in Fb], Bb)
        g = ga * (1 - mix) + gb * mix
        g *= (fk < sr * 0.47)
        x += g * np.sin(k * ph) / k ** tilt
    # ademruis door dezelfde klinkerkleur (gemiddeld): via FFT met de formantcurve van klinker a/b
    nz = RNG.standard_normal(n)
    spec = np.fft.rfft(nz); fr = np.fft.rfftfreq(n, 1 / sr) + 1
    env = formant_gain(fr, [f * fshift for f in Fa], Ba) * (1 - mix.mean()) + formant_gain(fr, [f * fshift for f in Fb], Bb) * mix.mean()
    nz = np.fft.irfft(spec * env / (fr / 300 + 1), n)
    x = x / (np.abs(x).max() + 1e-9) + breath * nz / (np.abs(nz).max() + 1e-9)
    return x


def group(nvoices, f0_curve, vowel, sr, detune=0.009, spread=0.012, **kw):
    out = np.zeros(len(f0_curve) + int(spread * sr) + 1)
    for v in range(nvoices):
        d = 2 ** (RNG.uniform(-detune, detune))
        off = int(RNG.uniform(0, spread) * sr)
        fs = RNG.uniform(0.95, 1.06)
        x = voice(f0_curve * d, vowel, sr, fshift=fs, **kw)
        out[off:off + len(x)] += x * RNG.uniform(0.75, 1.0)
    return out[:len(f0_curve)]


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def vox(name, sr):
    if name == 'vox_a':                                # bovenstem 'ha', A4, aanhoudend (loop)
        dur = 0.75; n = int(dur * sr); t = np.arange(n) / sr
        f0 = np.full(n, hz(69))
        mix = np.clip(t / 0.05, 0, 1) * 0.0
        x = group(4, f0, ('a', 'o', mix), sr, detune=0.006, breath=0.06, vib=(5.5, 0.010), tilt=1.15)
        x = x / np.abs(x).max()                       # geen 'h': legato gezongen (melisma), zachte inzet
        env = np.minimum(1, t / 0.015)
        x *= env
        key = 69
    elif name == 'vox_hu':                             # lage mannen-'hu', F#3, aanhoudend (loop)
        dur = 0.75; n = int(dur * sr); t = np.arange(n) / sr
        f0 = np.full(n, hz(54))
        x = group(5, f0, ('o', 'u', np.clip(t / 0.15, 0, 1) * 0.6), sr, detune=0.008, breath=0.10, vib=(5.0, 0.008), tilt=1.0)
        h = band(RNG.standard_normal(n), 600, 3500) * np.exp(-t / 0.02) * 0.6
        x = x / np.abs(x).max(); x += h * (t < 0.06)
        x *= np.minimum(1, t / 0.02)
        key = 54
    elif name == 'shout':                              # 'HOO!': glijdt F#3 -> A#3 (80 ms), o -> oe, valt aan het eind
        dur = 0.95; n = int(dur * sr); t = np.arange(n) / sr
        semis = -4 * np.exp(-t / 0.035) - 2.0 * np.clip((t - 0.62) / 0.33, 0, 1) ** 2
        f0 = hz(58) * 2 ** (semis / 12)
        mix = np.clip((t - 0.15) / 0.45, 0, 1) * 0.7
        x = group(6, f0, ('o', 'u', mix), sr, detune=0.012, spread=0.02, breath=0.14, vib=(4.5, 0.006), tilt=0.85,
                  jitter=0.012)
        h = band(RNG.standard_normal(n), 500, 4000) * np.exp(-t / 0.025) * 0.7
        x = x / np.abs(x).max(); x += h * (t < 0.08)
        x = np.tanh(1.8 * x) / np.tanh(1.8)                       # geperste, schreeuwende stem
        env = np.minimum(1, t / 0.015) * np.where(t > 0.55, np.exp(-(t - 0.55) / 0.17), 1.0)
        x *= env
        key = 58
    x = lowpass_sr(x, sr, 5200)
    return x / np.abs(x).max() * 0.97, key


def synth(rate):
    """v3: de synth van maat 9-12 ('TUDUDUDUUUU - TUDUDUDU', Jordi: 'het grootste gebrek') en de synthbas: twee
    bandbegrensde zaagtanden met perioden van 80 en 81 samples (21.024 Hz: 262,8 + 259,6 Hz, gemiddeld C4) plus een
    kwart blokgolf voor de 'buzz'. Loop = kgv(80, 81) = 6480 samples = exact (0,31 s, zweving 3,2 Hz = breed/ontstemd).
    Harmonischen tot ±4,5 kHz (op F4 gespeeld nog onder de Nyquist van de mixer)."""
    n = 80 * 81
    t = np.arange(n)
    x = np.zeros(n)
    for per, amp in ((80, 1.0), (81, 0.9)):
        f0 = rate / per
        for k in range(1, int(4500 / f0) + 1):
            g = amp / k * (1.0 if k * f0 < 2500 else np.exp(-(k * f0 - 2500) / 1500))
            x += g * np.sin(2 * np.pi * k * t / per)
            if k % 2:
                x += 0.25 * g * np.sin(2 * np.pi * k * t / per + 0.5)
    x = x / np.abs(x).max() * 0.97
    return x, 60, (0, n)


# v5: de lead van maat 9-12 is een synth-brass (koperachtige synth), geen kale zaagtand. Gemeten op de stem 'other'
# (alleen E3 klinkt in maat 9:2-9:7, de mix geeft hetzelfde profiel): harmonischen 1-8 = -6 -5 0 -10 -11 -10 -21 -17 dB
# (zwakke grondtoon, top op de 2e-3e harmonische = koperformant ±350-550 Hz), daarna vlak tot ±4 kHz (-18..-26 dB);
# toonhoogte stabiel (pyin: std 0,2 halve toon, geen vibrato), wel een zweving van 13-17 dB op 2,5-3,5 en 8-9 Hz
# = een ensemble van licht ontstemde stemmen. In maat 11-12 gaat het filter open: 1,6-4 kHz 6-8 dB sterker.
BRASS_H = [-4, -2, -1, -8, -11, -13, -17, -15, -20, -21, -20, -20, -22, -24, -25, -25, -26, -27, -28, -29,
           -30, -31, -32, -33, -35, -37, -39, -41]
BRASS_VOICES = ((129, 0.55), (130, 0.85), (131, 1.0), (132, 0.85), (133, 0.55))   # cycli per loop van 0,5 s


def brass(rate, bright):
    """Vijf ontstemde stemmen (258-266 Hz, +-26 cent; elke stem een heel aantal perioden in de loop van 10512
    samples = exact) met het gemeten harmonischenprofiel; aanzet 80 ms met een kleine val-in van onderen
    (-0,35 halve toon, zoals de E3 van maat 9) en een korte, heldere 'blaas'. bright: het open filter van maat 11-12."""
    rng = np.random.default_rng(5150 + bright)
    L = rate // 2
    A = int(0.08 * rate)
    n = A + L
    t = np.arange(n) / rate
    scoop = np.where(t < 0.06, -0.35 * (1 - t / 0.06) ** 2, 0.0)            # halve tonen
    ratio = 2 ** (scoop / 12)
    integ = np.concatenate([[0], np.cumsum(ratio[:-1])]) / rate             # integraal van de toonhoogteverhouding
    gain = np.array(BRASS_H, float)
    if bright:
        k = np.arange(1, len(gain) + 1)
        gain += 7 * np.clip((k - 4) / 4, 0, 1)
    x = np.zeros(n)
    for cyc, amp in BRASS_VOICES:
        f0 = cyc * rate / L                                                # Hz
        for k, g in enumerate(gain, 1):
            if k * f0 * 2 ** (5 / 12) > rate * 0.48:                       # tot F4 (+5) onder de Nyquist van de mixer
                break
            blast = 1 + 0.6 * (k > 4) * np.exp(-t / 0.05)                  # heldere aanblaas
            x += amp * 10 ** (g / 20) * blast * np.sin(2 * np.pi * k * f0 * integ + rng.uniform(0, 2 * np.pi))
    x *= np.minimum(1, t / 0.02)
    x = x / np.abs(x).max() * 0.97
    return x, 60, (A, n)


# v6: de climax-figuur van maat 11-12 (Jordi's neurie tapu_hum_climax.ogg). Gemeten in de mix (FFT per noot, t.o.v.
# het liggende akkoord in 10:12-10:15): A#5 h1 +8..+10 dB, h2 -13..-17, h3 -16..-18, h4 -19..-22 dB onder de grondtoon;
# E5 h2 -14..-16, h3 -19..-21 dB. Dus een zachte lead met een dominante grondtoon (bijna een driehoek/gefilterde zaag),
# geen koperformant. Grondtoon A5 (880 Hz, toets 81): tot F6 (+8) blijven 7 harmonischen onder de Nyquist van de mixer.
LEAD_H = [0, -12, -16, -20, -24, -27, -30]
LEAD_VOICES = ((438, 0.55), (440, 1.0), (442, 0.55))     # cycli per loop van 0,5 s: +-4 cent, zachte zweving (snel spel)


def lead(rate):
    rng = np.random.default_rng(7171)
    L = rate // 2
    A = int(0.03 * rate)
    n = A + L
    t = np.arange(n) / rate
    x = np.zeros(n)
    for cyc, amp in LEAD_VOICES:
        f0 = cyc * rate / L
        for k, g in enumerate(LEAD_H, 1):
            if k * f0 * 2 ** (8 / 12) > rate * 0.48:
                break
            blast = 1 + 0.8 * (k > 1) * np.exp(-t / 0.025)                 # korte heldere aanzet (snelle noten)
            x += amp * 10 ** (g / 20) * blast * np.sin(2 * np.pi * k * f0 * t + rng.uniform(0, 2 * np.pi))
    x *= np.minimum(1, t / 0.006)
    x = x / np.abs(x).max() * 0.97
    return x, 81, (A, n)


def lowpass_sr(x, sr, hi):
    f = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / sr)
    f[fr > hi] *= np.exp(-(fr[fr > hi] - hi) / 600)
    return np.fft.irfft(f, len(x))


# naam: (soort, lengte s, samplerate, loop)
SAMPLES = {
    'tapu_odaiko': ('drum', 1.1, 13379, False),
    'tapu_taiko':  ('drum', 0.7, 13379, False),
    'tapu_ka':     ('drum', 0.15, 13379, False),
    'tapu_crash':  ('drum', 1.3, 13379, False),
    'tapu_vox_a':  ('vox', 0.75, 16384, True),
    'tapu_vox_hu': ('vox', 0.75, 16384, True),
    'tapu_synth':  ('synth', 0, 21024, True),
    'tapu_impact': ('drum', 1.8, 13379, False),     # v4; achteraan + eigen seed: de andere samples blijven gelijk
    'tapu_brass':  ('brass', 0, 21024, True),       # v5: synth-brass-lead maat 9-12 (eigen seed)
    'tapu_brass_hi': ('brass_hi', 0, 21024, True),  # v5: idem, filter open (maat 11-12)
    'tapu_lead':   ('lead', 0, 21024, True),        # v6: climax-figuur maat 11-12 (eigen seed)
}


def main(only=None):
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    total = 0
    for name, (kind, dur, rate, loop) in SAMPLES.items():
        if only and name not in only:
            continue
        short = name[5:]
        if kind == 'drum':
            a = resample(drum(short, dur), SR, rate)
            key, lp = 60, None
        elif kind == 'synth':
            a, key, lp = synth(rate)
        elif kind == 'lead':
            a, key, lp = lead(rate)
        elif kind.startswith('brass'):
            a, key, lp = brass(rate, kind == 'brass_hi')
        else:
            a, key = vox(short, rate)
            lp = None
            if loop:
                a, lp = auto_loop(a, rate)
        write_wav(OUT + name + '.wav', a, rate, key, lp)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        total += len(a)
        print('%-12s %5d samples @ %5d Hz (%.2f s), grondtoon %d%s' % (name, len(a), rate, len(a) / rate, key,
                                                                       ', loop %d-%d' % lp if lp else ''))
    open(DATA, 'w').write(inc)
    print('totaal %.1f KB' % (total / 1024))


if __name__ == '__main__':
    main(sys.argv[1:] or None)

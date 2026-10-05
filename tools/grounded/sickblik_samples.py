#!/usr/bin/env python3
"""Project Grounded: de samples voor Battle! SickBlik (sb_*): een slap bass in vier articulaties (thumb, pop, dode
thumb, dode pop), funkgitaar (wah-chank, scratch, gedempte losse noot), clavinet, Rhodes-akkoorden, een hoornsectie
(trompet + tenorsax een octaaf lager in één sample = 1 kanaal), een 'talkbox'-lead en een paar drumgeluiden.

Bron: de GM-soundfont FluidR3 (fluidsynth), daarna bewerkt:
  - thumb: FluidR3 Slap Bass 1 (GM 36) + een eigen aanslag: het hoge deel (> 1,5 kHz) van de eerste ±12 ms extra
    versterkt (de 'klap' van de duim op de bovenste fret), lichte tanh-groom, lowpass 6 kHz (geen schelle zaag)
  - pop: FluidR3 Slap Bass 2 (GM 37) + een snap (2-5 kHz, ±8 ms) en een fretklik (ruis 2,5-5 kHz, 3 ms)
  - dead notes: dezelfde aanslag, maar de snaar is gedempt: na ±5 ms sterft alles in 12-20 ms (thumb: een doffe 'tock'
    met een vleugje toon, pop: een droge klik)
  - wah-chank: een E9-greep (G#3 D4 F#4 B4) van FluidR3 Clean Guitar door een wah die in 0,12 s opengaat ('wacka')
  - talkbox: zaagtand door formanten die van 'oe' naar 'aa' glijden (aanzet), daarna een exacte loop op 'aa'
Elke sample: anti-aliasfilter bij het omlaag resamplen, 8 bit volle schaal, smpl-chunk met grondtoon (+ loop).
Vereist: apt-get install fluidsynth fluid-soundfont-gm (zie MUZIEK.md).
Gebruik: python3 tools/grounded/sickblik_samples.py [--analyse]"""
import os, struct, subprocess, sys, tempfile, wave
import numpy as np
import mido
from scipy.signal import butter, sosfilt

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
SR = 44100

# naam: (stemmen [(GM-programma | 'drum', noot)], grondtoon voor de smpl-chunk, lengte in s, samplerate, loop, velocity)
SAMPLES = {
    'sb_slap_thumb':  ([(36, 33)], 33, 1.4, 22050, None, 120),           # A1; gespeeld E1-D3
    'sb_slap_pop':    ([(37, 45)], 45, 1.1, 22050, None, 124),           # A2; gespeeld E2-A3
    'sb_dead_thumb':  ([(36, 33)], 33, 0.12, 22050, None, 120),
    'sb_dead_pop':    ([(37, 45)], 45, 0.08, 22050, None, 124),
    'sb_gtr_wah_m9':  ([(27, 55), (27, 62), (27, 66), (27, 71)], 52, 0.32, 22050, None, 112),   # Em9 (zonder grondtoon)
    'sb_gtr_wah_9':   ([(27, 56), (27, 62), (27, 66), (27, 71)], 52, 0.32, 22050, None, 112),   # E9: op A gespeeld = A9
    'sb_gtr_scratch': ([(28, 56), (28, 62), (28, 66), (28, 71)], 52, 0.07, 22050, None, 110),
    'sb_gtr_mute':    ([(28, 52)], 52, 0.4, 22050, None, 118),
    'sb_clav':        ([(7, 60)], 60, 0.6, 22050, None, 118),
    'sb_rhodes_m9':   ([(4, 55), (4, 59), (4, 62), (4, 66)], 52, 1.6, 16000, None, 100),     # Em9 zonder grondtoon
    'sb_rhodes_13':   ([(4, 55), (4, 61), (4, 66), (4, 71)], 57, 1.6, 16000, None, 100),     # A13 zonder grondtoon
    'sb_horns':       ([(56, 64), (66, 52)], 64, 1.0, 22050, 'auto', 122),                     # trompet E4 + tenorsax E3
    'sb_horns_hi':    ([(56, 76), (66, 64)], 76, 1.0, 22050, 'auto', 122),                     # vanaf C5 (minder transponeren)
    'sb_pedal_hat':   ([('drum', 44)], 60, 0.2, 22050, None, 100),
    'sb_clap':        ([('drum', 39)], 60, 0.4, 22050, None, 110),
    # ---- v2 (Steely Dan-refreinen): elk akkoord = één sample (1 kanaal), rootless close voicings op klinkende hoogte;
    # de grondtoon in de smpl-chunk = de noot waarop de MIDI het akkoord speelt (de bas speelt de echte grondtoon)
    'sb_rh_cmaj9':    ([(4, 52), (4, 55), (4, 59), (4, 62)], 48, 1.8, 16000, None, 96),      # E G B D
    'sb_rh_b7alt':    ([(4, 57), (4, 63), (4, 67), (4, 74)], 47, 1.8, 16000, None, 96),      # A D# G D (7#9b13)
    'sb_rh_am9':      ([(4, 55), (4, 59), (4, 60), (4, 64)], 45, 1.8, 16000, None, 96),      # G B C E
    'sb_rh_d13':      ([(4, 54), (4, 59), (4, 60), (4, 64)], 50, 1.8, 16000, None, 96),      # F# B C E
    'sb_rh_gmu':      ([(4, 57), (4, 59), (4, 62), (4, 66)], 43, 1.8, 16000, None, 96),      # A B D F# ('mu')
    'sb_rh_fmaj7s11': ([(4, 57), (4, 59), (4, 64), (4, 67)], 41, 1.8, 16000, None, 96),      # A B E G
    'sb_rh_fsm7b5':   ([(4, 57), (4, 60), (4, 64), (4, 66)], 42, 1.8, 16000, None, 96),      # A C E F#
    'sb_rh_cmu':      ([(4, 60), (4, 62), (4, 64), (4, 67)], 48, 1.8, 16000, None, 96),      # C D E G ('Mu Major')
    # zachte blazers in close voicing (altsax boven, tenorsax + trombone eronder), aangehouden
    'sb_br_em9':      ([(57, 55), (66, 59), (66, 62), (65, 66)], 52, 2.4, 16000, None, 84),
    'sb_br_a13':      ([(57, 55), (66, 61), (66, 66), (65, 71)], 57, 2.4, 16000, None, 84),
    'sb_br_cmaj9':    ([(57, 52), (66, 55), (66, 59), (65, 62)], 48, 2.4, 16000, None, 84),
    'sb_br_b7alt':    ([(57, 57), (66, 63), (66, 67), (65, 74)], 47, 2.4, 16000, None, 84),
    'sb_br_am9':      ([(57, 55), (66, 59), (66, 60), (65, 64)], 45, 2.4, 16000, None, 84),
    'sb_br_d13':      ([(57, 54), (66, 59), (66, 60), (65, 64)], 50, 2.4, 16000, None, 84),
    'sb_br_gmu':      ([(57, 57), (66, 59), (66, 62), (65, 66)], 43, 2.4, 16000, None, 84),
    'sb_br_fmaj7s11': ([(57, 57), (66, 59), (66, 64), (65, 67)], 41, 2.4, 16000, None, 84),
    # leads: gedempte trompet (harmon-achtig, FluidR3 GM 59) en cleane jazzgitaar in octaven (GM 26, 'Wes'-octaven)
    'sb_mute_tpt':    ([(59, 67)], 67, 1.0, 22050, 'auto', 112),
    'sb_mute_tpt_hi': ([(59, 77)], 77, 1.0, 22050, 'auto', 112),
    'sb_jazz_oct':    ([(26, 55), (26, 67)], 55, 1.5, 22050, None, 112),
    'sb_jazz_oct_hi': ([(26, 64), (26, 76)], 64, 1.5, 22050, None, 112),
}

# vaste kopieën in grounded/ (eenmalig gekopieerd uit Heatran v2/v3, zodat SickBlik niet meeverandert met een ander thema)
STATIC = ['sb_closed_hat', 'sb_kick', 'sb_snare', 'sb_open_hat', 'sb_crash', 'sb_side_stick', 'sb_floor_tom']


def render(voices, dur, vel):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    chans = {}
    for prog, note in voices:
        if prog == 'drum':
            chans[prog] = 9
        elif prog not in chans:
            chans[prog] = len([c for c in chans.values() if c != 9])
            t.append(mido.Message('program_change', channel=chans[prog], program=prog, time=0))
    for prog, note in voices:
        t.append(mido.Message('note_on', channel=chans[prog], note=note, velocity=vel, time=0))
    for i, (prog, note) in enumerate(voices):
        t.append(mido.Message('note_off', channel=chans[prog], note=note, velocity=0, time=int(dur * 960) if i == 0 else 0))
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', str(SR), '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    a = a / 32768.0
    start = np.argmax(np.abs(a) > 0.002)
    return a[start:start + int((dur + 0.5) * SR)]


def bp(a, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], 'bandpass', fs=SR, output='sos'), a)


def lp(a, f, order=2):
    return sosfilt(butter(order, f, 'lowpass', fs=SR, output='sos'), a)


def hp(a, f, order=2):
    return sosfilt(butter(order, f, 'highpass', fs=SR, output='sos'), a)


def env_exp(n, tau, hold=0.0):
    t = np.arange(n) / SR
    return np.where(t < hold, 1.0, np.exp(-(t - hold) / tau))


def noise_burst(n, lo, hi, tau, seed):
    rng = np.random.default_rng(seed)
    return bp(rng.standard_normal(n), lo, hi) * env_exp(n, tau)


def norm(a):
    return a / max(1e-9, np.abs(a).max())


def slap(a, kind):
    """Eigen aanslag op de FluidR3-slap: thumb = klap > 1,5 kHz (12 ms) + groom; pop = snap 2-5 kHz + fretklik."""
    a = norm(a)
    n = len(a)
    if kind == 'thumb':
        a = a + 6.0 * hp(a, 1500) * env_exp(n, 0.020, 0.002)          # 2-5 kHz in de aanslag: ±14% (was 2%)
        a = a + 1.2 * noise_burst(n, 1800, 4500, 0.006, 1)            # de duim tegen de fret
        a = np.tanh(norm(a) * 2.0) / np.tanh(2.0)                     # groom (smerig, niet vervormd)
        a = lp(a, 6000)
    else:
        a = a + 2.8 * bp(a, 2000, 5000) * env_exp(n, 0.008, 0.002)
        a = a + 0.7 * noise_burst(n, 2500, 5000, 0.003, 2)            # snaar slaat terug op de fret
        a = np.tanh(norm(a) * 1.6) / np.tanh(1.6)
        a = lp(a, 7000)
    return hp(a, 30, 1)


def dead(a, kind):
    """Gedempte noot: dezelfde aanslag, dan sterft de snaar meteen (vinger van de linkerhand ligt erop)."""
    a = slap(a, kind)
    n = len(a)
    if kind == 'thumb':
        a = a * env_exp(n, 0.020, 0.004)
        a = a + 0.35 * noise_burst(n, 150, 900, 0.012, 3)             # doffe 'tock'
        a = lp(a, 3500)
    else:
        a = a * env_exp(n, 0.010, 0.003)
        a = a + 0.5 * noise_burst(n, 1500, 5000, 0.004, 4)            # droge klik
    return a


def wah(a):
    """Wah-chank: bandpass die in 0,12 s van 450 naar 1800 Hz opengaat (state-variable filter), korte greep."""
    n = len(a)
    a = norm(a)
    out = np.zeros(n)
    low = band = 0.0
    q = 1 / 3.5
    for i in range(n):
        t = i / SR
        fc = 450 * (1800 / 450) ** min(1.0, t / 0.12)
        f = 2 * np.sin(np.pi * fc / SR)
        high = a[i] - low - q * band
        band += f * high
        low += f * band
        out[i] = band
    out = 0.8 * norm(out) + 0.2 * a
    return out * env_exp(n, 0.05, 0.07)


def scratch(a):
    n = len(a)
    a = norm(a) * env_exp(n, 0.015, 0.01) + 0.6 * noise_burst(n, 1000, 4000, 0.012, 5)
    return a


def talkbox(f0_note=72, per=40, dur=0.5, loop_periods=8):
    """Zaagtand (harmonischen 1/k) door drie formanten; de eerste 90 ms glijden ze van 'oe' naar 'aa' (de 'w' van
    'wah'), daarna vast: loop van precies `loop_periods` perioden."""
    f0 = 440.0 * 2 ** ((f0_note - 69) / 12)
    rate = int(round(f0 * per))
    f0 = rate / per                                                   # exact `per` samples per periode
    n = int(dur * rate) // per * per
    t = np.arange(n) / rate
    g = np.clip(t / 0.09, 0, 1)
    g = g * g * (3 - 2 * g)
    F = [(300 + 450 * g, 80), (870 + 330 * g, 100), (2240 + 500 * g, 140)]   # 'oe' -> 'aa'
    a = np.zeros(n)
    for k in range(1, per // 2):
        fk = k * f0
        amp = 0.05
        for (fc, bw), w in zip(F, (1.0, 0.7, 0.35)):
            amp = amp + w / (1 + ((fk - fc) / bw) ** 2)
        if fk > 6000:
            amp = amp * np.exp(-(fk - 6000) / 1500)
        a += amp / k ** 0.6 * np.sin(2 * np.pi * fk * t)
    att = np.clip(t / 0.006, 0, 1)
    a = norm(a * att) * 0.97
    s = n - loop_periods * per
    return a, rate, (s, n), f0_note


def harmonic(f0_note=64, rate=22050, dur=1.6):
    """Flageolet op de bas (natuurlijke boventoon): bijna een sinus, een klokachtige aanzet (plukje ruis + een zwakke
    2e/3e harmonische die snel uitsterft) en een lange, zachte uitklinktijd. Grondtoon = `f0_note`."""
    f0 = 440.0 * 2 ** ((f0_note - 69) / 12)
    n = int(dur * SR)
    t = np.arange(n) / SR
    a = np.sin(2 * np.pi * f0 * t) * np.exp(-t / 0.55)
    a += 0.25 * np.sin(2 * np.pi * 2 * f0 * t) * np.exp(-t / 0.08)
    a += 0.12 * np.sin(2 * np.pi * 3 * f0 * t) * np.exp(-t / 0.04)
    a += 0.15 * noise_burst(n, 2000, 6000, 0.004, 6)
    a *= np.clip(t / 0.002, 0, 1)
    a = resample(norm(a), rate) * 0.97
    fade = int(rate * 0.05)
    a[-fade:] *= np.linspace(1, 0, fade)
    return a, rate, f0_note, None


def resample(a, dst):
    if dst < SR:
        f = np.fft.rfft(a)
        f[int(len(f) * 0.9 * dst / SR):] = 0
        a = np.fft.irfft(f, len(a))
    m = int(len(a) * dst / SR)
    return np.interp(np.arange(m) * SR / dst, np.arange(len(a)), a)


def auto_loop(a, rate, note, at=0.5, length=0.12, xfade=0.03):
    per = rate / (440.0 * 2 ** ((note - 69) / 12))
    best = min(range(max(1, int(length * rate / per)), int(2 * length * rate / per) + 1),
               key=lambda m: abs(m * per - round(m * per)))
    L = int(round(best * per))
    e = int(at * rate) + L
    s = e - L
    x = int(xfade * rate)
    w = np.linspace(0, 1, x)
    a = a.copy()
    a[e - x:e] = a[e - x:e] * (1 - w) + a[s - x:s] * w
    return a[:e], (s, e)


def write_wav(path, x, rate, key, loop):
    q = np.clip(np.round(x * 127), -128, 127).astype(np.int16) + 128
    data = q.astype(np.uint8).tobytes()
    fmt = struct.pack('<HHIIHH', 1, 1, rate, rate, 1, 8)
    smpl = struct.pack('<9I', 0, 0, int(1e9 / rate), key, 0, 0, 0, 1 if loop else 0, 0)
    if loop:
        smpl += struct.pack('<6I', 0, 0, loop[0], loop[1] - 1, 0, 0)
    chunks = b'fmt ' + struct.pack('<I', len(fmt)) + fmt + b'smpl' + struct.pack('<I', len(smpl)) + smpl
    chunks += b'data' + struct.pack('<I', len(data)) + data + (b'\0' if len(data) & 1 else b'')
    open(path, 'wb').write(b'RIFF' + struct.pack('<I', 4 + len(chunks)) + b'WAVE' + chunks)


def make(name):
    voices, key, dur, rate, loop, vel = SAMPLES[name]
    a = render(voices, max(dur, 0.3), vel)
    if name == 'sb_slap_thumb':
        a = slap(a, 'thumb')
    elif name == 'sb_slap_pop':
        a = slap(a, 'pop')
    elif name == 'sb_dead_thumb':
        a = dead(a, 'thumb')
    elif name == 'sb_dead_pop':
        a = dead(a, 'pop')
    elif name.startswith('sb_gtr_wah'):
        a = wah(a[:int(dur * SR)])
    elif name == 'sb_gtr_scratch':
        a = scratch(a[:int(dur * SR)])
    elif name.startswith('sb_mute_tpt'):
        a = lp(norm(a), 3800, 4)                                      # harmon-'zoem' > 5 kHz weg (schel in de mix)
    a = a[:int(dur * SR)]
    a = resample(a, rate)
    a = norm(a) * 0.97
    if loop == 'auto':
        a, loop = auto_loop(a, rate, key)
    else:
        fade = int(rate * min(0.05, dur / 4))
        a[-fade:] *= np.linspace(1, 0, fade)
    return a, rate, key, loop


def bands(a, rate, t0=0.0, t1=0.05):
    seg = a[int(t0 * rate):int(t1 * rate)]
    f = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
    fr = np.fft.rfftfreq(len(seg), 1 / rate)
    tot = f.sum() + 1e-12
    b = lambda lo, hi: 100 * f[(fr >= lo) & (fr < hi)].sum() / tot
    return '<200 %4.1f  200-1k %4.1f  1-2k %4.1f  2-5k %4.1f  >5k %4.1f' % (
        b(0, 200), b(200, 1000), b(1000, 2000), b(2000, 5000), b(5000, 1e6))


def main():
    analyse = '--analyse' in sys.argv
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    items = [(n, make(n)) for n in SAMPLES]
    a, rate, loop, key = talkbox()
    items.append(('sb_talkbox', (a, rate, key, loop)))
    items.append(('sb_bass_harm', harmonic()))
    for name, (a, rate, key, loop) in items:
        write_wav(OUT + name + '.wav', a, rate, key, loop)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-15s %6d samples @ %5d Hz, grondtoon %d%s' % (name, len(a), rate, key, ', loop' if loop else ''))
        if analyse:
            print('    aanslag 0-50 ms: ' + bands(a, rate) + '   |  50-200 ms: ' + bands(a, rate, 0.05, 0.2))
    for name in STATIC:            # vaste kopieën (niet gegenereerd): eigen drumgeluiden, los van andere thema's
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()

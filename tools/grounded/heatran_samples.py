#!/usr/bin/env python3
"""Project Grounded: de Heatran-samples (heatran_*), v4: 100% Kyuss (Blues for the Red Sun / Welcome to Sky Valley).

Jordi over v3: 'nog steeds veel te netjes, helder en vrolijk'. Zijn productieregels, hier letterlijk als keten:
  GITAAR (Josh Homme): schone gitaar op de NEK-pickup met de TONE-knop DICHT (2-polige lowpass 900 Hz vóór de
    fuzz; Homme speelde zo) -> asymmetrische, verzadigde fuzz (twee clipstadia met bias = ook even harmonischen)
    -> COCKED WAH (wahpedaal halverwege vastgezet: resonante bandpass rond 800 Hz, Q 4, nasaal/hol)
    -> 'Ampeg SVT/TubeWorks' basversterker + kast: lage shelf +7 dB < 160 Hz, middenboost +7 dB rond 700 Hz
    (500 Hz - 1 kHz), buisverzadiging, kast-lowpass 3,6 kHz (8-polig) + nog een 8-polige op 4 kHz: boven 4 kHz
    praktisch niets meer, geen twang.
  BAS (Scott Reeder): FluidR3 picked bass een octaaf onder de gitaar (C1 bij een C2-riff), zware tube-fuzz
    (asymmetrisch) met de schone grondtoon erbij (anders verdwijnt die in de fuzz), modderige middens rond 500 Hz,
    lowpass 2,4 kHz. Gelabeld een octaaf te hoog: dezelfde MIDI-noten als de gitaar klinken een octaaf lager.
  DRUMS: FluidR3 Power-kit; snare zonder 'crack' (lowpass 1,8 kHz), hihat/crash gruizig en dof.

Elke gitaar/bas/lead-noot heeft een EIGEN sample op zijn toonhoogte (keysplit `keysplit_heatran`, zie
heatran_theme.py), op 21.024 Hz = de mixfrequentie van de game: geen transpositie, dus de lowpass van 4 kHz blijft
4 kHz (een C2-sample op Bb2 zou zijn hele spectrum x1,8 omhoog schuiven). Aanhoudende noten hebben een gecrossfade
loop in het fuzz-sustain.

Rendert met fluidsynth, schrijft 8-bit WAV's met smpl-chunk; make maakt er .bin van.
Vereist: apt-get install fluidsynth fluid-soundfont-gm.  Gebruik: python3 tools/grounded/heatran_samples.py"""
import os, struct, subprocess, tempfile, wave
import numpy as np
import mido
from scipy.signal import butter, sosfilt, lfilter

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
DRUMKIT = 16                     # FluidR3 'Power'-kit
FS = 44100                       # bewerken op 44,1 kHz
RATE = 21024                     # = mixfrequentie van de game (src/m4a.c)

# toonhoogtes met een eigen sample (keysplit_heatran): de riffnoten in C-mineur-pentatonisch (+ b5 via F2)
RIFF_KEYS = (36, 39, 41, 43, 46, 48)      # C2 Eb2 F2 G2 Bb2 C3
LEAD_KEYS = (60, 65, 70)                  # C4 F4 Bb4 (cocked-wah-lead / feedback)

# naam: (GM-programma, noten (akkoord = tuple), lengte in s, loop, keten, label-toets)
SAMPLES = {}
for k in RIFF_KEYS:
    SAMPLES['heatran_pw_%d' % k] = (27, (k, k + 7, k + 12), 1.6, 'auto', 'homme', k)     # powerchord, 1 kanaal
    SAMPLES['heatran_nt_%d' % k] = (27, (k, k + 12), 1.6, 'auto', 'homme', k)            # riffnoot (+ octaaf)
    SAMPLES['heatran_pm_%d' % k] = (28, (k, k + 7), 0.55, None, 'mute', k)               # palm-mute
    SAMPLES['heatran_bs_%d' % k] = (34, k - 12, 1.6, 'auto', 'reeder', k)                # bas, octaaf lager
for k in LEAD_KEYS:
    SAMPLES['heatran_ld_%d' % k] = (27, k, 1.6, 'auto', 'lead', k)
SAMPLES.update({
    'heatran_ky_kick':      (128, 36, 0.6, None, 'kick', 60),
    'heatran_ky_snare':     (128, 38, 0.7, None, 'snare', 60),
    'heatran_ky_hat':       (128, 46, 0.5, None, 'hat', 60),
    'heatran_ky_crash':     (128, 49, 2.2, None, 'cymbal', 60),
    'heatran_ky_floor_tom': (128, 41, 0.9, None, 'tom', 60),
})
# v1-v3-samples die v4 niet meer gebruikt (worden verwijderd, ook uit direct_sound_data.inc)
OLD = ('heatran_fuzz_power', 'heatran_fuzz_low', 'heatran_fuzz_bass', 'heatran_fuzz_lead', 'heatran_muff_power',
       'heatran_muff_low', 'heatran_doom_low', 'heatran_mute_power', 'heatran_octfuzz_bass', 'heatran_closed_hat',
       'heatran_doom_power', 'heatran_doom_mute', 'heatran_svt_bass', 'heatran_doom_lead', 'heatran_warm_clean',
       'heatran_ride', 'heatran_china')
# NIET weggooien: heatran_kick/snare/crash/floor_tom/open_hat/side_stick (v3, FluidR3 Power-kit) zitten ook in de
# drumkit van SickBlik (drumsets/sickblik.inc); v4 heeft eigen drums (heatran_ky_*), de v3-bestanden blijven staan.


def render(prog, note, dur, vel=112):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    ch = 9 if prog >= 128 else 0
    notes = note if isinstance(note, tuple) else (note,)
    t.append(mido.Message('program_change', channel=ch, program=DRUMKIT if ch == 9 else prog, time=0))
    for n in notes:
        t.append(mido.Message('note_on', channel=ch, note=n, velocity=vel, time=0))
    for i, n in enumerate(notes):
        t.append(mido.Message('note_off', channel=ch, note=n, velocity=0, time=int(dur * 960) if i == 0 else 0))
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', str(FS), '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    return a / 32768.0


# ---- filters -----------------------------------------------------------------------------------------------------
def sos(kind, f, order=2):
    return butter(order, f, kind, fs=FS, output='sos')


def biquad(kind, f0, q, gain_db=0.0):
    """RBJ-cookbook: 'bp' (bandpass, piek 0 dB), 'peak', 'lowshelf'."""
    A = 10 ** (gain_db / 40)
    w = 2 * np.pi * f0 / FS
    al = np.sin(w) / (2 * q)
    c = np.cos(w)
    if kind == 'bp':
        b = [al, 0, -al]; a = [1 + al, -2 * c, 1 - al]
    elif kind == 'peak':
        b = [1 + al * A, -2 * c, 1 - al * A]; a = [1 + al / A, -2 * c, 1 - al / A]
    else:   # lowshelf, S = 1
        sq = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) - (A - 1) * c + sq), 2 * A * ((A - 1) - (A + 1) * c), A * ((A + 1) - (A - 1) * c - sq)]
        a = [(A + 1) + (A - 1) * c + sq, -2 * ((A - 1) + (A + 1) * c), (A + 1) + (A - 1) * c - sq]
    return np.array(b) / a[0], np.array(a) / a[0]


def bqf(x, kind, f0, q, gain_db=0.0):
    b, a = biquad(kind, f0, q, gain_db)
    return lfilter(b, a, x)


def norm(a):
    return a / max(1e-9, np.abs(a).max())


# ---- de ketens -----------------------------------------------------------------------------------------------------
def neck_tone_closed(a):
    """Nek-pickup (warm, veel grondtoon) met de toonknop dicht: 2-polige lowpass 900 Hz + 1-polige 1,5 kHz."""
    a = sosfilt(sos('lowpass', 900, 2), sosfilt(sos('lowpass', 1500, 1), a))
    return norm(a)


def fuzz(a, gain=45.0, bias=0.35):
    """Asymmetrische, verzadigde fuzz: twee clipstadia met bias (even + oneven harmonischen), lowpass ertussen."""
    a = sosfilt(sos('highpass', 35, 1), a)
    a = np.tanh(a * gain + bias) - np.tanh(bias)
    a = sosfilt(sos('lowpass', 2500, 1), a)
    a = np.tanh(norm(a) * 5.0 - 0.2) + np.tanh(0.2)
    return norm(sosfilt(sos('highpass', 30, 1), a))


def cocked_wah(a, f0=800.0, q=4.0, dry=0.9, gain=2.4):
    """Wahpedaal vastgezet in het midden: resonante bandpass (de nasale 'wah'-piek, +8 dB boven de rest) bovenop
    het droge signaal (een echte wah laat de lage tonen niet helemaal weg)."""
    return dry * a + gain * bqf(a, 'bp', f0, q)


def svt(a, cut=3600.0, drive=1.8):
    """Ampeg SVT / TubeWorks + kast: lage shelf +11 dB < 220 Hz, middenboost +6 dB rond 700 Hz (500 Hz-1 kHz),
    buisverzadiging, steile kast-lowpass (8-polig op 3,6 kHz) + 8-polig op 4 kHz: boven 4 kHz niets."""
    a = norm(a)
    a = bqf(a, 'lowshelf', 220, 0.7, 11.0)
    a = bqf(a, 'peak', 700, 0.9, 6.0)
    a = np.tanh(norm(a) * drive)
    a = sosfilt(sos('lowpass', cut, 8), a)
    a = sosfilt(sos('lowpass', 4000, 8), a)
    return sosfilt(sos('highpass', 32, 2), a)


def chain(kind, a, note):
    if kind == 'homme':                          # nek + toon dicht -> fuzz -> cocked wah -> SVT
        n = neck_tone_closed(a)                  # (de schone grondtoon lekt mee, zoals bij een echte SVT-rig)
        return svt(cocked_wah(fuzz(n) + 0.8 * norm(sosfilt(sos('lowpass', 200, 2), n))))
    if kind == 'mute':                           # palm-mute: zelfde keten, minder fuzz, snaar sterft snel
        env = np.exp(-np.arange(len(a)) / FS / 0.10)
        a = fuzz(neck_tone_closed(a * env), 18.0)
        a = svt(cocked_wah(a), 3000)
        return a * np.exp(-np.arange(len(a)) / FS / 0.20)
    if kind == 'lead':                           # lead/feedback: de wah nog smaller en hoger (snarl), kast 3,4 kHz
        return svt(cocked_wah(fuzz(neck_tone_closed(a), 60.0), 900.0, 5.5, 0.6, 3.0), 3400)
    if kind == 'reeder':                         # bas: tube-fuzz + schone grondtoon, modder rond 500 Hz
        a = norm(sosfilt(sos('lowpass', 1200, 2), a))
        clean = norm(sosfilt(sos("lowpass", 160, 2), a))
        d = np.tanh(a * 16.0 + 0.3) - np.tanh(0.3)
        d = norm(sosfilt(sos('highpass', 40, 1), d))
        d = bqf(d, "peak", 500, 0.8, 8.0)
        d = sosfilt(sos('lowpass', 2400, 8), d)
        return sosfilt(sos('highpass', 28, 2), norm(d) + 0.55 * clean)
    if kind == 'kick':                           # zware kick: laag erbij, geen klik
        a = bqf(norm(a), 'lowshelf', 90, 0.7, 4.0)
        return sosfilt(sos('lowpass', 2500, 4), np.tanh(norm(a) * 1.5))
    if kind == 'snare':                          # doffe snare: lichaam, geen crack/sis
        a = np.tanh(norm(a) * 2.0)
        a = bqf(a, 'peak', 200, 1.0, 4.0)
        return sosfilt(sos('lowpass', 1800, 4), a)
    if kind == 'tom':
        return sosfilt(sos('lowpass', 1500, 4), norm(a))
    if kind == 'hat':                            # gruizig, dof
        a = np.tanh(norm(a) * 2.0)
        return sosfilt(sos('lowpass', 5000, 4), a)
    if kind == 'cymbal':
        a = np.tanh(norm(a) * 2.0)
        return sosfilt(sos('lowpass', 5000, 4), a)
    return a


def resample(a, src, dst):
    if dst < src:                                                    # anti-alias
        f = np.fft.rfft(a)
        f[int(len(f) * 0.9 * dst / src):] = 0
        a = np.fft.irfft(f, len(a))
    n = int(len(a) * dst / src)
    return np.interp(np.arange(n) * src / dst, np.arange(len(a)), a)


def auto_loop(a, rate, period):
    """Loop in het sustaindeel van een geheel aantal perioden (± het best passende), laatste 40% gecrossfade met wat
    vóór het loopbegin staat (geen klik bij de terugsprong)."""
    s = int(len(a) * 0.40)
    k = max(1, round(0.30 * rate / period))
    cands = [int(round(j * period)) for j in range(k - 2, k + 3)]
    n = int(rate * 0.04)
    best = max(cands, key=lambda L: np.dot(a[s:s + n], a[s + L:s + L + n]) / (np.linalg.norm(a[s + L:s + L + n]) + 1e-9))
    e = s + best
    f = int(best * 0.4)
    w = np.linspace(0, 1, f)
    a = a[:e].copy()
    a[e - f:e] = a[e - f:e] * (1 - w) + a[s - f:s] * w
    return a, (s, e)


def write_wav(path, x, rate, key, loop):
    q = np.clip(np.round(x * 127), -128, 127).astype(np.int16) + 128
    data = q.astype(np.uint8).tobytes()
    fmt = struct.pack('<HHIIHH', 1, 1, rate, rate, 1, 8)
    nloops = 1 if loop else 0
    smpl = struct.pack('<9I', 0, 0, int(1e9 / rate), key, 0, 0, 0, nloops, 0)
    if loop:
        smpl += struct.pack('<6I', 0, 0, loop[0], loop[1] - 1, 0, 0)
    chunks = b'fmt ' + struct.pack('<I', len(fmt)) + fmt + b'smpl' + struct.pack('<I', len(smpl)) + smpl
    chunks += b'data' + struct.pack('<I', len(data)) + data + (b'\0' if len(data) & 1 else b'')
    open(path, 'wb').write(b'RIFF' + struct.pack('<I', 4 + len(chunks)) + b'WAVE' + chunks)


def make(name, out=OUT):
    prog, note, dur, loop, kind, key = SAMPLES[name]
    a = render(prog, note, dur + 0.3)
    start = np.argmax(np.abs(a) > 0.002)                           # stilte vooraan weg
    a = a[start:start + int(dur * FS)]
    low = min(note) if isinstance(note, tuple) else note
    a = chain(kind, a, low)
    a = resample(a, FS, RATE)
    a = norm(a) * 0.97                                             # 8 bit: volle schaal
    if loop == 'auto':
        a, loop = auto_loop(a, RATE, RATE / (440 * 2 ** ((low - 69) / 12)))
    else:
        fade = int(RATE * 0.04)
        a[-fade:] *= np.linspace(1, 0, fade)
    write_wav(out + name + '.wav', a, RATE, key, loop)
    return len(a)


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    for old in OLD:
        inc = inc.replace('\n\t.align 2\nDirectSoundWaveData_%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (old, old), '')
        for ext in ('.wav', '.bin'):
            if os.path.exists(OUT + old + ext):
                os.remove(OUT + old + ext)
    total = 0
    for name in SAMPLES:
        n = make(name)
        total += n
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-20s %-7s %6d samples' % (name, SAMPLES[name][4], n))
    print('totaal %.0f KB' % (total / 1024))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()

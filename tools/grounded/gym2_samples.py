#!/usr/bin/env python3
"""Project Grounded: samples voor de gymleider-remixes 651-654 (tools/grounded/gym_remixes2.py), voorvoegsel gym2_.

Norman (blockbuster-tv-orkest), Winona (bubblegum-dancepop), Tate & Liza (psytrance), Wallace (Franse lounge/bossa).
Alleen wat de game zelf niet heeft; de rest (strijkers/hoorn/trompet/piano/pauken/taiko/koor/accordeon/fluit/nylon/
909-clap/hihats/glockenspiel/synthbas) komt uit de vanilla-samples in sound/direct_sound_samples/.

Twee soorten:
  FLUID: gerenderd met fluidsynth uit FluidR3 (GM-programma, of ('drum', kit, noot) = GM-drumkanaal met kitpreset);
         een akkoord/voicing of octaaf = meerdere (programma, noot)-paren in één sample = één kanaal in de game.
  SYNTH: gesynthetiseerd (psy-kick/-bas/-leads, pop-lead/-pluck, zap): exacte loops van hele perioden.
Gebruik: python3 tools/grounded/gym2_samples.py   (hulpjes uit sample_utils.py, geen samples van andere thema's)"""
import os, subprocess, sys, tempfile, wave
import numpy as np
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sample_utils import resample, auto_loop, write_wav

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
FS = 44100

# naam: (lijst van (programma, noot) of ('drum', kitpreset, noot), lengte in s, loop, label-toets, samplerate,
#        velocity, lowpass in Hz of None, gain-curve)
FLUID = {
    # --- Norman: blockbuster-tv-orkest ---
    'gym2_cello':       ([(42, 60)], 1.3, True, 60, 22050, 112, None),          # epische cello (melodie)
    'gym2_ostinato':    ([(42, 48), (43, 36)], 0.34, False, 36, 18000, 124, None),  # cello + contrabas in octaven, kort
    'gym2_braam':       ([(57, 48), (57, 55), (60, 60), (61, 48)], 1.5, False, 48, 18000, 122, 5000),  # koper-'braam' C3+G3+C4
    # --- Winona: bubblegum-dancepop ---
    'gym2_pop_stab':    ([(62, 60), (62, 67), (62, 74)], 0.40, False, 60, 22050, 118, 7000),   # synthbrass sus2 (C G D)
    'gym2_pop_stab5':   ([(62, 60), (62, 67), (62, 72)], 0.40, False, 60, 22050, 118, 7000),   # synthbrass kwint+octaaf
    'gym2_pop_brass':   ([(62, 60)], 1.0, True, 60, 22050, 112, 7000),           # synthbrass, enkele noot (melodie)
    # --- Wallace: Franse lounge ---
    'gym2_vibes':       ([(11, 72)], 1.8, False, 72, 22050, 100, None),          # vibrafoon
    'gym2_rhodes':      ([(4, 60)], 1.5, False, 60, 22050, 96, None),            # Rhodes (melodie/pianodelen)
    'gym2_rh_dom':      ([(4, 67), (4, 69), (4, 70), (4, 74)], 1.4, False, 60, 22050, 84, None),   # C13 zonder 1 en 3 (G A Bb D): past bij E én F in de melodie
    'gym2_rh_maj':      ([(4, 64), (4, 69), (4, 71), (4, 74)], 1.4, False, 60, 22050, 84, None),   # Cmaj13 zonder 1 en 5 (E A B D): past bij de #11 (Bb-lydisch)
    'gym2_rh_min':      ([(4, 63), (4, 67), (4, 70), (4, 74)], 1.4, False, 60, 22050, 84, None),   # Cm9 zonder grondtoon
    'gym2_rh_sus':      ([(4, 65), (4, 67), (4, 70), (4, 74)], 1.4, False, 60, 22050, 84, None),   # C9sus4 (Bb/C)
    'gym2_upright':     ([(32, 36)], 1.3, False, 36, 16000, 110, None),          # contrabas (getokkeld)
    'gym2_flugel':      ([(56, 67)], 1.2, True, 67, 22050, 70, 3200),            # zachte trompet = bugel
    'gym2_brush_tap':   ([('drum', 40, 38)], 0.45, False, 60, 18000, 110, None),
    'gym2_brush_swirl': ([('drum', 40, 40)], 0.60, False, 60, 18000, 110, None),
    'gym2_side_stick':  ([('drum', 40, 37)], 0.25, False, 60, 18000, 110, None),
    'gym2_soft_kick':   ([('drum', 40, 36)], 0.40, False, 60, 18000, 100, None),
    'gym2_ride':        ([('drum', 40, 51)], 1.0, False, 60, 18000, 96, None),
    # (v0.9.103: concert-basdrum, lage tom, pop-kick, shaker en de Winona v2-celesta/-pads verwijderd: geen nummer
    # gebruikt ze meer; ROM-ruimte)
}
# ronde 2, Norman v2: gelaagde akkoorden uit de échte Emerald-samples (Jordi: 'Trumpet / Brass Section samples',
# 'Pizzicato Strings'). Elk akkoord = de vanilla-sample per toon getransponeerd en opgeteld (13.379 Hz, 8 bit) = één
# kanaal per stoot. ('h', noot) = hoorn (sc88pro_french_horn_60) als fundament, anders trompet (keysplit 60/72/84)
# of pizzicato. Gelabeld op C4 (60); de remix speelt ze op de grondtoon (-6..+5 rond C4, dus nooit onder F#3).
LAYER = {
    'gym2_nb_dom': ('brass', [('h', 60), 67, 70, 74]),       # C G Bb D (C9 zonder terts: past bij E én F in de melodie)
    'gym2_nb_maj': ('brass', [('h', 60), 64, 69, 74]),       # 6/9 (big band)
    'gym2_nb_min': ('brass', [('h', 60), 67, 70, 75]),       # m7 (Bb-mineur in maat 58-59, C-mineur in het B-deel)
    'gym2_nb_sus': ('brass', [('h', 60), 65, 70, 74]),       # 9sus4
    'gym2_nb_5':   ('brass', [('h', 60), 67, 72]),
    'gym2_np_dom': ('pizz', [48, 60, 67, 70]),
    'gym2_np_maj': ('pizz', [48, 64, 67, 69]),
    'gym2_np_min': ('pizz', [48, 60, 63, 67]),
    'gym2_np_sus': ('pizz', [48, 60, 65, 70]),
    'gym2_np_5':   ('pizz', [48, 60, 67]),
}
SRC_DIR = 'sound/direct_sound_samples/'
# Tate & Liza v2: zaagtand voor het PSG-golfkanaal (één periode over 32 stappen = klinkt een octaaf lager dan
# genoteerd, zoals ProgrammableWaveData_8; zo kan de psy-bas onder C2 zonder dat m4a hem op C2 klemt)
WAVES = {'gym2_saw': [int(round(15 - 15 * i / 31)) for i in range(32)]}

SYNTH = ['gym2_pop_lead', 'gym2_pop_pluck', 'gym2_psy_bass', 'gym2_psy_lead_a', 'gym2_psy_lead_b',
         'gym2_psy_acid']   # gym2_psy_kick en gym2_psy_zap: ongebruikt, v0.9.103 verwijderd


def render(notes, dur, vel):
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    on = []
    for k, n in enumerate(notes):
        if n[0] == 'drum':
            ch, prog, key = 9, n[1], n[2]
        else:
            ch, prog, key = k % 8 if k % 8 != 9 else 10, n[0], n[1]
        t.append(mido.Message('program_change', channel=ch, program=prog, time=0))
        on.append((ch, key))
    for ch, key in on:
        t.append(mido.Message('note_on', channel=ch, note=key, velocity=vel, time=0))
    for i, (ch, key) in enumerate(on):
        t.append(mido.Message('note_off', channel=ch, note=key, velocity=0, time=int(dur * 960) if i == 0 else 0))
    t.append(mido.MetaMessage('end_of_track', time=960))
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', str(FS), '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    return a / 32768.0


def lowpass(a, rate, fc):
    f = np.fft.rfft(a)
    fr = np.fft.rfftfreq(len(a), 1 / rate)
    f *= 1 / np.sqrt(1 + (fr / fc) ** 8)
    return np.fft.irfft(f, len(a))


def periodic(harm, per, cycles=4):
    """Golf uit harmonischen {k: amplitude} met precies `cycles` perioden van `per` samples (naadloze loop)."""
    t = np.arange(per * cycles) / per * 2 * np.pi
    a = np.zeros_like(t)
    for k, amp in harm.items():
        a += amp * np.sin(k * t)
    return a / np.abs(a).max() * 0.97


def synth(name):
    """-> (golf, samplerate, label-toets, loop)"""
    if name == 'gym2_pop_lead':
        # glanzende poplead: zaagtand + blokgolf (50%) met zachte bovenkant, loop van 4 perioden op C5
        per = 32
        h = {k: (1 / k) * (1.0 if k <= 8 else np.cos((k - 8) / 8 * np.pi / 2) ** 2) for k in range(1, 16)}
        for k in range(1, 16, 2):
            h[k] += 0.6 / k
        a = periodic(h, per, 8)
        return a, int(round(523.2511 * per)), 72, (0, len(a))
    if name == 'gym2_pop_pluck':
        # pluk: blokgolf (25%) met snelle filter- en volumedaling, eenmalig (C5)
        rate = 22050
        n = int(rate * 0.45)
        tt = np.arange(n) / rate
        ph = 2 * np.pi * 523.2511 * tt
        a = np.zeros(n)
        for k in range(1, 20):
            amp = np.sin(np.pi * k * 0.25) / k
            a += amp * np.sin(k * ph) * np.exp(-tt * (4 + 2.2 * k))
        a *= np.minimum(1, tt / 0.002)
        return a / np.abs(a).max() * 0.97, rate, 72, None
    if name == 'gym2_psy_kick':
        # psytrance-kick: korte sinus die van 190 naar 48 Hz zakt + klik; strak (geen staart die de rollende bas raakt)
        rate = 18000
        n = int(rate * 0.20)
        tt = np.arange(n) / rate
        f = 48 + 142 * np.exp(-tt / 0.022)
        ph = 2 * np.pi * np.cumsum(f) / rate
        a = np.sin(ph) * np.exp(-tt / 0.075) * np.minimum(1, (0.20 - tt) / 0.03)
        rng = np.random.default_rng(7)
        a += 0.35 * rng.standard_normal(n) * np.exp(-tt / 0.002)
        a = np.tanh(1.6 * a)
        return a / np.abs(a).max() * 0.97, rate, 60, None
    if name == 'gym2_psy_bass':
        # rollende psybas: zaagtand C2 met snel sluitend laagdoorlaatfilter (pluk 'dum'), 95 ms, geen loop
        rate = 16000
        n = int(rate * 0.095)
        tt = np.arange(n) / rate
        f0 = 65.406
        a = np.zeros(n)
        for k in range(1, 40):
            fk = k * f0
            cut = 180 + 1400 * np.exp(-tt / 0.018)
            a += (1 / k) * np.sin(2 * np.pi * fk * tt) / np.sqrt(1 + (fk / cut) ** 4)
        a *= np.minimum(1, tt / 0.003) * np.minimum(1, (0.095 - tt) / 0.012)
        a = np.tanh(1.4 * a / np.abs(a).max())
        return a / np.abs(a).max() * 0.97, rate, 36, None
    if name == 'gym2_psy_lead_a':
        # Tate: acid-zaagtand met resonantiepiek rond de 3e-4e harmonische ('squelch'), loop 4 perioden op C5
        per = 32
        h = {k: (1 / k) * (1 + 2.0 * np.exp(-((k - 3.5) / 1.1) ** 2)) * (1 if k < 8 else 0.35) for k in range(1, 14)}
        a = periodic(h, per, 8)
        return a, int(round(523.2511 * per)), 72, (0, len(a))
    if name == 'gym2_psy_lead_b':
        # Liza: holle blokgolf (oneven harmonischen) met een formant rond de 3e: ander timbre, zelfde register
        per = 32
        h = {k: (1 / k) * (1 + 1.6 * np.exp(-((k - 3) / 1.0) ** 2)) for k in range(1, 16, 2)}
        a = periodic(h, per, 8)
        return a, int(round(523.2511 * per)), 72, (0, len(a))
    if name == 'gym2_psy_zap':
        # 'zap': sinus die in 140 ms van 2400 naar 160 Hz duikt (laser), eenmalig
        rate = 18000
        n = int(rate * 0.14)
        tt = np.arange(n) / rate
        f = 160 + 2240 * np.exp(-tt / 0.03)
        ph = 2 * np.pi * np.cumsum(f) / rate
        a = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.exp(-tt / 0.06) * np.minimum(1, tt / 0.002)
        return a / np.abs(a).max() * 0.97, rate, 60, None
    if name == 'gym2_psy_acid':
        # 303-achtige acid-noot: zaagtand C3 door een resonant filter dat in 160 ms dichtgaat (de 'wauw'), eenmalig
        rate = 18000
        n = int(rate * 0.16)
        tt = np.arange(n) / rate
        f0 = 130.81
        a = np.zeros(n)
        for k in range(1, 60):
            fk = k * f0
            if fk > rate * 0.45:
                break
            cut = 300 + 2600 * np.exp(-tt / 0.045)
            res = 1 + 3.0 * np.exp(-((fk - cut) / (0.25 * cut)) ** 2)
            a += (1 / k) * np.sin(2 * np.pi * fk * tt) * res / np.sqrt(1 + (fk / cut) ** 6)
        a *= np.minimum(1, tt / 0.002) * np.minimum(1, (0.16 - tt) / 0.02)
        a = np.tanh(1.5 * a / np.abs(a).max())
        return a / np.abs(a).max() * 0.97, rate, 48, None
    raise ValueError(name)


def read_gba_wav(name):
    """Vanilla-sample -> (golf -1..1, samplerate, toets, loop of None) uit de wav (8 bit + smpl-chunk)."""
    import struct
    d = open(SRC_DIR + name + '.wav', 'rb').read()
    i, rate, key, loop, data = 12, None, 60, None, None
    while i < len(d) - 8:
        cid, sz = d[i:i + 4], struct.unpack('<I', d[i + 4:i + 8])[0]
        body = d[i + 8:i + 8 + sz]
        if cid == b'fmt ':
            rate = struct.unpack('<I', body[4:8])[0]
        elif cid == b'smpl':
            v = struct.unpack('<9I', body[:36])
            key = v[3]
            if v[7]:
                lp = struct.unpack('<6I', body[36:60])
                loop = (lp[2], lp[3] + 1)
        elif cid == b'data':
            data = (np.frombuffer(body, np.uint8).astype(float) - 128) / 128
        i += 8 + sz + (sz & 1)
    return data, rate, key, loop


def layer(kind, notes, R=13379):
    """Akkoord uit vanilla-samples: per toon de sample (zoals de keysplit hem kiest) getransponeerd naar R."""
    dur = 1.0 if kind == 'brass' else 0.45
    n_out = int(R * dur)
    mix = np.zeros(n_out)
    for nt in notes:
        horn = isinstance(nt, tuple)
        m = nt[1] if horn else nt
        if kind == 'pizz':
            src = 'sc88pro_pizzicato_strings'
        elif horn:
            src = 'sc88pro_french_horn_60'
        else:
            src = 'sc88pro_trumpet_60' if m <= 66 else ('sc88pro_trumpet_72' if m <= 78 else 'sc88pro_trumpet_84')
        a, r, k, lp = read_gba_wav(src)
        eff = r * 2 ** ((m - k) / 12)                       # samples per seconde waarmee deze toon klinkt
        need = int(dur * eff) + 8
        if lp and len(a) < need:                            # sustain via de loop van de vanilla-sample
            reps = (need - lp[0]) // (lp[1] - lp[0]) + 1
            a = np.concatenate([a[:lp[0]]] + [a[lp[0]:lp[1]]] * reps)
        a = resample(a[:need], eff, R)[:n_out]
        mix[:len(a)] += a * (0.8 if horn else 1.0)
    tt = np.arange(n_out) / R
    if kind == 'brass':                                     # sforzando-stoot: 0,12 s vol, dan zakken naar ±45%
        env = np.where(tt < 0.12, 1.0, 0.45 + 0.55 * np.exp(-(tt - 0.12) / 0.18))
    else:                                                   # pizzicato: snelle natuurlijke uitsterving
        env = np.exp(-tt / 0.11)
    mix *= env
    fade = int(R * 0.04)
    mix[-fade:] *= np.linspace(1, 0, fade)
    return mix / np.abs(mix).max() * 0.97, R


# ---- ronde 3 (v3): Winona (donkere dance pop / hyperpop) en Tate & Liza (Goa/psytrance) ------------------------
# Jordi: beide klonken als 'kermis/circus'. Alle begeleiding opnieuw, alleen synths/drums uit het genre: geen
# blazers, fluitjes, klokjes, piano. Gelust = exact periodiek (hele perioden per stem, detune als (n+1)/n), zodat er
# geen klik in de loop zit. Nieuwe namen (gym2_w_*, gym2_tl_*): de v2-samples blijven byte-identiek.
SYNTH3 = ['gym2_w_saw', 'gym2_w_saw_dark', 'gym2_w_reese', 'gym2_w_stab_min', 'gym2_w_stab_maj', 'gym2_w_stab_sus',
          'gym2_w_stab_5', 'gym2_w_snare', 'gym2_tl_pluck', 'gym2_tl_pluck_b', 'gym2_tl_lead', 'gym2_tl_pad_min',
          'gym2_tl_pad_maj']
# akkoordstoten (Winona): intervallen boven de grondtoon (gelabeld op C4); de remix speelt ze op de grondtoon
W_STABS = {'min': (0, 3, 7, 10, 12), 'maj': (0, 4, 7, 12, 14), 'sus': (0, 5, 7, 10, 12), '5': (0, 7, 12)}
# pads (Tate & Liza): reine stemming (gehele verhoudingen = exacte loop): mineur 10:12:15, majeur 4:5:6 (x2 = 8:10:12)
TL_PADS = {'min': (20, 24, 30), 'maj': (16, 20, 24)}


def saw_loop(per, cycles, cutoff_h, drive=0.0, square=False):
    """Bandbegrensde zaagtand(en) als exacte loop: lengte per x cycles[0]; stem j doet cycles[j] perioden.
    cutoff_h = harmonische waarop een zacht laagdoorlaatfilter (4e orde) begint."""
    L = per * cycles[0]
    t = np.arange(L) / L * 2 * np.pi
    a = np.zeros(L)
    for c in cycles:
        kmax = int(per * cycles[0] / c * 0.45)
        for k in range(1, kmax):
            if square and k % 2 == 0:
                continue
            a += (1 / k) / np.sqrt(1 + (k / cutoff_h) ** 4) * np.sin(k * c * t + 1.7 * k * c / cycles[0])
    a /= np.abs(a).max()
    if drive:
        a = np.tanh(drive * a) / np.tanh(drive)
    return a / np.abs(a).max() * 0.97


def chord_oneshot(freqs, rate, dur, cut0, cut1, tau_cut, tau_amp, detune=0.006, drive=1.6, square=False, hp=0, res=0.0):
    """Eenmalige akkoordstoot/pluk: per toon twee licht ontstemde zaagtanden met een sluitend filter."""
    n = int(rate * dur)
    tt = np.arange(n) / rate
    cut = cut1 + (cut0 - cut1) * np.exp(-tt / tau_cut)
    a = np.zeros(n)
    for f0 in freqs:
        for d in (1 - detune, 1 + detune):
            f = f0 * d
            for k in range(1, 60):
                fk = k * f
                if fk > rate * 0.45:
                    break
                if square and k % 2 == 0:
                    continue
                g = 1 / np.sqrt(1 + (hp / fk) ** 4) if hp else 1
                if res:                                         # resonantiepiek op de filterfrequentie (psy-'squelch')
                    g = g * (1 + res * np.exp(-((fk - cut) / (0.3 * cut)) ** 2))
                a += g * (1 / k) * np.sin(2 * np.pi * fk * tt + k) / np.sqrt(1 + (fk / cut) ** 4)
    a *= np.minimum(1, tt / 0.002) * np.exp(-tt / tau_amp)
    a = np.tanh(drive * a / np.abs(a).max())
    fade = int(rate * 0.02)
    a[-fade:] *= np.linspace(1, 0, fade)
    return a / np.abs(a).max() * 0.97


def synth3(name):
    """-> (golf, samplerate, label-toets, loop)"""
    C2, C3, C4, C5 = 65.406, 130.813, 261.626, 523.251
    if name == 'gym2_w_saw':
        # Winona-lead: scherpe zaagtand, drie stemmen ±13 cent (supersaw-achtig), licht overstuurd; C5, 4096 samples
        a = saw_loop(32, (128, 127, 129), 11, drive=1.8)
        return a, int(round(C5 * 32)), 72, (0, len(a))
    if name == 'gym2_w_saw_dark':
        # tweede stem/harmonie: dezelfde zaag, donker gefilterd (3e harmonische), C4
        a = saw_loop(64, (128, 129), 3.5, drive=1.3)
        return a, int(round(C4 * 64)), 60, (0, len(a))
    if name == 'gym2_w_reese':
        # ronkende reese-bas: twee zaagtanden 17 cent uit elkaar (langzame zweving 0,65 Hz), filter 6e harmonische,
        # overstuurd; C2, loop 1,5 s
        a = saw_loop(256, (100, 101), 6, drive=2.2)
        return a, int(round(C2 * 256)), 36, (0, len(a))
    if name.startswith('gym2_w_stab_'):
        iv = W_STABS[name.rsplit('_', 1)[1]]
        # hoogdoorlaat 260 Hz: een korte middenstoot, de grondtoon laat hij aan de reese over
        a = chord_oneshot([C3 * 2 ** (i / 12) for i in iv], 22050, 0.30, 5200, 900, 0.06, 0.11, drive=2.4, hp=260)
        return a, 22050, 60, None
    if name == 'gym2_w_snare':
        # droge harde snare: FluidR3 Power-kit-snare + 909-clap (GM-drumkit) + ruisstoot, overstuurd, 0,17 s, geen galm
        rate = 22050
        a = render([('drum', 16, 38), ('drum', 25, 39)], 0.25, 127)
        start = int(np.argmax(np.abs(a) > 0.002))
        a = resample(a[start:start + int(0.17 * FS)], FS, rate)
        tt = np.arange(len(a)) / rate
        rng = np.random.default_rng(38)
        nz = lowpass(rng.standard_normal(len(a)), rate, 7000) * np.exp(-tt / 0.035)
        a = a / np.abs(a).max() + 0.55 * nz / np.abs(nz).max()
        a *= np.exp(-tt / 0.07)
        a = np.tanh(3.0 * a / np.abs(a).max())
        a[-int(rate * 0.015):] *= np.linspace(1, 0, int(rate * 0.015))
        return a / np.abs(a).max() * 0.97, rate, 60, None
    if name == 'gym2_tl_pluck':
        # Tate: psy-pluk (zaagtand, filter 5 kHz -> 700 Hz in 70 ms), 0,22 s, C4 (ref-leads: 38% in 1-4 kHz)
        a = chord_oneshot([C4], 22050, 0.22, 5000, 900, 0.10, 0.09, detune=0.004, drive=1.8, res=3.0)
        return a, 22050, 60, None
    if name == 'gym2_tl_pluck_b':
        # Liza: holle blokgolf-pluk (oneven harmonischen), trager filter, iets langer, C4
        a = chord_oneshot([C4], 22050, 0.26, 3800, 800, 0.12, 0.12, detune=0.007, drive=1.5, square=True, res=2.0)
        return a, 22050, 60, None
    if name == 'gym2_tl_lead':
        # 'mind-control'-lead voor de lange noten met pitch bends: twee zaagtanden 7 cent, filter 8e harmonische, C4
        a = saw_loop(64, (256, 257), 8.0, drive=1.5)
        return a, int(round(C4 * 64)), 60, (0, len(a))
    if name.startswith('gym2_tl_pad_'):
        # donkere pad: drieklank in reine stemming + grondtoon een octaaf lager, elke toon met een ontstemde tweeling
        # (+1 periode per loop), filter 900 Hz; C3, loop 1,5 s
        r = TL_PADS[name.rsplit('_', 1)[1]]
        per = 128                                 # C3 doet 200 perioden per loop
        L = per * 200
        rate = int(round(C3 * per))
        t = np.arange(L) / L * 2 * np.pi
        a = np.zeros(L)
        cyc = [100] + [200 * x // r[0] for x in r]
        for c0 in cyc:
            for c in (c0, c0 + 1):
                for k in range(1, 40):
                    fk = k * c / 200 * C3
                    if fk > rate * 0.45:
                        break
                    a += (1 / k) / np.sqrt(1 + (fk / 900) ** 4) * np.sin(k * c * t + 0.9 * k * c)
        a /= np.abs(a).max()
        return a * 0.97, rate, 48, (0, len(a))
    raise ValueError(name)


def main():
    os.makedirs(OUT, exist_ok=True)
    inc = open(DATA).read()
    names = []
    for name, (notes, dur, loop, key, rate, vel, lp) in FLUID.items():
        a = render(notes, dur, vel)
        start = int(np.argmax(np.abs(a) > 0.002))
        a = a[start:start + int(dur * FS)]
        if lp:
            a = lowpass(a, FS, lp)
        a = resample(a, FS, rate)
        a = a / max(1e-6, np.abs(a).max()) * 0.97
        lpts = None
        if loop:
            a, lpts = auto_loop(a, rate)
        else:
            fade = int(rate * min(0.05, dur / 4))
            a[-fade:] *= np.linspace(1, 0, fade)
        write_wav(OUT + name + '.wav', a, rate, key, lpts)
        names.append(name)
        print('%-17s %s, %d samples @ %d Hz, loop %s' % (name, notes, len(a), rate, lpts))
    for name in SYNTH:
        a, rate, key, lpts = synth(name)
        write_wav(OUT + name + '.wav', a, rate, key, lpts)
        names.append(name)
        print('%-17s synth, %d samples @ %d Hz, loop %s' % (name, len(a), rate, lpts))
    for name, (kind, notes) in LAYER.items():
        a, rate = layer(kind, notes)
        write_wav(OUT + name + '.wav', a, rate, 60, None)
        names.append(name)
        print('%-17s %s %s, %d samples @ %d Hz' % (name, kind, notes, len(a), rate))
    for name in SYNTH3:
        a, rate, key, lpts = synth3(name)
        write_wav(OUT + name + '.wav', a, rate, key, lpts)
        names.append(name)
        print('%-17s synth (v3), %d samples @ %d Hz, loop %s' % (name, len(a), rate, lpts))
    pw =open('sound/programmable_wave_data.inc').read()
    for name, vals in WAVES.items():
        open('sound/programmable_wave_samples/%s.pcm' % name, 'wb').write(
            bytes((vals[2 * i] << 4) | vals[2 * i + 1] for i in range(16)))
        label = 'ProgrammableWaveData_%s::' % name
        if label not in pw:
            pw = pw.rstrip('\n') + '\n\n%s\n\t.incbin "sound/programmable_wave_samples/%s.pcm"\n' % (label, name)
    open('sound/programmable_wave_data.inc', 'w').write(pw)
    for name in names:
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()

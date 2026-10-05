#!/usr/bin/env python3
"""Project Grounded: eigen samples voor Battle! Darkrai (darkrai_theme.py): een speeldoos-wiegelied dat ontspoort.

- darkrai_music_box     FluidR3 Music Box (GM 10) op C5 + een kopie +22 cent erbovenop gebakken: een ontstemde
                        speeldoos die langzaam zweeft (±7 Hz op C5), 1 kanaal per noot.
- darkrai_celesta       FluidR3 Celesta (GM 8) op C5, voor clusters en prikjes.
- darkrai_rev_box       één speeldoosnoot (C5) achterstevoren: zwelt aan en eindigt hard op de 'aanslag'.
- darkrai_rev_cluster   cluster E5-F5-Bb5 op speeldoos + celesta, achterstevoren (grondtoon C5 = speel 72 voor E-F-Bb).
- darkrai_lullaby_rev   het hele wiegelied (4 maten 7/8, 150 bpm) op de speeldoos, achterstevoren, precies 5,6 s: één kanaal.
- darkrai_cry_rev       de Gen 3-cry van Darkrai achterstevoren en op 0,8x (dieper, trager), grondtoon 60.
- darkrai_revcym        crashbekken (FluidR3 drum 49) achterstevoren, precies 1 maat 7/8 (1,4 s) lang: riser.
v2 (Giratina-achtig, duisterder):
- darkrai_brass_dim     rauwe koperstoot (FluidR3 Brass Section 61 + Synth Brass 62) E3-G3-Bb3-E4 (verminderd),
                        door tanh x3 en op 13.379 Hz (Gen 3-korrel): één kanaal per akkoord, grondtoon E3 (52).
- darkrai_brass_tt      idem als cluster E3-Bb3-E4-F4 (tritonus + kleine none): de schurendste stoot.
- darkrai_drone         kerkorgel (GM 19) E1-Bb1-E2 (tritonus-drone), gelust, label E2 (40): speel 40 = E1-Bb1-E2.
v3 (climax):
- darkrai_brass_low     denderende lage koperstoot: trombone 57 + tuba 58 + brass 61, E2-Bb2-E3-F3, tanh x3, 13.379 Hz.
- darkrai_scream        schurend clusterakkoord E4-F4-Bb4-B4: tremolo-strijkers 44 + koor 52, tanh x1,8, gelust.
Gebruik: python3 tools/grounded/darkrai_samples.py  (vereist fluidsynth + FluidR3_GM, zie MUZIEK.md)"""
import os, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gm_samples import render                     # FluidR3-render van één noot / loopje (alleen gelezen)
from sample_utils import resample, write_wav, auto_loop

OUT = 'sound/direct_sound_samples/grounded/'
DATA = 'sound/direct_sound_data.inc'
SR = 44100
# het wiegelied (zelfde als LULLABY in darkrai_theme.py): (noot, achtsten)
LULLABY = [(71, 2), (67, 2), (71, 1), (76, 2), (75, 2), (72, 2), (71, 3),
           (69, 2), (72, 2), (71, 1), (67, 2), (66, 2), (70, 2), (64, 3)]


def fade(x, rate, a=0.004, b=0.01):
    x = x.copy()
    k, f = int(a * rate), int(b * rate)
    if k:
        x[:k] *= np.linspace(0, 1, k)
    x[-f:] *= np.linspace(1, 0, f)
    return x


def trim(a, thr=0.002):
    nz = np.nonzero(np.abs(a) > thr)[0]
    return a[nz[0]:nz[-1] + 1] if len(nz) else a


def norm(a, peak=0.95):
    return a / np.abs(a).max() * peak


def render_seq(prog, notes, step_s):
    """Meerdere noten na elkaar (elk `dur` achtsten) in één render: via een eigen MIDI met fluidsynth."""
    import mido, subprocess, tempfile
    from gm_samples import SF2
    m = mido.MidiFile(ticks_per_beat=480)
    t = mido.MidiTrack(); m.tracks.append(t)
    t.append(mido.Message('program_change', program=prog, time=0))
    t.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))   # 960 ticks/s
    for n, d in notes:
        t.append(mido.Message('note_on', note=n, velocity=96, time=0))
        t.append(mido.Message('note_off', note=n, velocity=0, time=int(d * step_s * 960)))
    t.append(mido.Message('note_off', note=0, velocity=0, time=960))
    with tempfile.TemporaryDirectory() as d:
        mid, wav = os.path.join(d, 'n.mid'), os.path.join(d, 'n.wav')
        m.save(mid)
        subprocess.run(['fluidsynth', '-ni', '-g', '1.0', '-R', '0', '-C', '0', '-r', str(SR), '-F', wav, SF2, mid],
                       check=True, capture_output=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).mean(1)
    return a / 32768.0


def main():
    out = {}
    # ontstemde speeldoos: origineel + kopie 22 cent hoger (korter afgespeeld)
    box = trim(render(10, 72, 1.6))
    hi = resample(box, SR * 2 ** (22 / 1200), SR, antialias=False)
    n = min(len(box), len(hi))
    det = 0.6 * box[:n] + 0.45 * hi[:n]
    det = det[:int(1.5 * SR)]
    out['darkrai_music_box'] = (fade(norm(resample(det, SR, 22050)), 22050, 0, 0.08), 22050, 72)
    cel = trim(render(8, 72, 1.3))[:int(1.2 * SR)]
    out['darkrai_celesta'] = (fade(norm(resample(cel, SR, 22050)), 22050, 0, 0.08), 22050, 72)
    # achterstevoren speeldoosnoot: 1,0 s, de aanslag precies aan het eind
    rb = trim(render(10, 72, 1.2))[:int(1.0 * SR)][::-1]
    out['darkrai_rev_box'] = (fade(norm(resample(rb, SR, 16000), 0.9), 16000, 0.05, 0.003), 16000, 72)
    # cluster E5-F5-Bb5 achterstevoren (speeldoos + celesta)
    n = int(1.2 * SR)
    pad = lambda a: np.pad(a, (0, max(0, n - len(a))))[:n]
    c = sum(0.6 * pad(trim(render(10, k, 1.3))) + 0.5 * pad(trim(render(8, k, 1.3))) for k in (76, 77, 82))
    out['darkrai_rev_cluster'] = (fade(norm(resample(c[::-1], SR, 16000), 0.9), 16000, 0.08, 0.003), 16000, 72)
    # het wiegelied achterstevoren (4 maten 7/8 bij 150 bpm: een achtste = 0,2 s)
    # precies 5,6 s (= 4 maten 7/8 = 28 achtsten) door het iets sneller af te spelen (+0,6 halve toon: extra vals)
    lul = trim(render_seq(10, LULLABY, 0.2))[::-1]
    lul = resample(lul, len(lul), int(5.6 * 13379), antialias=False)
    out['darkrai_lullaby_rev'] = (fade(norm(lul, 0.9), 13379, 0.3, 0.02), 13379, 60)
    # de cry van Darkrai achterstevoren, op 0,8x
    w = wave.open('sound/direct_sound_samples/cries/darkrai.wav')
    rate = w.getframerate()
    cry = (np.frombuffer(w.readframes(w.getnframes()), np.uint8).astype(float) - 128) / 128.0
    slow = resample(cry[::-1], rate, rate / 0.8, antialias=False)
    out['darkrai_cry_rev'] = (fade(norm(slow, 0.9), rate, 0.15, 0.01), rate, 60)
    # omgekeerd bekken: precies 1,4 s (1 maat 7/8) op 16 kHz, de 'klap' in de laatste 20 ms
    cy = trim(render(('drum', 49), 60, 2.5))
    L = int(1.4 * SR)
    cy = np.pad(cy, (0, max(0, L - len(cy))))[:L][::-1]
    cy = cy * np.linspace(0.15, 1, L) ** 1.5           # langzamer aanzwellen, laatste stuk het luidst
    out['darkrai_revcym'] = (fade(norm(resample(cy, SR, 16000), 0.85), 16000, 0.1, 0.004), 16000, 60)

    # v2: rauwe brass-stabs (één sample per voicing) en een tritonus-orgeldrone
    def stab(notes):
        n = int(0.55 * SR)
        pad = lambda a: np.pad(a, (0, max(0, n - len(a))))[:n]
        x = 0.6 * pad(trim(render(61, 0, 0.5, run=notes))) + 0.5 * pad(trim(render(62, 0, 0.5, run=notes)))
        x = np.tanh(3.0 * norm(x, 1.0))
        return fade(norm(resample(x, SR, 13379), 0.95), 13379, 0, 0.06)
    out['darkrai_brass_dim'] = (stab([52, 55, 58, 64]), 13379, 52)
    out['darkrai_brass_tt'] = (stab([52, 58, 64, 65]), 13379, 52)
    org = trim(render(19, 0, 3.0, run=[28, 34, 40]))[:int(2.6 * SR)]
    org = norm(resample(np.tanh(1.5 * norm(org, 1.0)), SR, 13379), 0.9)
    org, lp = auto_loop(org, 13379)
    out['darkrai_drone'] = (org, 13379, 40, lp)

    # v3: de climax (Giratina-dreiging): denderende lage koperstoot en een schurend, aangehouden clusterakkoord
    def low_stab(notes):
        n = int(0.75 * SR)
        pad = lambda a: np.pad(a, (0, max(0, n - len(a))))[:n]
        x = (0.6 * pad(trim(render(57, 0, 0.7, run=notes))) + 0.55 * pad(trim(render(58, 0, 0.7, run=notes)))
             + 0.4 * pad(trim(render(61, 0, 0.7, run=notes))))
        x = np.tanh(3.0 * norm(x, 1.0))
        return fade(norm(resample(x, SR, 13379), 0.95), 13379, 0, 0.08)
    out['darkrai_brass_low'] = (low_stab([40, 46, 52, 53]), 13379, 40)     # E2-Bb2-E3-F3, label E2 (40)
    scr = (0.6 * trim(render(44, 0, 3.0, run=[64, 65, 70, 71]))[:int(2.6 * SR)]
           + 0.5 * np.pad(trim(render(52, 0, 3.0, run=[64, 65, 70, 71])), (0, SR))[:int(2.6 * SR)])
    scr = norm(resample(np.tanh(1.8 * norm(scr, 1.0)), SR, 13379), 0.9)
    scr, lp = auto_loop(scr, 13379)
    out['darkrai_scream'] = (scr, 13379, 64, lp)                          # E4-F4-Bb4-B4, label E4 (64)

    inc = open(DATA).read()
    for name, v in out.items():
        x, r, key = v[:3]
        write_wav(OUT + name + '.wav', x, r, key, v[3] if len(v) > 3 else None)
        label = 'DirectSoundWaveData_' + name
        if label + '::' not in inc:
            inc = inc.rstrip('\n') + '\n\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/grounded/%s.bin"\n' % (label, name)
        print('%-22s %6d samples @ %5d Hz (%.2f s)' % (name, len(x), r, len(x) / r))
    open(DATA, 'w').write(inc)


if __name__ == '__main__':
    main()

"""Project Grounded: muziek in batches controleren (Jordi: 'per 10 of 20 i.p.v. per 1').
Bouwt per 8 nummers één test-ROM (debug-scripts 1-8 = playbgm), neemt elk nummer op en geeft één overzicht:
recpcm (overlopen + piek), recaudio + audiocheck (pieken, constante tonen, RMS) en een preview-mp3.
Gebruik (vanuit de hoofdmap):
  python3 tools/grounded/maptools/batchrec.py <uitmap> MUS_A:90 MUS_B:120[:start] ...
  (seconden = opnameduur; optioneel start = vanaf welke seconde de preview begint, standaard 0)
Daarna `make` opnieuw voor een schone ROM. Opnames lopen met 3 processen tegelijk."""
import os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
PY = sys.executable
ENV = dict(os.environ, PYTHONPATH=HERE)


def run(cmd):
    r = subprocess.run(cmd, cwd=REPO, env=ENV, capture_output=True, text=True)
    return r.stdout + r.stderr


def one(rom, st, k, song, sec, start, out):
    base = os.path.join(out, song.lower())
    pcm = run([PY, os.path.join(HERE, 'recpcm.py'), rom, st, str(k), str(sec + 10), base + '_pcm.wav'])
    run([PY, os.path.join(HERE, 'recaudio.py'), rom, st, str(k), str(sec), base + '.wav'])
    ac = run([PY, os.path.join(HERE, 'audiocheck.py'), base + '.wav'])
    mp3 = base + '_preview.mp3'
    n = min(sec - start, 90)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(start + 0.1), '-i', base + '.wav', '-t', str(n),
                    '-af', 'afade=t=in:d=0.05,afade=t=out:st=%g:d=2' % (n - 2), '-b:a', '160k', mp3])
    vd = subprocess.run(['ffmpeg', '-i', mp3, '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True).stderr
    mx = re.search(r'max_volume: (\S+) dB', vd)
    for f in (base + '_pcm.wav',):
        if os.path.exists(f):
            os.remove(f)
    ov = re.search(r'OVERLOPEN \(knapperen\): (\d+)', pcm)
    pk = re.search(r'piek (\d+)/127', pcm)
    peaks = re.search(r'peaks at s: (\[[^\]]*\])', ac)
    tones = re.search(r'constant tones \(Hz\): (\[[^\]]*\])', ac)
    rmsl = re.search(r'rms per 5s: (\[[^\]]*\])', ac)
    return dict(song=song, overlopen=int(ov.group(1)) if ov else 0, piek=pk.group(1) if pk else '?',
                peaks=peaks.group(1) if peaks else '?', tones=tones.group(1) if tones else '[]',
                rms=rmsl.group(1) if rmsl else '?', max_db=mx.group(1) if mx else '?', mp3=mp3)


def main():
    out, items = sys.argv[1], sys.argv[2:]
    os.makedirs(out, exist_ok=True)
    songs = []
    for it in items:
        p = it.split(':')
        songs.append((p[0], float(p[1]), float(p[2]) if len(p) > 2 else 0.0))
    results = []
    for c in range(0, len(songs), 8):
        chunk = songs[c:c + 8]
        d = os.path.join(out, 'rom%d' % (c // 8))
        print(run([PY, os.path.join(HERE, 'testrom.py'), d] + ['playbgm %s, FALSE' % s for s, _, _ in chunk]).strip()[-200:])
        rom, st = os.path.join(d, 'test.gba'), os.path.join(d, 'intro.bin')
        with ThreadPoolExecutor(3) as ex:
            futs = [ex.submit(one, rom, st, k, s, sec, start, out) for k, (s, sec, start) in enumerate(chunk, 1)]
            results += [f.result() for f in futs]
    print('\n%-32s %9s %6s %9s  %s' % ('nummer', 'overlopen', 'piek', 'max dB', 'pieken / constante tonen / rms per 5 s'))
    bad = 0
    for r in results:
        ok = r['overlopen'] == 0 and r['piek'] != '?' and int(r['piek']) <= 120 and r['peaks'] in ('[]', '?')
        bad += not ok
        print('%-32s %9d %6s %9s  %s %s %s %s' % (r['song'], r['overlopen'], r['piek'], r['max_db'],
              'OK ' if ok else 'FOUT', r['peaks'], r['tones'], r['rms']))
    print('\npreviews in', out, '| afgekeurd:', bad)


if __name__ == '__main__':
    main()

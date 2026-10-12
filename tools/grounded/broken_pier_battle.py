#!/usr/bin/env python3
"""Project Grounded: Battle! Boo (v0.9.244), een lichte battle-remix van de Broken Pier-rip (Mario Kart: Super Circuit).
Jordi (10 okt): "Broken Pier is goed. Kan je die heel licht remixen zodat het net meer een battle theme klinkt?" en
"broken pier dan behouden voor de boo house ... en dan de battle theme voor Boos".
Uit sound/songs/mus_grounded_mksc_broken_pier.s (de 1-op-1-rip, mp2k_rip.py) maakt dit script
sound/songs/mus_grounded_vs_boo.s:
- tempo 116 -> 132 bpm (het TEMPO-commando in spoor 0),
- een extra drumspoor (de eigen MKSC-drumkit: kick 36, snare 40, hihat 96) in de eerste 9 maten, die in het
  origineel zonder drums zijn: kick op 1 en 3 (met een opmaat-kick), snare op 2 en 4, hihat op de achtsten. Vanaf maat
  10 speelt het originele drumspoor; het extra spoor rust dan tot het einde van de loop (26 maten).
Alle data (voicegroup, drumkit) wordt met eigen labels gekopieerd. Gebruik: python3 tools/grounded/broken_pier_battle.py"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'sound/songs/mus_grounded_mksc_broken_pier.s')
DST = os.path.join(ROOT, 'sound/songs/mus_grounded_vs_boo.s')
OLD, NEW = 'mus_grounded_mksc_broken_pier', 'mus_grounded_vs_boo'
TEMPO = 132
BAR, LOOP_BARS, INTRO_BARS = 96, 26, 9
W = list(range(25)) + [28, 30, 32, 36, 40, 42, 44, 48, 52, 54, 56, 60, 64, 66, 68, 72, 76, 78, 80, 84, 88, 90, 92, 96]
KICK, SNARE, HAT = 36, 40, 96


def wait(n):
    out = []
    while n > 0:
        i = max(k for k in range(len(W)) if W[k] <= n)
        out.append(0x80 + i)
        n -= W[i]
    return out


def drum_track():
    """Bytes van het extra drumspoor (zonder GOTO/FINE)."""
    ev = []                                      # (tick, key, velocity)
    for b in range(INTRO_BARS):
        t0 = b * BAR
        for s in range(8):                       # achtsten
            ev.append((t0 + s * 12, HAT, 52 if s % 2 else 68))
        for p, v in ((0, 96), (48, 92)):
            ev.append((t0 + p, KICK, v))
        if b % 2 == 1:
            ev.append((t0 + 84, KICK, 76))       # opmaat naar de volgende maat
        for p in (24, 72):
            ev.append((t0 + p, SNARE, 84))
    ev.sort()
    out, t = [], 0
    for tick in sorted(set(e[0] for e in ev)):
        out += wait(tick - t)
        t = tick
        for _, k, v in [e for e in ev if e[0] == tick]:
            out += [0xD5, k, v]                  # N06
    out += wait(LOOP_BARS * BAR - t)
    return out


def main():
    s = open(SRC).read()
    s = s.replace(OLD, NEW)
    s = s.replace('@ Project Grounded: Mario Kart: Super Circuit, Boo Lake & Broken Pier',
                  '@ Project Grounded: Battle! Boo, lichte battle-remix van Boo Lake & Broken Pier (tools/grounded/broken_pier_battle.py)', 1)
    # tempo: eerste TEMPO-commando (0xBB, waarde = bpm/2) in spoor 0
    i = s.index(NEW + '_0:')
    m = re.compile(r'0xBB, 0x([0-9A-F]{2})').search(s, i)
    assert m and int(m.group(1), 16) * 2 == 116, 'tempo niet gevonden'
    s = s[:m.start()] + '0xBB, 0x%02X' % (TEMPO // 2) + s[m.end():]
    # extra spoor vóór de songkop
    h = s.index('\t.global %s\n' % NEW)
    body = [0xBC, 0x00, 0xBD, 0x7F, 0xBE, 0x5A, 0xBF, 0x40] + drum_track()
    lines = ['%s_6:' % NEW, '%s_6_loop:' % NEW]
    for k in range(0, len(body), 16):
        lines.append('\t.byte ' + ', '.join('0x%02X' % x for x in body[k:k + 16]))
    lines += ['\t.byte 0xB2', '\t.4byte %s_6_loop' % NEW, '\t.byte 0xB1', '', '\t.align 2', '']
    s = s[:h] + '\n'.join(lines) + s[h:]
    # songkop: 7 sporen
    s = s.replace('%s:\n\t.byte 6, 0, 0, 178' % NEW, '%s:\n\t.byte 7, 0, 0, 178' % NEW, 1)
    s = s.replace('\t.4byte %s_5\n' % NEW, '\t.4byte %s_5\n\t.4byte %s_6\n' % (NEW, NEW), 1)
    assert '.byte 7, 0, 0, 178' in s and '%s_6\n' % NEW in s
    open(DST, 'w').write(s)
    print('geschreven:', DST, '(%d bytes drumspoor)' % len(body))


if __name__ == '__main__':
    main()

"""Fully Ungrounded: haalt alle trainerteams uit src/data/trainers.party behalve het skelet (PLAN_HOENN_ERUIT.md, stap 6).

Blijft: TRAINER_NONE, Keccles (alle TRAINER_KECCLES_*) en elke trainer die de skeletkaarten of de algemene scripts
nog bevechten (trainerbattle-regels in data/maps/*/scripts.inc en data/scripts/*.inc).
include/constants/opponents.h blijft zoals hij is (niet hernummeren: de trainerflags hangen aan de id's);
gTrainers gebruikt aangewezen initialisatie, dus een id zonder team wordt een leeg team.
Idempotent. Gebruik: python3 tools/grounded/trainers_eruit.py
"""
import glob, re

P = 'src/data/trainers.party'


def fought():
    """Trainers die nog ergens in een script bevochten worden."""
    res = set()
    for f in glob.glob('data/maps/*/scripts.inc') + glob.glob('data/scripts/*.inc'):
        for l in open(f, errors='ignore'):
            if re.match(r'\s*trainerbattle\w*\s', l):
                res.update(re.findall(r'\bTRAINER_[A-Z0-9_]+\b', l))
    return res


def main():
    text = open(P).read()
    parts = re.split(r'(?m)^(?==== )', text)
    head, blocks = parts[0], parts[1:]
    keep = {'TRAINER_NONE'} | fought()
    out, gone = [head], 0
    for b in blocks:
        tid = re.match(r'=== (\w+) ===', b).group(1)
        if tid in keep or tid.startswith('TRAINER_KECCLES'):
            out.append(b)
        else:
            gone += 1
    t = ''.join(out).rstrip('\n') + '\n'
    open(P, 'w').write(t)
    print('trainers weg: %d, over: %d (%s)' % (gone, len(out) - 1,
                                             ', '.join(re.findall(r'(?m)^=== (\w+) ===', t))))


if __name__ == '__main__':
    main()

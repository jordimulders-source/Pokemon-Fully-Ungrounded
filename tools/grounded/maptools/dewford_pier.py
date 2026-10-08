"""Project Grounded: verlengt de steiger van Dewford naar het oosten voor het visserstoernooi (ZEE_PLAN.md).

Vanilla: steiger op rij 9, x 11-13 (0x228 linkereinde, 0x229 planken, rij 10 = palen 0x230/0x231).
Nieuw: planken op rij 9, x 14-18 (een breed: Brineys boot vaart over rij 8 naar Slateport), met palen eronder (rij 10). Idempotent: draait vanaf de vanilla-tiles.
"""
import json, struct

LAYOUT = 'LAYOUT_DEWFORD_TOWN'
# volledige waarden (metatile | botsing << 10 | hoogte << 12), gekopieerd van de vanilla-steiger
PLANK, LEGS, SHORE = 0x3229, 0x0631, 0x311C
X0, X1, ROW = 14, 18, 9

layouts = json.load(open('data/layouts/layouts.json'))['layouts']
L = [l for l in layouts if l['id'] == LAYOUT][0]
w, h = L['width'], L['height']
path = L['blockdata_filepath']
v = list(struct.unpack(f'<{w*h}H', open(path, 'rb').read()))

def put(x, y, value):
    v[y * w + x] = value

for x in range(X0, X1 + 1):
    put(x, ROW, PLANK)        # begaanbare planken
    put(x, ROW + 1, LEGS)      # palen in het water (niet begaanbaar)
# de oever schuift een rij op: zand met waterrand bovenaan (zoals x 12-13, rij 11)
for x in (14, 15):
    put(x, ROW + 2, SHORE)

open(path, 'wb').write(struct.pack(f'<{w*h}H', *v))
print('steiger verlengd: x', X0, '-', X1, 'rij', ROW)

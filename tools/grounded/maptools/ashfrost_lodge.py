"""Bouwt de bovenverdieping van de Ashfrost Lodge uit de houten hutten van de S.S. Tidal (tileset InsideShip,
alleen de bovenste rij hutten: die hebben geen patrijspoorten of reddingsboeien).
- data/layouts/AshfrostLodge_2F: gang (24x7) met vier kamerdeuren in de achterwand en een mat linksonder
  (warp naar de trap in de lobby).
- data/layouts/AshfrostLodge_Rooms: de vier kamers (36x9), een kopie van de bovenste helft van SSTidalRooms;
  elke kamer heeft zijn deur bovenin (x 4, 13, 22, 31 op y 1).
Gebruik: python3 tools/grounded/maptools/ashfrost_lodge.py"""
import os, struct
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
SRC = os.path.join(REPO, 'data/layouts/SSTidalRooms')
SW, SH = 36, 18
src = struct.unpack(f'<{SW*SH}H', open(SRC + '/map.bin', 'rb').read())
at = lambda x, y: src[y * SW + x]          # ruwe waarde: metatile + botsing + hoogte
mt = lambda v: v & 0x3ff
def raw(m, like):
    """metatile m met de botsing/hoogte van een vergelijkbare tegel uit het origineel"""
    return (like & ~0x3ff) | m
FLOOR, WALLX, BLACK = at(3, 5), at(0, 2), at(8, 0)
assert mt(FLOOR) == 0x238 and mt(WALLX) == 0x23e and mt(BLACK) == 0x201

# --- gang ---
W, H = 24, 7
g = [[BLACK] * W for _ in range(H)]
# achterwand: kale houten wand (26c/274, zoals de hut rechtsonder) met vier deuren (295 263 296 / 29d 297 29e);
# geen kozijnstukken met bedlampjes, die horen bij de bedden in de hutten
DOORS = [4, 9, 14, 19]
for x in range(23):
    g[0][x], g[1][x] = at(3, 9), at(3, 10)
for d in DOORS:
    for dx in (-1, 0, 1):
        g[0][d + dx], g[1][d + dx] = at(4 + dx, 0), at(4 + dx, 1)
for y in range(2, 6):
    for x in range(0, 23):
        if y == 2: g[y][x] = at(10 if x == 0 else 11, 11)   # schaduwrand onder de muur (23a / 23b)
        else: g[y][x] = at(10, 12) if x == 0 else FLOOR     # 23d / 238
assert mt(g[0][3]) == 0x295 and mt(g[1][4]) == 0x297 and mt(g[0][0]) == 0x26c and mt(g[2][0]) == 0x23a
g[5][2], g[5][3] = at(4, 16), at(5, 16)         # mat naar de trap in de lobby
assert mt(g[5][2]) == 0x264
out = os.path.join(REPO, 'data/layouts/AshfrostLodge_2F')
os.makedirs(out, exist_ok=True)
open(out + '/map.bin', 'wb').write(struct.pack(f'<{W*H}H', *[g[y][x] for y in range(H) for x in range(W)]))
open(out + '/border.bin', 'wb').write(struct.pack('<4H', *[BLACK] * 4))
print('gang:', out, 'deuren op x', DOORS, 'y 1; mat (2,5),(3,5)')

# --- kamers: bovenste helft van SSTidalRooms (rij 8 = zwart) ---
RH = 9
out = os.path.join(REPO, 'data/layouts/AshfrostLodge_Rooms')
os.makedirs(out, exist_ok=True)
open(out + '/map.bin', 'wb').write(struct.pack(f'<{SW*RH}H', *[at(x, y) for y in range(RH) for x in range(SW)]))
open(out + '/border.bin', 'wb').write(open(SRC + '/border.bin', 'rb').read())
assert all(mt(at(x, 1)) == 0x297 for x in (4, 13, 22, 31))
print('kamers:', out, 'deuren op x 4, 13, 22, 31 y 1')

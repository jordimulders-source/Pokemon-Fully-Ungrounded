"""Project Grounded: het Battle Stadium (à la Pokémon World Tournament) op het Battle Frontier-eiland.

- BattleFrontier_OutsideEast wordt EXTRA rijen hoger aan de onderkant (zee). Er verschuift dus niets:
  geen events, geen verbinding met OutsideWest (die rekent vanaf de bovenkant), geen veerboot-warps.
- Het plein linksonder (onder het Pokémon Center en de lounges) loopt door naar het zuiden: de oude
  bloementuin, het lage terras en de zuidkust (x 5..34) maken plaats voor een nieuw plateau met
  dezelfde Frontier-randen als de rest van het eiland (wit hek met vlaggen, klif van drie rijen,
  kustlijn). Het stadion staat daar midden op, met looppaden links en rechts en een voorplein met
  twee bloembakken (de plantenbak van de Arena, verkleind).
- Het stadion (21 x 14 metatiles, groter dan de Battle Tower) is pixel voor pixel opgebouwd in de
  Frontier-stijl: een ovale kom van bovenaf (wit dak, tribunes met blauwe stoelen en trappen, een
  grasveld met lijnen in palet 7) en een gevel in de kleuren van de Battle Dome (palet 1 van General:
  oranje/rode lijst, witte pilaren, blauw glas, rode banieren met Poké Ball) met in het midden de
  ingang van de Battle Dome (luifel + glazen schuifdeur, pixels uit gTileset_BattleFrontierOutsideWest).
- Deur: metatile 0x28A met MB_ANIMATED_DOOR. field_door.c zoekt de deuranimatie op metatile-nummer,
  dus de deur schuift open met de Battle Dome-animatie (palet 1). De oude 0x28A van East (Pyramid-plein)
  verhuist naar een vrije plek.
- Tiles/metatiles komen op vrije plekken van gTileset_BattleFrontierOutsideEast (alleen deze kaart
  gebruikt die tileset).
- Binnen: BattleFrontier_StadiumLobby (kopie van de Battle Dome-lobby) en BattleFrontier_StadiumArena
  (kopie van de Battle Dome-gevechtszaal). Scripts.inc wordt alleen aangemaakt als hij nog niet bestaat.

Idempotent: leest de oorspronkelijke kaart/tilesets uit git (commit ORIG) en bouwt alles opnieuw.
Gebruik: python3 tools/grounded/maptools/stadium.py [voorbeeld.png]
"""
import io, json, math, os, re, shutil, struct, subprocess, sys
from PIL import Image

ORIG = 'b0dc8440'           # commit vóór het stadion
W, H0 = 72, 72
EXTRA = 18                  # extra rijen zee onderaan
H = H0 + EXTRA
assert (W + 15) * (H + 14) <= 10240          # MAX_MAP_DATA_SIZE (include/fieldmap.h)
TS = 'data/tilesets/secondary/battle_frontier_outside_east/'
WEST = 'data/tilesets/secondary/battle_frontier_outside_west/'
GEN = 'data/tilesets/primary/general/'
LAY = 'data/layouts/BattleFrontier_OutsideEast/'
MAPJ = 'data/maps/BattleFrontier_OutsideEast/map.json'
NUM_TILES = 508             # -num_tiles in graphics_file_rules.mk
FLAG_ANIM_TILES = range(218, 224)
DOOR_LABELS = {0x3FC, 0x291, 0x329, 0x396, 0x3B0}   # deuranimaties op metatile-nummer (field_door.c)
DOOR_MT = 0x28A             # = METATILE_BattleFrontierOutsideWest_Door_BattleDome (deuranimatie)
MB_ANIMATED_DOOR = 0x69
COVERED = 1 << 12

# ---------------------------------------------------------------- indeling (kaartcoördinaten)
XS_W, XC_W, XF_W = 4, 5, 6          # westkant: kustlijn, klif, hek
XF_E, XC_E, XS_E = 32, 33, 34       # oostkant: hek, klif, kustlijn
TOP = 54                            # eerste rij die het nieuwe plateau overschrijft
SX, SY = 9, 59                      # linksboven van het stadion
SW, SH = 21, 14                     # stadion in metatiles
DOOR = (SX + SW // 2, SY + SH - 1)  # (19, 72)
YF = SY + SH + 5                    # hekrij met vlaggen (78); voorplein SY+SH .. YF-1
YC = YF + 1                         # klif YC..YC+2, kustlijn YC+3
LOBBY = 'MAP_BATTLE_FRONTIER_STADIUM_LOBBY'

# metatiles uit General (kliffen, water, hek) en uit East (vlaggen, plantenbak)
SEA, ROCK = 0x170, (0x150, 0x151, 0x158, 0x159)
FLOOR, FLOOR_GRASS_TOP = 0x109, 0x101
CLIFF_W, CLIFF_E, CLIFF_TOP, CLIFF, CLIFF_SW, CLIFF_SE = 0x73, 0x75, 0x7C, 0xA9, 0x7B, 0x7D
SHORE_W, SHORE_E, SHORE_S, SHORE_SW, SHORE_SE, SHORE_IN = 0x192, 0x179, 0x189, 0x19A, 0x198, 0x181
FENCE_L, FENCE_R, FENCE_B, FENCE_BL, FENCE_BR = 0x5D, 0x5F, 0x66, 0x65, 0x67
FENCE_POLE, FLAG_L, FLAG_R = 0x3FD, 0x39E, 0x39F
VFLAG_TOP, VFLAG_BOT = 0x3F6, 0x3F5        # vlag aan een verticaal hek (+ 0x3F7 rechts ernaast)
PLANTER = ((0x2C8, 0x2CB, 0x2F7), (0x2D0, 0x2CC, 0x2FF), (0x2C9, 0x2CD, 0x307))


def read_pal(data):
    return [tuple(map(int, l.split())) for l in data.decode().replace('\r', '').split('\n')[3:19]]


RGB = [read_pal(open(GEN + 'palettes/%02d.pal' % p, 'rb').read()) for p in range(6)] + \
      [read_pal(open(TS + 'palettes/%02d.pal' % p, 'rb').read()) for p in range(6, 13)]


def unify(block, pals):
    """Tile met pixels uit meerdere paletten: zet alles om naar één palet met dezelfde RGB-kleuren."""
    for p in sorted(pals):
        out = []
        for v in block:
            if v is None or v[0] == p:
                out.append(v)
                continue
            idx = [i for i in range(1, 16) if RGB[p][i] == RGB[v[0]][v[1]]]
            if not idx:
                break
            out.append((p, idx[0]))
        else:
            return out
    raise AssertionError('tile met meerdere paletten: %s' % pals)


def git(path):
    return subprocess.check_output(['git', 'show', '%s:%s' % (ORIG, path)])


def png(data):
    im = Image.open(io.BytesIO(data))
    im.load()
    return im


# ---------------------------------------------------------------- pixels van bestaande metatiles
class Tiles:
    """Leest metatiles (secondary + General) als 16x16 (palet, kleur)/None."""
    def __init__(self, sec_mts, sec_tiles, gen_mts, gen_tiles):
        self.sm, self.gm = sec_mts, gen_mts
        self.st, self.gt = sec_tiles.load(), gen_tiles.load()

    def entries(self, mid):
        src, i = (self.sm, mid - 512) if mid >= 512 else (self.gm, mid)
        return list(struct.unpack_from('<8H', src, i * 16))

    def tile(self, e):
        t = e & 0x3FF
        hf, vf, pal = (e >> 10) & 1, (e >> 11) & 1, e >> 12
        px, t = (self.gt, t) if t < 512 else (self.st, t - 512)
        tx, ty = (t % 16) * 8, (t // 16) * 8
        return [[px[tx + (7 - x if hf else x), ty + (7 - y if vf else y)] for x in range(8)] for y in range(8)], pal

    def pixels(self, mid, ground=()):
        """Beide lagen over elkaar; tiles in `ground` (onderlaag) tellen als doorzichtig."""
        e = self.entries(mid)
        out = [[None] * 16 for _ in range(16)]
        for layer in (0, 1):
            for q in range(4):
                ent = e[layer * 4 + q]
                if layer == 0 and (ent & 0x3FF) in ground:
                    continue
                if layer == 1 and (ent & 0x3FF) == 0:
                    continue
                d, pal = self.tile(ent)
                for y in range(8):
                    for x in range(8):
                        if d[y][x]:
                            out[(q // 2) * 8 + y][(q % 2) * 8 + x] = (pal, d[y][x])
        return out


# ---------------------------------------------------------------- het stadion tekenen
P1, P7 = 1, 7               # palet 1 (General: Battle Dome-kleuren), palet 7 (East: groen voor het veld)
WHITE, L1, L2, L3, G1, G2, G3, NAVY = 1, 2, 3, 4, 5, 6, 7, 8
SKY, BLUE, PEACH, ORANGE, RED, CRIMSON = 9, 10, 11, 12, 13, 14
GR_L, GR_M, GR_D = 11, 12, 13        # palet 7: lichtgroen, groen, donkergroen
PW = SW * 16
PH = SH * 16
BOWL_H = 8 * 16             # kom (bovenaanzicht) rij 0..7, gevel rij 8..13
RC = 40                     # straal van de ronde hoeken van de kom
PITCH = (3, 3, 17, 7)       # veld in metatiles (x0, y0, x1, y1), palet 7


def draw_stadium(dome):
    img = [[None] * PW for _ in range(PH)]

    def put(x, y, c, pal=P1):
        if 0 <= x < PW and 0 <= y < PH:
            img[y][x] = None if c is None else (pal, c)

    # --- kom: afgeronde rechthoek, afstand tot de buitenrand bepaalt de ringen
    def depth(x, y):
        cx = RC if x < RC else (PW - 1 - RC if x > PW - 1 - RC else x)
        if y < RC and cx != x:
            dd = math.hypot(x - cx, y - RC)
            return RC - dd, 'c'
        dx = min(x, PW - 1 - x)
        return (min(dx, y), 'x' if dx < y else 'y')

    px0, py0, px1, py1 = PITCH[0] * 16, PITCH[1] * 16, (PITCH[2] + 1) * 16, (PITCH[3] + 1) * 16
    for y in range(BOWL_H + 16):
        for x in range(PW):
            d, side = depth(x, y)
            if d < 0:
                continue
            d = int(d)
            if d == 0:
                c = NAVY
            elif d <= 2:
                c = L2
            elif d <= 10:
                c = WHITE
            elif d <= 12:
                c = L1
            elif d == 13:
                c = G1
            elif d == 14:
                c = G3
            else:
                k = (d - 15) % 6
                c = (BLUE, BLUE, SKY, SKY, BLUE, G3)[k] if k < 5 else G3
                c = (SKY, BLUE, BLUE, BLUE, L3, G3)[k]
                # trappen tussen de vakken (elke 32 px, loodrecht op de rand)
                along = y if side == 'x' else x
                if side != 'c' and along % 32 in (14, 15):
                    c = L2 if along % 32 == 14 else G1
            put(x, y, c)
    # muurtje om het veld
    for x in range(px0 - 2, px1 + 2):
        for y in (py0 - 2, py0 - 1):
            put(x, y, NAVY if y == py0 - 1 else G2)
    for y in range(py0 - 2, py1):
        for x in (px0 - 2, px0 - 1, px1, px1 + 1):
            put(x, y, NAVY if x in (px0 - 1, px1) else G2)
    # veld (palet 7): maaistroken per metatile, witte lijnen
    cxm = (px0 + px1) // 2
    for y in range(py0, py1):
        for x in range(px0, px1):
            c = GR_L if ((x - px0) // 16) % 2 == 0 else GR_M
            ix, iy = x - px0, y - py0
            w, h = px1 - px0, py1 - py0
            line = False
            if (iy in (3,) or iy == h - 4) and 3 <= ix <= w - 4:
                line = True
            if (ix == 3 or ix == w - 4) and 3 <= iy <= h - 4:
                line = True
            if x == cxm and 3 <= iy <= h - 4:
                line = True
            dd = math.hypot(x + 0.5 - cxm, y + 0.5 - (py0 + 40))
            if 6.0 <= dd < 7.0:
                line = True
            # doelgebiedjes aan beide kanten (binnen één metatile)
            gy0, gy1 = py0 + 34, py0 + 46
            for gx0, gx1 in ((px0 + 3, px0 + 10), (px1 - 11, px1 - 4)):
                if gy0 <= y <= gy1 and gx0 <= x <= gx1 and (x in (gx0, gx1) or y in (gy0, gy1)):
                    line = True
            put(x, y, WHITE if line else c, P7)

    # --- gevel
    fy = BOWL_H                       # 128: voorkant van het dak
    for x in range(PW):
        d, _ = depth(x, fy)
        if d < 0:
            continue
        for y in range(fy, PH):
            put(x, y, None)
    # rand van het dak (bovenkant), daarna de oranje lijst
    band = [WHITE, WHITE, WHITE, L1, L2, G1, NAVY, PEACH, ORANGE, ORANGE, ORANGE, RED, RED, CRIMSON, NAVY]
    wall_top = fy + len(band)         # 143
    base_y = PH - 10                  # plint
    for x in range(PW):
        for i, c in enumerate(band):
            put(x, fy + i, c)
    # glasgevel met witte pilaren (periode 32 px)
    for x in range(PW):
        k = x % 32
        for y in range(wall_top, base_y):
            ry = y - wall_top
            if k in (0, 7):
                c = NAVY
            elif k in (1, 2, 3):
                c = (WHITE, WHITE, L1)[k - 1]
            elif k in (4, 5, 6):
                c = (L1, L2, L3)[k - 4]
            else:
                # glas: lichtere bovenrand, horizontale stijl in het midden
                if ry < 2:
                    c = G3
                elif ry in (26, 27):
                    c = G3 if ry == 26 else L3
                elif ry < 6:
                    c = SKY
                else:
                    c = BLUE
                    if (k - 8 + ry) % 24 in (0, 1) and ry < 26 and k > 9:
                        c = SKY          # schuine weerspiegeling
            put(x, y, c)
    # plint
    for x in range(PW):
        for i, c in enumerate([NAVY, L1, L1, L2, L2, L3, L3, G1, G2, NAVY]):
            put(x, base_y + i, c)
    # zijkanten van de gevel: ronde hoekpilaren (licht links, schaduw rechts)
    cap = [NAVY, L2, WHITE, WHITE, WHITE, L1, L2, L3, G1, NAVY]
    for y in range(fy + 6, PH):
        for i, c in enumerate(cap):
            if y >= PH - 2 and i in (0, len(cap) - 1):
                continue
            cl = NAVY if y in (fy + 6, PH - 1) and 0 < i < len(cap) - 1 else c
            put(i, y, cl)
            put(PW - len(cap) + i, y, NAVY if y in (fy + 6, PH - 1) and 0 < i < len(cap) - 1 else c)
    # banieren (rood, met Poké Ball) aan de lijst, tussen de pilaren
    def banner(bx):
        for y in range(wall_top - 1, wall_top + 40):
            for x in range(bx, bx + 12):
                ry, rx = y - wall_top, x - bx
                if ry > 34 and abs(rx - 5.5) * 2 + (ry - 34) * 2 > 12:
                    continue                      # puntje onderaan
                c = RED
                if rx in (0, 11):
                    c = CRIMSON
                if ry in (-1, 0):
                    c = ORANGE if ry == 0 else NAVY
                cy = 18
                dd = math.hypot(rx - 5.5, ry - cy)
                if dd <= 4.2:
                    c = WHITE if ry > cy else RED
                    if abs(ry - cy) < 1:
                        c = NAVY
                    if dd < 1.6:
                        c = WHITE
                    if dd > 3.5:
                        c = NAVY
                put(x, y, c)
    for col in (2, 6, 14, 18):
        banner(col * 16 + 10)
    # ingang: Battle Dome-ingang (3x2 metatiles) in het midden, met een grote luifel erboven
    ex = (SW // 2 - 1) * 16
    for cy in range(2):
        for cx in range(3):
            block = dome[cy][cx]
            for y in range(16):
                for x in range(16):
                    v = block[y][x]
                    if v is not None:
                        img[PH - 32 + cy * 16 + y][ex + cx * 16 + x] = v
    # embleem boven de ingang: grote Poké Ball op een wit bord
    ecx, ecy = ex + 24, wall_top + 18
    for y in range(wall_top, PH - 32):
        for x in range(ex + 2, ex + 46):
            c = WHITE if (x - ex) not in (2, 45) else G3
            dd = math.hypot(x + 0.5 - ecx, y + 0.5 - ecy)
            if dd <= 13:
                c = RED if y + 0.5 < ecy else WHITE
                if abs(y + 0.5 - ecy) < 1.5:
                    c = NAVY
                if dd < 5:
                    c = NAVY if dd >= 3.5 else WHITE
                if dd > 12:
                    c = NAVY
            put(x, y, c)
    return img


# ---------------------------------------------------------------- bouwen
def build():
    orig_map = list(struct.unpack('<%dH' % (W * H0), git(LAY + 'map.bin')))
    mts = bytearray(git(TS + 'metatiles.bin'))
    attrs = bytearray(git(TS + 'metatile_attributes.bin'))
    tiles_img = png(git(TS + 'tiles.png'))
    border = struct.unpack('<4H', git(LAY + 'border.bin'))
    gen_mts = open(GEN + 'metatiles.bin', 'rb').read()
    gen_tiles = Image.open(GEN + 'tiles.png')
    west = Tiles(git(WEST + 'metatiles.bin'), png(git(WEST + 'tiles.png')), gen_mts, gen_tiles)

    # vrije metatiles: niet op de kaart/rand, geen deurlabel
    used = set(v & 0x3FF for v in orig_map) | set(b & 0x3FF for b in border)
    nmt = len(mts) // 16
    reserved = used | DOOR_LABELS | {DOOR_MT}
    free_mt = [512 + i for i in range(nmt) if 512 + i not in reserved] + list(range(512 + nmt, 1024))
    # 0x28A wordt de Battle Dome-deur: de bestaande 0x28A van East verhuist
    mv = free_mt.pop(0)
    mts[(mv - 512) * 16:(mv - 511) * 16] = mts[(DOOR_MT - 512) * 16:(DOOR_MT - 511) * 16]
    attrs[(mv - 512) * 2:(mv - 511) * 2] = attrs[(DOOR_MT - 512) * 2:(DOOR_MT - 511) * 2]
    orig_map = [(v & ~0x3FF) | mv if (v & 0x3FF) == DOOR_MT else v for v in orig_map]
    used = (used - {DOOR_MT}) | {mv}
    ref = set()
    for i in range(nmt):
        if 512 + i in used or 512 + i in DOOR_LABELS:
            for k in range(8):
                t = struct.unpack_from('<H', mts, i * 16 + k * 2)[0] & 0x3FF
                if t >= 512:
                    ref.add(t - 512)
    free_tiles = [t for t in range(1, NUM_TILES) if t not in ref and t not in FLAG_ANIM_TILES]

    # ---------------- terrein
    grid = [orig_map[y * W:(y + 1) * W] for y in range(H0)] + [[SEA] * W for _ in range(EXTRA)]
    C = 1 << 10                                     # collision-bit

    def setm(x, y, m, coll=None):
        if coll is None:
            coll = 0 if m in (FLOOR, FLOOR_GRASS_TOP, SEA, FLAG_L, FLAG_R) else 1
        grid[y][x] = m | (C if coll else 0)

    # oude rifrand onderaan (rij 69-71) gaat naar de nieuwe onderkant; daar weer zee
    reef = [row[:] for row in grid[69:72]]
    for y in range(69, 72):
        for x in range(W):
            grid[y][x] = SEA
    for i in range(3):
        grid[H - 3 + i] = reef[i][:]
    # alles van x 0..XS_E vanaf rij TOP opnieuw (behalve de oude kust links van het plateau)
    for y in range(TOP, H - 3):
        for x in range(0, XS_E + 1):
            if x < XS_W and y < 59:
                continue                            # oude kust (sluit aan op OutsideWest)
            if x <= XF_W and y < 56:
                continue                            # vlaggen en hek van de oude kust
            if x >= XF_E and y < SY:
                continue                            # bomenrij rechts van het plein
            setm(x, y, SEA)
    # kust links: oude zuidklif (rij 56-58) eindigt tegen de nieuwe westklif
    for y in range(56, 59):
        setm(XS_W, y, (CLIFF_TOP, CLIFF, CLIFF)[y - 56])
    setm(XS_W, 59, SHORE_IN)
    for x in range(XS_W):
        setm(x, 59, SHORE_S)
    # plateau
    for y in range(TOP, YF):
        for x in range(XF_W + 1, XF_E):
            if y < SY and x >= XF_E - 4:
                continue
            setm(x, y, FLOOR)
    for y in range(TOP, SY):                        # rechts boven: oude grasstrook met bomen blijft
        for x in range(XF_E - 4, XF_E + 2):
            grid[y][x] = orig_map[y * W + x] if y < H0 else SEA
    for x in range(18, 27):                          # rand van de oude bloementuin
        setm(x, TOP - 1, FLOOR)
    for x in range(XF_E - 4, XF_E):
        setm(x, SY, FLOOR_GRASS_TOP)
    # westkant: klif + hek met vlaggen
    for y in range(56, YC + 3):
        setm(XC_W, y, CLIFF_W if y < YC + 2 else CLIFF_SW)
        if y >= 60:
            setm(XS_W, y, SHORE_W)
    setm(XS_W, YC + 3, SHORE_SW)
    for y in range(56, YF):
        setm(XF_W, y, FENCE_L)
    for y in range(57, YF - 2, 5):
        setm(XF_W, y, VFLAG_TOP)
        setm(XF_W + 1, y, 0x3F7, 0)
        setm(XF_W, y + 1, VFLAG_BOT)
    # oostkant: hek + klif
    for y in range(SY, YC + 3):
        setm(XC_E, y, CLIFF_E if y < YC + 2 else CLIFF_SE)
        if SY < y and not (64 <= y <= 67):          # de waterval blijft
            setm(XS_E, y, SHORE_E)
    grid[SY][XS_E] = orig_map[SY * W + XS_E]        # binnenhoek onder de grasstrook (0x180)
    setm(XS_E, YC + 3, SHORE_SE)
    for y in range(SY, YF):
        setm(XF_E, y, FENCE_R)
    # zuidkant: hek met vlaggen, klif van drie rijen, kustlijn
    setm(XF_W, YF, FENCE_BL)
    setm(XF_E, YF, FENCE_BR)
    for x in range(XF_W + 1, XF_E):
        pole = (x - XF_W) % 3 == 1
        setm(x, YF, FENCE_POLE if pole else FENCE_B)
        if pole:
            setm(x, YF - 1, FLAG_L, 0)
            setm(x + 1, YF - 1, FLAG_R, 0)
    for x in range(XF_W, XC_E):
        setm(x, YC, CLIFF_TOP)
        setm(x, YC + 1, CLIFF)
        setm(x, YC + 2, CLIFF)
    for x in range(XC_W, XS_E):
        setm(x, YC + 3, SHORE_S)
    # bloembakken op het voorplein
    for bx in (SX + 1, SX + SW - 6):
        for j in range(3):
            for i in range(5):
                row = PLANTER[j]
                setm(bx + i, SY + SH + 1 + j, row[0] if i == 0 else (row[2] if i == 4 else row[1]))
    # half overschreven rotsen in zee opruimen
    rocks = set(ROCK)
    for y in range(H):
        for x in range(W):
            m = grid[y][x] & 0x3FF
            if m not in rocks:
                continue
            i = ROCK.index(m)
            ox, oy = x - (i % 2), y - (i // 2)
            ok = all(0 <= ox + a < W and 0 <= oy + b < H and grid[oy + b][ox + a] & 0x3FF == ROCK[b * 2 + a]
                     for a in (0, 1) for b in (0, 1))
            if not ok:
                grid[y][x] = SEA | (grid[y][x] & 0xFC00)
    # een paar rotsen in de nieuwe zee
    for rx, ry in ((1, 66), (8, YC + 6), (27, YC + 5), (41, 75), (52, 79), (63, 73), (69, 80), (20, H - 7)):
        if all(grid[ry + b][rx + a] & 0x3FF == SEA for a in (0, 1) for b in (0, 1)):
            for a in (0, 1):
                for b in (0, 1):
                    grid[ry + b][rx + a] = ROCK[b * 2 + a] | C

    # ---------------- stadion
    ground = {0x002, 0x003}                          # gras onder de Dome telt als doorzichtig
    dome = [[west.pixels(m, ground) for m in r] for r in ((0x2D3, 0x282, 0x2D5), (0x2DB, DOOR_MT, 0x2DD))]
    pix = draw_stadium(dome)
    tiles_px = tiles_img.load()
    tile_index, out_tiles = {}, {}

    def get_tile(block):
        if all(v is None for v in block):
            return 0
        pals = set(v[0] for v in block if v)
        if len(pals) > 1:
            block = unify(block, pals)
            pals = set(v[0] for v in block if v)
        pal = pals.pop()
        data = tuple(v[1] if v else 0 for v in block)
        for hf in (0, 1):
            for vf in (0, 1):
                d = tuple(data[(7 - r if vf else r) * 8 + (7 - c if hf else c)] for r in range(8) for c in range(8))
                if (pal, d) in tile_index:
                    return (512 + tile_index[(pal, d)]) | (hf << 10) | (vf << 11) | (pal << 12)
        t = free_tiles.pop(0)
        tile_index[(pal, data)] = t
        out_tiles[t] = data
        return (512 + t) | (pal << 12)

    floor_bottom = list(struct.unpack_from('<8H', gen_mts, FLOOR * 16))[:4]
    mt_index = {}
    for my in range(SH):
        for mx in range(SW):
            block = [[pix[my * 16 + y][mx * 16 + x] for x in range(16)] for y in range(16)]
            top = [get_tile([block[(q // 2) * 8 + i // 8][(q % 2) * 8 + i % 8] for i in range(64)]) for q in range(4)]
            gx, gy = SX + mx, SY + my
            if (gx, gy) == DOOR:
                struct.pack_into('<8H', mts, (DOOR_MT - 512) * 16, *(floor_bottom + top))
                struct.pack_into('<H', attrs, (DOOR_MT - 512) * 2, MB_ANIMATED_DOOR | COVERED)
                grid[gy][gx] = DOOR_MT
                continue
            if all(t == 0 for t in top):
                setm(gx, gy, FLOOR)
                continue
            key = tuple(top)
            if key not in mt_index:
                m = free_mt.pop(0)
                mt_index[key] = m
                if m - 512 >= len(mts) // 16:
                    mts += b'\0' * ((m - 512 + 1) * 16 - len(mts))
                    attrs += b'\0' * ((m - 512 + 1) * 2 - len(attrs))
                struct.pack_into('<8H', mts, (m - 512) * 16, *(floor_bottom + top))
                struct.pack_into('<H', attrs, (m - 512) * 2, COVERED)
            grid[gy][gx] = mt_index[key] | C
    for t, data in out_tiles.items():
        tx, ty = (t % 16) * 8, (t // 16) * 8
        for i, c in enumerate(data):
            tiles_px[tx + i % 8, ty + i // 8] = c
    print('stadion: %d metatiles (+1 deur, +1 verhuisd), %d tiles (vrij over: %d metatiles, %d tiles)'
          % (len(mt_index), len(out_tiles), len(free_mt), len(free_tiles)))

    open(LAY + 'map.bin', 'wb').write(b''.join(struct.pack('<H', grid[y][x]) for y in range(H) for x in range(W)))
    open(TS + 'metatiles.bin', 'wb').write(bytes(mts))
    open(TS + 'metatile_attributes.bin', 'wb').write(bytes(attrs))
    tiles_img.save(TS + 'tiles.png')
    return pix


def metadata():
    lj = open('data/layouts/layouts.json').read()
    i = lj.index('"id": "LAYOUT_BATTLE_FRONTIER_OUTSIDE_EAST"')
    j = lj.index('}', i)
    lj = lj[:i] + re.sub(r'"height": \d+', '"height": %d' % H, lj[i:j], 1) + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)

    # map.json OutsideEast: deur van het stadion (achteraan, dus bestaande warp-id's blijven gelijk)
    m = json.loads(git(MAPJ))
    m['warp_events'].append({'x': DOOR[0], 'y': DOOR[1], 'elevation': 0, 'dest_map': LOBBY, 'dest_warp_id': '0'})
    open(MAPJ, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    return len(m['warp_events']) - 1


# ---------------------------------------------------------------- binnenkaarten
def obj(gfx, x, y, mv, script, lid=None, elev=0):
    return dict(([('local_id', lid)] if lid else []) + [
        ('graphics_id', gfx), ('x', x), ('y', y), ('elevation', elev), ('movement_type', mv),
        ('movement_range_x', 1), ('movement_range_y', 1), ('trainer_type', 'TRAINER_TYPE_NONE'),
        ('trainer_sight_or_berry_tree_id', '0'), ('script', script), ('flag', '0')])


def interior(name, const, src, layout_after, music, objects, warps, bgs, script):
    """Kopie van een vanilla layout (eigen map) + map.json; voegt layout, mapgroep en include toe."""
    src_layout = json.loads(open('data/maps/%s/map.json' % src).read())['layout']
    lay = [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id') == src_layout][0]
    os.makedirs('data/layouts/' + name, exist_ok=True)
    for f in ('map.bin', 'border.bin'):
        shutil.copy('data/layouts/%s/%s' % (src, f), 'data/layouts/%s/%s' % (name, f))
    lj = open('data/layouts/layouts.json').read()
    if '"LAYOUT_%s"' % const not in lj:
        i = lj.index('"id": "%s"' % layout_after); j = lj.index('},', i) + 2
        lj = lj[:j] + '''
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "%s",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    },''' % (const, name, lay['width'], lay['height'], lay['primary_tileset'], lay['secondary_tileset'], name, name) + lj[j:]
        open('data/layouts/layouts.json', 'w').write(lj)

    base = json.loads(open('data/maps/%s/map.json' % src).read())
    m = dict(base)
    m.update({'id': 'MAP_' + const, 'name': name, 'layout': 'LAYOUT_' + const, 'music': music,
              'object_events': objects, 'warp_events': warps, 'coord_events': [], 'bg_events': bgs})
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    if not os.path.exists('data/maps/%s/scripts.inc' % name):
        open('data/maps/%s/scripts.inc' % name, 'w').write(script)

    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        last = re.search(r'\n(    "BattleFrontier_(?:SpireLobby|StadiumLobby)")\n', g)
        g = g[:last.start(1)] + last.group(1) + ',\n    "%s"' % name + g[last.end(1):]
        open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = (re.search(r'\t\.include "data/maps/BattleFrontier_StadiumLobby/scripts\.inc"\n', es)
                  or re.search(r'\t\.include "data/maps/BattleFrontier_SpireLobby/scripts\.inc"\n', es))
        es = es[:anchor.end()] + inc + es[anchor.end():]
        open('data/event_scripts.s', 'w').write(es)


LOBBY_SCRIPT = '''@ Project Grounded: lobby van het Battle Stadium (toernooien à la Pokémon World Tournament).
@ Placeholders: de toernooi-engine wordt later aan deze scripts gehangen.
BattleFrontier_StadiumLobby_MapScripts::
\t.byte 0

BattleFrontier_StadiumLobby_EventScript_SinglesDesk::
\tmsgbox BattleFrontier_StadiumLobby_Text_SinglesDesk, MSGBOX_NPC
\tend

BattleFrontier_StadiumLobby_EventScript_DoublesDesk::
\tmsgbox BattleFrontier_StadiumLobby_Text_DoublesDesk, MSGBOX_NPC
\tend

BattleFrontier_StadiumLobby_EventScript_Board::
\tmsgbox BattleFrontier_StadiumLobby_Text_Board, MSGBOX_SIGN
\tend

BattleFrontier_StadiumLobby_EventScript_Fan::
\tmsgbox BattleFrontier_StadiumLobby_Text_Fan, MSGBOX_NPC
\tend

BattleFrontier_StadiumLobby_EventScript_Scout::
\tmsgbox BattleFrontier_StadiumLobby_Text_Scout, MSGBOX_NPC
\tend

BattleFrontier_StadiumLobby_EventScript_Snacks::
\tmsgbox BattleFrontier_StadiumLobby_Text_Snacks, MSGBOX_NPC
\tend

BattleFrontier_StadiumLobby_Text_SinglesDesk:
\t.string "Welcome to the BATTLE STADIUM!\\n"
\t.string "SINGLE BATTLE tournaments, right here.\\p"
\t.string "Registration opens soon. Our\\n"
\t.string "bracket printer is still warming up.$"

BattleFrontier_StadiumLobby_Text_DoublesDesk:
\t.string "DOUBLE BATTLE tournaments!\\n"
\t.string "Twice the POKéMON, twice the paperwork.\\p"
\t.string "Please come back once the forms\\n"
\t.string "have been printed. In duplicate.$"

BattleFrontier_StadiumLobby_Text_Board:
\t.string "TOURNAMENT BRACKET\\p"
\t.string "Round 1: TBA vs. TBA\\n"
\t.string "Round 2: Winner vs. also TBA\\p"
\t.string "Someone has drawn a tiny trophy\\n"
\t.string "in the corner. It looks smug.$"

BattleFrontier_StadiumLobby_Text_Fan:
\t.string "I bought a season ticket before they\\n"
\t.string "built the stadium. Before the island,\\l"
\t.string "actually. I just had a feeling.$"

BattleFrontier_StadiumLobby_Text_Scout:
\t.string "I scout trainers for the big leagues.\\p"
\t.string "So far I've scouted the snack bar,\\n"
\t.string "the restrooms and a very nice bench.$"

BattleFrontier_StadiumLobby_Text_Snacks:
\t.string "They don't sell snacks in here.\\n"
\t.string "I'm just holding this tray for morale.$"
'''

ARENA_SCRIPT = '''@ Project Grounded: gevechtszaal van het Battle Stadium. De toernooi-engine warpt de speler hierheen.
BattleFrontier_StadiumArena_MapScripts::
\t.byte 0
'''


def interiors(warp_id):
    L, A = 'BattleFrontier_StadiumLobby', 'BattleFrontier_StadiumArena'
    # lobby: kopie van de Battle Dome-lobby (twee balies, middenmonitor met toernooischema)
    interior(L, 'BATTLE_FRONTIER_STADIUM_LOBBY', 'BattleFrontier_BattleDomeLobby',
             'LAYOUT_BATTLE_FRONTIER_SPIRE_LOBBY', 'MUS_B_DOME_LOBBY',
             [obj('OBJ_EVENT_GFX_TEALA', 5, 10, 'MOVEMENT_TYPE_FACE_DOWN', L + '_EventScript_SinglesDesk',
                  'LOCALID_STADIUM_SINGLES_DESK'),
              obj('OBJ_EVENT_GFX_TEALA', 17, 10, 'MOVEMENT_TYPE_FACE_DOWN', L + '_EventScript_DoublesDesk',
                  'LOCALID_STADIUM_DOUBLES_DESK'),
              obj('OBJ_EVENT_GFX_FAT_MAN', 1, 11, 'MOVEMENT_TYPE_WANDER_AROUND', L + '_EventScript_Fan'),
              obj('OBJ_EVENT_GFX_GENTLEMAN', 14, 14, 'MOVEMENT_TYPE_FACE_LEFT', L + '_EventScript_Scout'),
              obj('OBJ_EVENT_GFX_LASS', 8, 14, 'MOVEMENT_TYPE_WANDER_AROUND', L + '_EventScript_Snacks')],
             [{'x': x, 'y': 16, 'elevation': 0, 'dest_map': 'MAP_BATTLE_FRONTIER_OUTSIDE_EAST',
               'dest_warp_id': str(warp_id)} for x in (11, 12)],
             [{'type': 'sign', 'x': x, 'y': 10, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
               'script': L + '_EventScript_Board'} for x in (7, 15)],
             LOBBY_SCRIPT)
    # arena: kopie van de Battle Dome-gevechtszaal (publiek, omroeper, scheidsrechter)
    room = json.loads(open('data/maps/BattleFrontier_BattleDomeBattleRoom/map.json').read())
    rename = {'LOCALID_DOME_ANNOUNCER': 'LOCALID_STADIUM_ANNOUNCER', 'LOCALID_DOME_REFEREE': 'LOCALID_STADIUM_REFEREE',
              'LOCALID_DOME_PLAYER': 'LOCALID_STADIUM_PLAYER', 'LOCALID_DOME_OPPONENT': 'LOCALID_STADIUM_OPPONENT',
              'LOCALID_DOME_AUDIENCE_TWIN': 'LOCALID_STADIUM_AUDIENCE_TWIN',
              'LOCALID_DOME_AUDIENCE_WALKING': 'LOCALID_STADIUM_AUDIENCE_WALKING'}
    objs = []
    for o in room['object_events']:
        o = dict(o)
        if 'local_id' in o:
            o['local_id'] = rename[o['local_id']]
        objs.append(o)
    interior(A, 'BATTLE_FRONTIER_STADIUM_ARENA', 'BattleFrontier_BattleDomeBattleRoom',
             'LAYOUT_BATTLE_FRONTIER_STADIUM_LOBBY', 'MUS_B_DOME', objs, [], [], ARENA_SCRIPT)


if __name__ == '__main__':
    build()
    wid = metadata()
    interiors(wid)
    print('klaar: kaart %dx%d, stadiondeur %s (warp-id %d)' % (W, H, DOOR, wid))
    if len(sys.argv) > 1:
        subprocess.check_call(['make', TS + 'tiles.4bpp'])
        subprocess.check_call(['python3', 'tools/grounded/maptools/render_map.py', 'BattleFrontier_OutsideEast',
                               sys.argv[1], '0', str(H)])

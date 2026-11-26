# Oogvarianten op impala r2: oog 1-op-1 uit een Gen 3-sprite (pixels overnemen, alleen omkleuren naar het impalapalet).
# Rollen: L = lijn/donker, I = iris, J = donkere iris, W = wit/glimlicht. Overige bronpixels = vacht (impala blijft).
from PIL import Image, ImageDraw, ImageFont
import sys
RONDE = sys.argv[1] if len(sys.argv) > 1 else "r5"
BASE = f"docs/concept/sprites/impala_lijn/impala/sprite/{RONDE}/impala_{RONDE}.png"
# palet r5 (alleen bestaande kleuren)
KLEUR = {"L": (0x1C,0x1A,0x22), "I": (0x5B,0x61,0x6C), "J": (0x3E,0x43,0x4E), "W": (0xF5,0xF7,0xF9)}
VACHT = (0xB5,0xBB,0xC4)
# bronpixels (x,y,rol) in bron-coördinaten + ankerpunt (midden van het oog in de bron)
BRON = {
 "rapidash":  ([(50,19,"L"),(51,19,"L"),(52,19,"L"),(49,20,"L"),(50,20,"I"),(51,20,"I"),(52,20,"W"),(50,21,"I"),(51,21,"J")], (51,20)),
 "absol":     ([(37,23,"L"),(38,23,"L"),(37,24,"W"),(38,24,"I"),(39,24,"J"),(40,24,"L")], (38,24)),
 "stantler":  ([(25,25,"L"),(26,25,"L"),(27,25,"L"),(23,26,"L"),(24,26,"L"),(25,26,"W"),(26,26,"W"),(27,26,"I"),(24,27,"L"),(25,27,"L"),(26,27,"W")], (25,26)),
}
ANKER = (21, 24)          # midden van het oog in impala r2
OUD = [(x,y) for x in range(19,25) for y in range(22,27)]   # oude oog (donker + oogwit uit de reductie)
base = Image.open(BASE).convert("RGBA")
def maak(naam):
    im = base.copy(); px = im.load()
    if naam != "model":
        for (x,y) in OUD:
            if px[x,y][:3] in [KLEUR["L"], KLEUR["W"], KLEUR["J"]]: px[x,y] = VACHT+(255,)
        pts, (ax,ay) = BRON[naam]
        for (x,y,r) in pts: px[ANKER[0]+x-ax, ANKER[1]+y-ay] = KLEUR[r]+(255,)
    return im
namen = ["model"] + list(BRON)
S = 8; f = ImageFont.load_default(size=16)
vel = Image.new("RGB", (len(namen)*(64*S+10), 64*S+130), "white"); d = ImageDraw.Draw(vel)
for i,n in enumerate(namen):
    im = maak(n); x0 = i*(64*S+10)
    if n != "model": im.save(f"docs/concept/sprites/impala_lijn/impala/oog/impala_{RONDE}_oog_{n}.png")
    bg = Image.new("RGBA", im.size, (255,255,255,255)); bg.alpha_composite(im)
    vel.paste(bg.convert("RGB").resize((64*S,64*S), Image.NEAREST), (x0, 30))
    vel.paste(bg.convert("RGB"), (x0+10, 64*S+50)); vel.paste(bg.convert("RGB").resize((128,128), Image.NEAREST), (x0+90, 64*S+50))
    d.text((x0+8, 6), f"{chr(65+i)}: {n}", fill="black", font=f)
vel.save(f"docs/concept/sprites/impala_lijn/impala/oog/oog_varianten_{RONDE}.png")

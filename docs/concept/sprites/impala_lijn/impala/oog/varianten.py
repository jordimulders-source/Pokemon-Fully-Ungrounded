# Oogvarianten op impala r2: oog 1-op-1 uit een Gen 3-sprite (pixels overnemen, alleen omkleuren naar het impalapalet).
# Rollen: L = lijn/donker, I = iris, J = donkere iris, W = wit/glimlicht. Overige bronpixels = vacht (impala blijft).
from PIL import Image, ImageDraw, ImageFont
BASE = "docs/concept/sprites/impala_lijn/impala/sprite/r2/impala_r2.png"
KLEUR = {"L": (0x1C,0x1A,0x22), "I": (0x4A,0x52,0x60), "J": (0x26,0x2C,0x38), "W": (0xF6,0xF8,0xFB)}
VACHT = (0xC8,0xD2,0xDE)
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
    if naam != "r2 (model)":
        for (x,y) in OUD:
            if px[x,y][:3] in [KLEUR["L"], KLEUR["W"], (0x4A,0x52,0x60)]: px[x,y] = VACHT+(255,)
        pts, (ax,ay) = BRON[naam]
        for (x,y,r) in pts: px[ANKER[0]+x-ax, ANKER[1]+y-ay] = KLEUR[r]+(255,)
    return im
namen = ["r2 (model)"] + list(BRON)
S = 8; f = ImageFont.load_default(size=16)
vel = Image.new("RGB", (len(namen)*(64*S+10), 64*S+130), "white"); d = ImageDraw.Draw(vel)
for i,n in enumerate(namen):
    im = maak(n); x0 = i*(64*S+10)
    if n != "r2 (model)": im.save(f"docs/concept/sprites/impala_lijn/impala/oog/impala_oog_{n}.png")
    bg = Image.new("RGBA", im.size, (255,255,255,255)); bg.alpha_composite(im)
    vel.paste(bg.convert("RGB").resize((64*S,64*S), Image.NEAREST), (x0, 30))
    vel.paste(bg.convert("RGB"), (x0+10, 64*S+50)); vel.paste(bg.convert("RGB").resize((128,128), Image.NEAREST), (x0+90, 64*S+50))
    d.text((x0+8, 6), f"{chr(65+i)}: {n}", fill="black", font=f)
vel.save("docs/concept/sprites/impala_lijn/impala/oog/oog_varianten.png")

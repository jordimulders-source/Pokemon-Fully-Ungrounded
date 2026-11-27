# Oog A (model) iets doortastender: alleen bestaande pixels van het oog omkleuren (bovenlid zwaarder, minder wit), varianten naast elkaar
from PIL import Image, ImageDraw, ImageFont
B = "docs/concept/sprites/impala_lijn/impala/sprite/r5/impala_r5.png"
L, W, V, S = (0x1C,0x1A,0x22), (0xF5,0xF7,0xF9), (0xB5,0xBB,0xC4), (0x5B,0x61,0x6C)
H = (0xD5,0xDA,0xE0)   # lichte kop-vachttint naast het oog
# Jordi: "nee moet niet groter, maar iets zelfverzekerder" (over het oog): geen extra donker, wit boven/naast de pupil wordt vacht (lid zakt)
VAR = {
 "A":  {},
 "B1": {(21,22):H, (22,22):H, (20,23):H},                                       # bovenlid zakt: wit boven de pupil wordt vacht
 "B2": {(21,22):H, (22,22):H, (20,23):H, (23,23):H},                            # + buitenhoek ook: blik smaller, rustig
 "B3": {(21,22):H, (22,22):H, (20,23):H, (20,26):V, (21,26):V, (22,26):V},      # + witte onderrand weg
}
S8 = 10; f = ImageFont.load_default(size=16)
vel = Image.new("RGB", (len(VAR)*(26*S8+10), 22*S8+120), "white"); d = ImageDraw.Draw(vel)
for i,(n,ch) in enumerate(VAR.items()):
    im = Image.open(B).convert("RGBA"); px = im.load()
    for (x,y),c in ch.items(): px[x,y] = c+(255,)
    if n != "A": im.save(f"docs/concept/sprites/impala_lijn/impala/oog/impala_r5_oog_{n}.png")
    bg = Image.new("RGBA", im.size, (255,255,255,255)); bg.alpha_composite(im); bg = bg.convert("RGB")
    x0 = i*(26*S8+10)
    vel.paste(bg.crop((8,12,34,34)).resize((26*S8,22*S8), Image.NEAREST), (x0, 28))
    vel.paste(bg, (x0+10, 22*S8+40)); vel.paste(bg.resize((128,128), Image.NEAREST).crop((0,0,128,80)), (x0+90, 22*S8+40))
    d.text((x0+6, 6), n, fill="black", font=f)
vel.save("docs/concept/sprites/impala_lijn/impala/oog/blik_varianten2.png")

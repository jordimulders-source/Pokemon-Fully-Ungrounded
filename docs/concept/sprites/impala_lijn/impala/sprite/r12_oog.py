# r12 = r11 (eindkeuring) + oog B3 (Jordi, 26 nov: "b3"): alleen pixels binnen de oogzone, omgekleurd naar bestaande vachttinten
from PIL import Image
D = "docs/concept/sprites/impala_lijn/impala"
im = Image.open(f"{D}/sprite/r11/impala_r11.png"); assert im.mode == "P"
pal = im.getpalette()[:48]; cols = [tuple(pal[i:i+3]) for i in range(0, 48, 3)]
def idx(c): return cols.index(c)
H, V = idx((0xD5,0xDA,0xE0)), idx((0xB5,0xBB,0xC4))
px = im.load()
for (x,y) in [(21,22),(22,22),(20,23)]: px[x,y] = H
for (x,y) in [(20,26),(21,26),(22,26)]: px[x,y] = V
im.save(f"{D}/sprite/r12/impala_r12.png", transparency=0)
rgba = Image.open(f"{D}/sprite/r12/impala_r12.png").convert("RGBA")
rgba.resize((512,512), Image.NEAREST).save(f"{D}/sprite/r12/impala_r12_8x.png")
print("ok", len(set(Image.open(f"{D}/sprite/r12/impala_r12.png").getdata())), "kleuren gebruikt")

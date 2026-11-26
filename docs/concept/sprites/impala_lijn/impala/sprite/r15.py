# r15 = r14 + grens wit borstvlak / grijze flank (x23-25, y32-41) als boog i.p.v. 7 rijen recht.
# Jordi (26 nov): "het witte vlak op de borst heeft nog steeds een lange verticale lijn".
# Gemeten in het model (rechterrand van het witte vlak, sprite-x): y34 23,9 · y36 23,9 · y37 24,1 · y38 24,3 · y39 24,8 · y40 (buik) -
# -> de grens buigt vanaf y37 naar buiten. Trap was 7-1-1 (x24 y32-38 grijs), wordt 5-2-2: wit tot x24 op y37-38, tot x25 op y39.
from PIL import Image
im = Image.open("docs/concept/sprites/impala_lijn/impala/sprite/r14/impala_r14.png"); assert im.mode == "P"
pal = im.getpalette()[:48]; cols = [tuple(pal[i:i+3]) for i in range(0,48,3)]
W, G = cols.index((0xF5,0xF7,0xF9)), cols.index((0xB5,0xBB,0xC4))
px = im.load()
for (x,y) in [(24,37),(24,38),(25,39)]:
    assert px[x,y] == G, (x,y,px[x,y]); px[x,y] = W
im.save("docs/concept/sprites/impala_lijn/impala/sprite/r15/impala_r15.png", transparency=0)
Image.open("docs/concept/sprites/impala_lijn/impala/sprite/r15/impala_r15.png").convert("RGBA").resize((512,512), Image.NEAREST).save("docs/concept/sprites/impala_lijn/impala/sprite/r15/impala_r15_8x.png")
print("ok")

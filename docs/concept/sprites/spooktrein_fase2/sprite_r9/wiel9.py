# Jordi 17 nov: "het wiel is minder mooi geworden, die was eerst dikker".
# A: wielzone van r4 terug (alleen groene pixels, x20-31 y45-56); B: schone ring van 2 px (index 5), binnen licht (3), rond 4.
from PIL import Image, ImageDraw
G = (2, 3, 4, 5, 6)
r8 = Image.open('sprite_r8/sprite.png'); r4 = Image.open('sprite_r4/sprite.png').load()
def opslaan(im, n):
    im.save(f'sprite_r9/sprite_{n}.png', transparency=0)
    im.convert('RGB').resize((512, 512), Image.NEAREST).save(f'sprite_r9/sprite_{n}_8x.png')
A = r8.copy(); a = A.load(); na = 0
for y in range(45, 57):
    for x in range(20, 32):
        if a[x, y] in G and r4[x, y] in G and a[x, y] != r4[x, y]: a[x, y] = r4[x, y]; na += 1
opslaan(A, 'A')
B = r8.copy(); b = B.load(); nb = 0
cx, cy = 26, 51.5
for y in range(45, 57):
    for x in range(20, 32):
        if b[x, y] not in G: continue
        d_out = ((x + .5 - cx) / 5.0) ** 2 + ((y + .5 - cy) / 5.8) ** 2
        d_in = ((x + .5 - cx) / 3.0) ** 2 + ((y + .5 - cy) / 3.8) ** 2
        v = 3 if d_in <= 1 else 5 if d_out <= 1 else 4
        if b[x, y] != v: b[x, y] = v; nb += 1
opslaan(B, 'B')
print('A', na, 'B', nb)
ims = []
for n, lab in (('sprite_r8/sprite', 'nu (r8)'), ('sprite_r4/sprite', 'eerder (r4)'), ('sprite_r9/sprite_A', 'A: wiel van r4 terug'), ('sprite_r9/sprite_B', 'B: ring 2 px dik')):
    im = Image.open(n + '.png').convert('RGB')
    z = im.crop((14, 40, 38, 60)).resize((288, 240), Image.NEAREST)
    t = Image.new('RGB', (300, 400), 'white'); t.paste(z, (0, 20)); t.paste(im.resize((128, 128), Image.NEAREST), (0, 268)); t.paste(im, (140, 268))
    ImageDraw.Draw(t).text((4, 4), lab, fill='black'); ims.append(t)
s = Image.new('RGB', (4 * 310, 400), 'white')
for i, t in enumerate(ims): s.paste(t, (i * 310, 0))
s.save('sprite_r9/wiel_varianten.png')

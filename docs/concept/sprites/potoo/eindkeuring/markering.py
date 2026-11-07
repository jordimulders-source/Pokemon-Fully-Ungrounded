"""Markeert de reparatiepixels uit RAPPORT.md op de kandidaat (12x, met nummer). Vanuit repo-root."""
from PIL import Image, ImageDraw
P = 'docs/concept/sprites/potoo/'
R = {1: [(29,40),(30,40),(31,40),(32,40),(29,41),(31,41),(32,41),(34,28),(34,29),(34,30),(34,31),(34,32)],
     2: [(25,29),(24,30),(31,33),(32,33),(31,38),(25,39),(33,40),(30,41)],
     3: [(35,28),(35,29),(37,28)],
     4: [(43,38),(43,39),(42,36),(42,37),(44,31),(44,32)],
     5: [(38,4),(38,5),(39,6)],
     6: [(25,23)],
     7: [(39,56),(39,58)]}
im = Image.open(P + 'kandidaat/potoo.png')
S = 12
rgb = Image.new('RGB', (64, 64), (200, 208, 216))
m = Image.new('L', (64, 64), 0)
for y in range(64):
    for x in range(64):
        if im.getpixel((x, y)): m.putpixel((x, y), 255)
rgb.paste(im.convert('RGB'), (0, 0), m)
v = rgb.crop((14, 0, 50, 64)).resize((36 * S, 64 * S), Image.NEAREST)
d = ImageDraw.Draw(v)
for k, pts in R.items():
    for x, y in pts:
        X, Y = (x - 14) * S, y * S
        d.rectangle([X, Y, X + S - 1, Y + S - 1], outline=(255, 0, 0), width=2)
        d.text((X + 3, Y + 1), str(k), fill=(255, 0, 0))
for x in range(14, 50, 2):
    d.text(((x - 14) * S + 1, 64 * S - 11), str(x % 100), fill=(0, 0, 160))
for y in range(0, 64, 2):
    d.text((1, y * S + 1), str(y), fill=(0, 0, 160))
v.save(P + 'eindkeuring/markering.png')

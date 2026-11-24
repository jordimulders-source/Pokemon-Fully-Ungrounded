# r16 = r15 + rechterhoek jaspand ronder (Jordi: "als je dit hoekje wat minder recht kan maken vind ik hem goed").
# Alleen randpixels weghalen en de omlijning 1 px naar binnen verschuiven; niets bijgetekend.
from PIL import Image
im = Image.open('sprite_r15/mr_prime.png'); p = im.load()
zet = {(53,43):0,(52,43):1,(53,44):0,(52,44):1,(53,45):0,(52,45):0}
for (x,y),v in zet.items(): p[x,y] = v
im.save('sprite_r16/mr_prime.png')
big = Image.new('RGB',(64,64),(220,220,220)); big.paste(im.convert('RGBA'),(0,0),im.convert('RGBA'))
big.resize((512,512),Image.NEAREST).save('sprite_r16/mr_prime_8x.png')
for y in range(38,48): print(y, ''.join('.' if p[x,y]==0 else str(p[x,y]) for x in range(44,58)))

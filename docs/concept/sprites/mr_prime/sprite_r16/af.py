# af = r16 + 3 MOET-punten en 1 MAG-punt van de eindkeuring (alleen omkleuren).
from PIL import Image
im = Image.open('sprite_r16/mr_prime.png'); p = im.load()
for (x,y),v in {(59,55):4,(55,57):7,(55,58):7,(22,29):2,(23,29):2,(51,30):1,(52,30):1}.items(): p[x,y] = v
im.save('af/mr_prime.png')
big = Image.new('RGB',(64,64),(220,220,220)); big.paste(im.convert('RGBA'),(0,0),im.convert('RGBA'))
big.resize((512,512),Image.NEAREST).save('af/mr_prime_8x.png')

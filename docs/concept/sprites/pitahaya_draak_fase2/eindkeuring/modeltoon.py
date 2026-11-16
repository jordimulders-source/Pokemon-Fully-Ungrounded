# modeltoon.py x0 y0 x1 y1 [sprite]: per spritepixel de gemiddelde modelkleur van zijn 3x3-blok -> dichtstbijzijnde paletkleur,
# naast de sprite (letters: K zwart, d r p P roze donker->licht, g G h H groen, w W vlees, s pit, v grijs gehemelte)
import sys, numpy as np; from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pitahaya_draak_fase2/'
im=Image.open(sys.argv[5] if len(sys.argv)>5 else B+'sprite_r9/pitahaya2_r9A.png'); a=np.array(im); pal=np.array(im.getpalette()[:42]).reshape(14,3)
nat=np.array(Image.open(B+'sprite_r9/natief.png').convert('RGB')).astype(int); fg=nat.min(2)<225
N='.KdrpPgGhHwWsv'
x0,y0,x1,y1=map(int,sys.argv[1:5])
print('    '+''.join(str(x%10) for x in range(x0,x1))+'   '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1):
    m=''
    for x in range(x0,x1):
        bl=nat[3*(y-13):3*(y-13)+3,2+3*x:5+3*x]; f=fg[3*(y-13):3*(y-13)+3,2+3*x:5+3*x]
        if f.sum()<5: m+='.'; continue
        c=bl[f].mean(0); m+=N[1+((pal[1:]-c)**2).sum(1).argmin()]
    print('%2d  %s   %s'%(y,''.join(N[v] for v in a[y,x0:x1]),m))

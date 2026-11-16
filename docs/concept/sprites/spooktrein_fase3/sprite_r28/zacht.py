# Jordi 16 nov: "de zwarte lijnen in het gezicht en de koeienvanger voelen nog wat hard".
# Binnenlijnen (zwart idx 1, niet grenzend aan transparant) in kop- en koeienvangerzone -> donkere tint.
# A: nieuwe index 15 = zeer donker roestbruin; B: idx 9 (roestdonker). Buitenlijn blijft zwart.
from PIL import Image; import numpy as np
im=Image.open('sprite_r27/sprite.png'); a=np.array(im); pal=im.getpalette()
H,W=a.shape
def binnen(y,x):
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if not(0<=yy<H and 0<=xx<W) or a[yy,xx]==0: return False
    return True
zone=np.zeros_like(a,bool); zone[20:61,0:33]=True
mask=np.zeros_like(a,bool)
for y in range(H):
    for x in range(W):
        if zone[y,x] and a[y,x]==1 and binnen(y,x): mask[y,x]=True
print('binnenlijnpixels',mask.sum(),'van zwart in zone',((a==1)&zone).sum())
for naam,idx,rgb in (('A',15,(62,32,26)),('B',9,None)):
    b=a.copy(); b[mask]=idx; p=list(pal)
    if rgb: p[idx*3:idx*3+3]=list(rgb)
    o=Image.fromarray(b,'P'); o.putpalette(p); o.save(f'sprite_r28/sprite_{naam}.png',transparency=0)
ims=[]
for f in ['sprite_r27/sprite.png','sprite_r28/sprite_A.png','sprite_r28/sprite_B.png']:
    s=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(s); ims.append(bg.convert('RGB'))
v=Image.new('RGB',(3*512+40,512+140),(235,235,235))
for i,m in enumerate(ims):
    v.paste(m.resize((512,512),Image.NEAREST),(i*532,0)); v.paste(m.resize((128,128),Image.NEAREST),(i*532,520)); v.paste(m,(i*532+140,520))
v.save('sprite_r28/vel_r27_A_B.png')

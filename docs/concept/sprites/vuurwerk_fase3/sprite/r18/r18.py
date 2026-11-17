# Jordi (16 nov): "linksbovenin is een afgekapt stuk vuurwerk, maar dat gaat er raar uitzien in een gevecht denk je niet?"
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
src=Image.open('../../af/vuurwerkslang.png'); a0=np.array(src); pal=src.getpalette()
lab,n=ndimage.label(a0>0)                      # 4-buren
main=np.bincount(lab.ravel())[1:].argmax()+1
SP={6,7,8}
def los_spikkels(sel):
    m=np.zeros_like(a0,bool)
    for i in range(1,n+1):
        if i==main: continue
        c=lab==i; kleuren=set(np.unique(a0[c]))
        if kleuren<=SP and sel(np.argwhere(c)): m|=c
    return m
tl=los_spikkels(lambda p: p[:,0].max()<15)     # barst linksboven (y<15)
bl=los_spikkels(lambda p: p[:,0].min()>=25)    # barst linksonder
def save(a,k):
    im=Image.fromarray(a,'P'); im.putpalette(pal); im.save(f'sprite_{k}.png',transparency=0)
a1=a0.copy(); a1[tl]=0; save(a1,'1_linksboven_weg')
# 2: ook de barst linksonder 2 px naar rechts, zodat hij de rand niet raakt (alleen op lege plekken)
a2=a1.copy(); ys,xs=np.where(bl); a2[bl]=0
ok=all(a2[y,x+2]==0 for y,x in zip(ys,xs))
for y,x in zip(ys,xs):
    if a2[y,x+2]==0: a2[y,x+2]=a0[y,x]
save(a2,'2_ook_linksonder_verschoven')
print('linksboven weg',tl.sum(),'px; linksonder',bl.sum(),'px, botsingsvrij:',ok, '; x=0 nog bezet:',np.nonzero(a2[:,0])[0])
outs=[('af (nu)','../../af/vuurwerkslang.png'),('1 linksboven weg','sprite_1_linksboven_weg.png'),('2 + linksonder 2px naar rechts','sprite_2_ook_linksonder_verschoven.png')]
S=6; W=Image.new('RGB',(16+3*(64*S+20),64*S+60+140),(235,235,235)); d=ImageDraw.Draw(W)
for i,(k,f) in enumerate(outs):
    r=Image.open(f).convert('RGBA'); x=16+i*(64*S+20); d.text((x,4),k,fill=(0,0,0))
    for j,c in enumerate([(255,255,255),(40,40,48)]):
        b=Image.new('RGBA',r.size,c+(255,)); b.alpha_composite(r)
        if j==0: W.paste(b.resize((64*S,64*S),Image.NEAREST).convert('RGB'),(x,20))
        W.paste(b.resize((128,128),Image.NEAREST).convert('RGB'),(x+j*140,64*S+40))
W.save('vel.png')

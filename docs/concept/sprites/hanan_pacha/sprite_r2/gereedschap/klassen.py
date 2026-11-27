# Klassen per natieve modelpixel: 0 achtergrond, 1 omlijning (L<44), 2 donkere punt (grijszwart L 44-90), 3 rood (kop/kam),
# 4 goud, 5 wit/grijs (band, kraag, dij, snavel, klauwen), 6 oranje (alleen r5)
import numpy as np; from PIL import Image
from collections import deque
def klassen(pad):
    a=np.asarray(Image.open(pad).convert('RGB')).astype(int)
    r,g,b=a[...,0],a[...,1],a[...,2]; L=(r*299+g*587+b*114)/1000; mx=a.max(2); mn=a.min(2)
    rf,gf,bf=r/255,g/255,b/255; d=(mx-mn).astype(float)
    hue=np.zeros(L.shape)
    m=d>0
    hr=((gf-bf)/np.maximum(d/255,1e-6))%6; hg=(bf-rf)/np.maximum(d/255,1e-6)+2; hb=(rf-gf)/np.maximum(d/255,1e-6)+4
    hue=np.where(mx==r,hr,np.where(mx==g,hg,hb))*60
    sat=d/np.maximum(mx,1)
    c=np.full(L.shape,5)                                   # wit/grijs
    col=sat>0.30
    c[col&((hue<14)|(hue>320))]=3                          # rood
    c[col&(hue>=14)&(hue<32)]=6                            # oranje
    c[col&(hue>=32)&(hue<75)]=4                            # goud
    c[(~col)&(L<110)]=2                                    # donkere punt
    c[L<40]=1                                              # omlijning
    # achtergrond: floodfill vanaf de rand over bijna-wit zonder kleur
    bgc=(mn>=236)&(mx-mn<12)
    H,W=L.shape; bg=np.zeros_like(bgc); q=deque()
    for y in range(H):
        for x in (0,W-1): q.append((y,x))
    for x in range(W):
        for y in (0,H-1): q.append((y,x))
    while q:
        y,x=q.popleft()
        if y<0 or x<0 or y>=H or x>=W or bg[y,x]: continue
        if not (bgc[y,x] or y<3 or x<3 or y>=H-3 or x>=W-3): continue
        bg[y,x]=1; q.extend(((y+1,x),(y-1,x),(y,x+1),(y,x-1)))
    c[bg.astype(bool)]=0
    return a,c,L
if __name__=='__main__':
    import sys
    a,c,L=klassen(sys.argv[1])
    kl=np.array([[255,255,255],[0,0,0],[90,90,90],[220,30,60],[230,190,40],[160,200,255],[255,130,0]],'uint8')
    im=Image.fromarray(kl[c]); im.resize((im.width*5,im.height*5),Image.NEAREST).save(sys.argv[2])
    print(np.bincount(c.ravel(),minlength=7))

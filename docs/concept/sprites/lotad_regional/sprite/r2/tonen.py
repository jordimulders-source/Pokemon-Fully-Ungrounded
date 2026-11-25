# Toonkaart per natieve modelpixel: materiaal + toon (drempels op de 4 gemeten modeltonen per materiaal),
# daarna een modusfilter (3x3 meerderheid binnen hetzelfde materiaal, geen nieuwe tinten, geen middeling) tegen Gemini-ruis.
import numpy as np; from PIL import Image
from klassen import klassen_r8; from gemeen import PAL
def tint(m,l):
    if m==2: return 2 if l<80 else 3 if l<114 else 4 if l<150 else 5
    if m==3: return 2 if l<97 else 3 if l<120 else 4 if l<139 else 5
    if m==4: return 6 if l<125 else 10 if l<172 else 11
    if m==5: return 6 if l<120 else 7 if l<161 else 8 if l<188 else 9
    if m==6: return 6 if l<99 else 3 if l<112 else 4 if l<130 else 5          # poten: 92/102-109/11x/147
def toonkaart(rondes=1):
    a,c,L=klassen_r8(); c=c.copy(); L=L.copy()
    kopL=np.median(L[c==3]); oog=c==7; L[oog]=kopL; c[oog]=3
    H,W=c.shape; t=np.zeros((H,W),int)
    for y in range(H):
        for x in range(W):
            if c[y,x]>=2: t[y,x]=tint(c[y,x],L[y,x])
            elif c[y,x]==1: t[y,x]=1
    # r2: kraag op cumulatief oppervlak (zoals r8/kleur_r1.py): percentiel van de modelhelderheid binnen de kraag
    # -> r1-kraagkleur op hetzelfde oppervlaktepercentiel. r1-kraag (r1_tinten.py, k=5): (87,66,43) 203 + (104,82,55) 89 -> 6,
    # (120,108,77) 168 -> 7, (161,132,92) 418 -> 8, (223,195,127) 38 -> 9; samen 916 px.
    kr=c==5; P=np.cumsum([292,168,418])/916.0
    drempel=np.percentile(L[kr],100*P)
    t[kr]=np.where(L[kr]<drempel[0],6,np.where(L[kr]<drempel[1],7,np.where(L[kr]<drempel[2],8,9)))
    for _ in range(rondes):
        t2=t.copy()
        for y in range(1,H-1):
            for x in range(1,W-1):
                if c[y,x]<2: continue
                buur=[t[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if c[y+dy,x+dx]==c[y,x]]
                v,n=np.unique(buur,return_counts=True)
                if n.max()>=5 and (t[y,x] not in v or n[list(v).index(t[y,x])]<=2): t2[y,x]=v[n.argmax()]
        t=t2
    return c,t,L,oog
if __name__=='__main__':
    c,t,L,oog=toonkaart()
    img=np.array([PAL[k] for k in t.ravel()]).reshape(t.shape+(3,)).astype('uint8'); img[c==0]=255
    Image.fromarray(img).crop((70,15,170,110)).resize((800,760),Image.NEAREST).save('/tmp/claude-0/t.png')

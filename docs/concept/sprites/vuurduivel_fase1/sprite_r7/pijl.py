# pijl.py: 4 varianten van alleen de staartpunt op basis van vuurduivel_r7_basis.png -> pijl_A..D.png + pijl_opties.png
# Gebied van de punt: x40-52, y33-45 (stampixel (46,45) en (45-46,46) blijven). Palet r6 ongewijzigd (16 kleuren).
import numpy as np; from PIL import Image, ImageDraw
src=Image.open('vuurduivel_r7_basis.png'); pal=src.getpalette(); A0=np.array(src)
K,R,r,O=1,5,6,7; H=r  # r7-palet: hoornmidden is samengevoegd met haarrood, index 14 is nu roze
C=46
def vorm(rijen):  # rijen: {y:[(x0,x1),...]}
    S=set()
    for y,segs in rijen.items():
        for a,b in segs:
            for x in range(a,b+1): S.add((x,y))
    return S
def tri(top,hw,barb):  # driehoek met rechte randen, weerhaken onderaan, inkeping in het midden
    rij={}
    for i,h in enumerate(hw): rij[top+i]=[(C-h,C+h)]
    y=top+len(hw); m=hw[-1]
    rij[y]=[(C-m-1,C-2),(C+2,C+m+1)]           # weerhaken, inkeping x45-47
    rij[y+1]=[(C-m-1,C-m-1),(C+m+1,C+m+1)]     # scherpe punten van de weerhaken
    return vorm(rij)
def kleur(S,mode):
    out={}
    for (x,y) in S:
        rand=any((x+dx,y+dy) not in S for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
        if rand:
            out[(x,y)]= R if (x<C or (x==C and (x,y+1) in S)) else K
            continue
        # breedte van deze rij binnen de vorm
        xs=[xx for (xx,yy) in S if yy==y]; lo,hi=min(xs),max(xs); u=(x-lo)/max(1,hi-lo)
        if mode=='vuur': out[(x,y)]= O if u<0.34 else (H if u<0.67 else R)
        else:  # D: egaal rood, donkerrode schaduw rechts, één oranje lichtrand links
            out[(x,y)]= O if (x-1,y) not in S or out_edge(S,x-1,y) else (R if u>0.67 else H)
    return out
def out_edge(S,x,y): return any((x+dx,y+dy) not in S for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
V={
 'A':(tri(36,[0,1,1,2,2,3,3,4],None),'vuur','klassieke duivelspijl'),
 'B':(tri(34,[0,1,1,1,2,2,2,2,3,3],None),'vuur','smalle speerpunt'),
 'D':(tri(36,[0,1,1,2,2,3,3,4],None),'egaal','egaal rood, oranje lichtrand'),
}
spade=vorm({36:[(46,46)],37:[(45,47)],38:[(44,48)],39:[(43,49)],40:[(42,50)],41:[(42,50)],42:[(42,50)],
            43:[(42,45),(47,50)],44:[(43,44),(48,49)]})
V['C']=(spade,'vuur','schoppenpunt, strak')
V=dict(sorted(V.items()))
stam={'A':[(46,44)],'B':[(46,44)],'C':[(46,43),(46,44)],'D':[(46,44)]}
res={}
for k,(S,mode,naam) in V.items():
    a=A0.copy()
    a[33:46,40:53]=0; a[45,46]=K
    for (x,y),c in kleur(S,mode).items(): a[y,x]=c
    for x,y in stam[k]: a[y,x]=K
    im=Image.fromarray(a,'P'); im.putpalette(pal); im.save(f'pijl_{k}.png',transparency=0,bits=4); res[k]=(a,naam)
    # controle: buiten het staartpuntgebied alpha- en indexdiff 0
    m=np.ones_like(A0,bool); m[33:46,40:53]=False
    print(k,naam,'diff buiten de punt:',int((a[m]!=A0[m]).sum()),'kleuren:',len(set(a.flatten())))
def op(a,bg):
    im=Image.fromarray(a,'P'); im.putpalette(pal); b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im.convert('RGBA',)) if False else None
    im2=Image.fromarray(a,'P'); im2.putpalette(pal); im2.info['transparency']=0
    b.alpha_composite(im2.convert('RGBA')); return b.convert('RGB')
W=4*(26*8+20); vel=Image.new('RGB',(W,20+28*8+20+140),(235,235,235)); d=ImageDraw.Draw(vel)
for i,(k,(a,naam)) in enumerate(res.items()):
    X=i*(26*8+20)
    d.text((X+4,4),f'{k}: {naam}',fill='black')
    vel.paste(op(a,(255,255,255)).crop((30,28,56,56)).resize((26*8,28*8),Image.NEAREST),(X,20))
    y=20+28*8+12
    vel.paste(op(a,(255,255,255)),(X,y)); vel.paste(op(a,(40,40,56)),(X,y+68))
    vel.paste(op(a,(255,255,255)).resize((128,128),Image.NEAREST),(X+72,y))
vel.save('pijl_opties.png')

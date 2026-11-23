# Gnomini r6: omlijning volgens Dragonfly Cave (outline base per onderdeel, zwart alleen als outline shadow
# aan de schaduwkant rechts/onder en op de diepste punten, binnenlijnen in de eigen tint, lijn 1 px).
# Bron: ../af/gnomini.png. Palet: 1 zwart | muts 2<3<4<5 | huid 6<7<8<9 | broek a<b<c<d (a = streep/outline base).
from PIL import Image, ImageDraw
src=Image.open('../af/gnomini.png'); a=src.load()
M,H,P=2,6,0xa
A={}
# Muts: binnenlijn van de omgeslagen punt (de plooi; (39,23) was al 2)
for p in [(39,24),(39,25),(40,26),(40,27)]: A[p]=M
# Muts: onderkant van de rand over de neus en over het lijf (binnenlijn) -> donkerlila
for p in [(23,34),(24,34),(25,34),(26,34),(21,35),(22,35),(27,35),(28,35),
          (30,36),(31,36),(32,37),(33,37),(34,37),(35,38),(36,38),(37,38),
          (38,39),(39,39),(40,39),(41,39)]: A[p]=M
# Cluster onder de rand (2 px dik bij x=30-31): onderste rij wordt lijf (schaduwtint 7), lijn weer 1 px
for p in [(30,37),(31,37)]: A[p]=7
# Neus: zijkanten en onderkant (binnenlijnen tegen muts/lijf/armpje, en de lichtkant links) -> donkerroze
for p in [(20,36),(20,37),(20,38),(20,39),(20,40),(29,36),(29,37),(29,38),(29,39),(29,40),(28,40),
          (21,41),(22,41),(23,42),(24,42),(25,42),(26,41),(27,41)]: A[p]=H
# Armpjes tegen lijf/broek -> donkerroze
for p in [(20,45),(43,46)]: A[p]=H
# Broek: linkerkant (lichtkant) en binnenlijnen voetjes/kruis -> donkerblauw (outline base = tint van de streep)
for p in [(20,47),(21,48),(21,49),(22,50),
          (23,51),(24,52),(25,53),(26,53),(27,54),
          (40,52),(38,53),(39,53),(36,54),(37,54)]: A[p]=P
# Outline highlights (schaduwtint in de lijn op de meest belichte randen)
OH={(17,40):7,(16,41):7,(20,51):0xb,(21,51):0xb}
A.update(OH)
B=dict(A)
B_ZWART=[(28,40),(29,40),(40,52)]   # zie RAPPORT: diepste hoek rechtsonder de neus (2 px), kier boven de rechtervoet
for p in B_ZWART: B[p]=1
G=(152,208,160)
def on(im,bg,k):
    b=Image.new('RGBA',(64,64),bg+(255,) if len(bg)==3 else bg); b.alpha_composite(im.convert('RGBA'))
    return b.resize((64*k,64*k),0).convert('RGB')
op=[(x,y) for y in range(64) for x in range(64) if a[x,y]]
b0=sum(a[p]==1 for p in op)
print('af: zwart %d (%.1f%%) van %d'%(b0,100*b0/len(op),len(op)))
outs={}
for n,F in (('A',A),('B',B)):
    im=src.copy(); o=im.load()
    for p,c in F.items():
        assert a[p]==1 or p in OH,(p,a[p])
        o[p]=c
    ch=[(x,y) for y in range(64) for x in range(64) if a[x,y]!=o[x,y]]
    assert set(ch)<=set(F)
    assert all((a[x,y]==0)==(o[x,y]==0) for y in range(64) for x in range(64))  # silhouet
    assert im.getpalette()==src.getpalette()
    bl=sum(o[p]==1 for p in op)
    print(n,len(ch),'gewijzigd; zwart %d (%.1f%%)'%(bl,100*bl/len(op)))
    im.save('gnomini_%s.png'%n); outs[n]=im
# vergelijk 8x: af | A | B | gewijzigde pixels van A (magenta)
diff=Image.new('RGBA',(64,64),(0,0,0,0)); oA=outs['A'].load()
base=src.convert('RGBA').copy()
grey=Image.eval(base.convert('L'),lambda v:v//2+100).convert('RGBA'); grey.putalpha(base.split()[3])
d=grey.load()
for y in range(64):
    for x in range(64):
        if a[x,y]!=oA[x,y]: d[x,y]=(255,0,255,255)
V=Image.new('RGB',(528*4,540),G); dr=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(src,'af'),(outs['A'],'A: strikt, min. zwart'),(outs['B'],'B: + zwart (28..29,40) en (40,52)'),(grey,'gewijzigd in A (magenta)')]):
    V.paste(on(im,G,8),(i*528,24)); dr.text((i*528+6,6),t,fill='black')
V.save('vergelijk_8x.png')
S=Image.new('RGB',(3*276+10,2*212),(128,128,128)); dr=ImageDraw.Draw(S)
for r,bg in enumerate([(0,0,0),(255,255,255)]):
    x=10
    for im in (src,outs['A'],outs['B']):
        S.paste(on(im,bg,1),(x,10+r*212)); S.paste(on(im,bg,3),(x+70,10+r*212)); x+=276
S.save('strook_1x.png')

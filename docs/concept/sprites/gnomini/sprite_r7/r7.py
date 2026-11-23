# Gnomini r7 variant C: vanaf ../sprite_r6/gnomini_A.png; lijnen met verloop mee met het licht linksboven:
# belichte kant = middentint (muts 3, huid 7, broek b), naar onder/rechts outline base (2, 6, a), zwart alleen op de diepste punten.
from PIL import Image, ImageDraw
af=Image.open('../af/gnomini.png'); A=Image.open('../sprite_r6/gnomini_A.png'); B=Image.open('../sprite_r6/gnomini_B.png')
a=A.load()
C={
 # mutsrand over de neus: linkerhelft (licht) 3, rechterhelft en verder naar rechts blijft 2
 (21,35):3,(22,35):3,(23,34):3,(24,34):3,
 # neus: linkerkant boven 7, naar onder 6, rechtsonder zwart (diepste punt)
 (20,36):7,(20,37):7,(20,38):7,(28,40):1,(29,40):1,
 # linkerarm: bovenkant en linkerkant boven 7 (naast de bestaande 7 op (17,40),(16,41))
 (18,40):7,(15,42):7,(15,43):7,
 # rechterarm: bovenkant links 7
 (45,41):7,
 # broek linkerkant: boven b, onder a
 (20,47):0xb,(21,48):0xb,
 # linkervoet: bovenkant/linkerkant boven b; binnenlijn voet/been begint met b
 (22,51):0xb,(19,52):0xb,(18,53):0xb,(23,51):0xb,
 # kier boven rechtervoet: zwart (diepste punt)
 (40,52):1,
}
out=A.copy(); o=out.load()
for p,c in C.items(): o[p]=c
assert out.getpalette()==A.getpalette()
assert all((a[x,y]==0)==(o[x,y]==0) for y in range(64) for x in range(64))
op=[(x,y) for y in range(64) for x in range(64) if o[x,y]]
ch=[(x,y) for y in range(64) for x in range(64) if a[x,y]!=o[x,y]]
print('C t.o.v. A: %d gewijzigd; zwart %d (%.1f%%)'%(len(ch),sum(o[p]==1 for p in op),100*sum(o[p]==1 for p in op)/len(op)))
out.save('gnomini_C.png')
G=(152,208,160)
def on(im,bg,k):
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im.convert('RGBA')); return b.resize((64*k,64*k),0).convert('RGB')
V=Image.new('RGB',(528*3,540),G); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(af,'af'),(B,'r6-B'),(out,'C: lijnen met verloop')]):
    V.paste(on(im,G,8),(i*528,24)); d.text((i*528+6,6),t,fill='black')
V.save('vergelijk_8x.png')
S=Image.new('RGB',(3*276+10,2*212),(128,128,128))
for r,bg in enumerate([(0,0,0),(255,255,255)]):
    x=10
    for im in (af,B,out):
        S.paste(on(im,bg,1),(x,10+r*212)); S.paste(on(im,bg,3),(x+70,10+r*212)); x+=276
S.save('strook_1x.png')

# Gnomad r11: binnenlijnen onder neus en snor zonder zwart (A) / met 2 zwarte pixels op het diepste punt (B). Bron: ../sprite_r10/gnomad.png
from PIL import Image, ImageDraw
src=Image.open('../sprite_r10/gnomad.png'); a=src.load()
NEUS={(x,33):6 for x in range(17,23)}          # onder de neus: outline base neus (donkerroze)
SNOR={(x,38):0xe for x in range(13,18)}        # onder de snor: outline base snor (bruin)
A=dict(NEUS); A.update(SNOR)
B=dict(A); B[(22,33)]=1; B[(17,38)]=1         # diepste punten: neushoek schaduwkant, kier snor/arm/lijf
ZONE=set(A)
G=(152,208,160,255)
def on(im,bg,k):
    b=Image.new('RGBA',(64,64),bg); b.alpha_composite(im.convert('RGBA')); return b.resize((64*k,64*k),0).convert('RGB')
outs={}
for n,F in (('A',A),('B',B)):
    im=src.copy(); o=im.load()
    for p,c in F.items(): assert a[p]==1,p; o[p]=c
    ch=[(x,y) for y in range(64) for x in range(64) if a[x,y]!=o[x,y]]
    assert set(ch)<=ZONE and all((a[x,y]==0)==(o[x,y]==0) for y in range(64) for x in range(64))
    op=sum(1 for y in range(64) for x in range(64) if o[x,y]); bl=sum(1 for y in range(64) for x in range(64) if o[x,y]==1)
    print(n,len(ch),'gewijzigd; zwart %d (%.1f%%)'%(bl,100*bl/op))
    im.save('gnomad_%s.png'%n); outs[n]=im
V=Image.new('RGB',(512*3+32,536),G[:3]); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(src,'r10'),(outs['A'],'A: zonder zwart'),(outs['B'],'B: 2 zwarte px (22,33) en (17,38)')]):
    V.paste(on(im,G,8),(i*528,24)); d.text((i*528+6,6),t,fill='black')
V.save('vergelijk_8x.png')
S=Image.new('RGB',(3*(64+192+20)+10,212),(128,128,128)); x=10
for im in (src,outs['A'],outs['B']):
    S.paste(on(im,G,1),(x,10)); S.paste(on(im,G,3),(x+70,10)); x+=276
S.save('strook_1x.png')

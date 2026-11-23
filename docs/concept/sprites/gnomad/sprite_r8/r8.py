# Gnomad r8: zwart verminderen in 4 zones (snor rechtsonder, rechter haarpluk onder, linkerhand/-arm, rechterarm/-hand).
from PIL import Image, ImageDraw
SRC='../af/gnomad.png'
B,M,P6,P7,P8,C,E=1,2,6,7,8,0xc,0xe
ZONES={
 'snor rechtsonder':     [((23,32),P6),((26,32),P6),((27,33),P6),((28,33),P6),((28,34),C),((29,35),P6),
                          ((30,36),P6),((31,36),P6),((32,36),P6),((30,37),C),((32,37),P6),((30,38),C),((31,38),P6),
                          ((26,38),P6),((22,38),C),((21,38),P6),((20,37),P6),((19,36),P6),((18,37),P6)],
 'rechter haarpluk onder':[((35,34),P6),((36,34),P6),((36,35),P6),((38,34),P6),((39,35),P6),((40,35),P6),
                          ((42,33),E),((42,31),C)],
 'linkerhand + -arm':    [((8,39),P6),((13,39),P6),((13,40),P6),((13,41),P6),((10,41),P6),((10,42),P6),((10,43),P6),((4,45),P6)],
 'rechterarm + -hand':   [((39,40),P6),((40,40),P6),((41,40),P6),((42,39),P6),((43,39),P6),((44,39),P6),((46,40),P6),((42,45),P6)],
}
BOX={'snor rechtsonder':(18,32,33,38),'rechter haarpluk onder':(34,31,44,35),
     'linkerhand + -arm':(4,38,13,47),'rechterarm + -hand':(30,34,49,47)}
BELT=set((x,y) for x in range(26,41) for y in range(41,49))  # riem+gesp (bevroren); armpixels erbuiten
def inbox(b,x,y): return b[0]<=x<=b[2] and b[1]<=y<=b[3]
im=Image.open(SRC); a=im.load(); out=im.copy(); o=out.load()
for z,ch in ZONES.items():
    for (x,y),c in ch:
        assert a[x,y]==B, (z,x,y,a[x,y]); assert inbox(BOX[z],x,y); assert (x,y) not in BELT or y<42 and x>40, (x,y)
        o[x,y]=c
out.save('gnomad.png')
# bewijs: diff 0 buiten de zones, alleen zwarte pixels gewijzigd
ch=[(x,y) for y in range(64) for x in range(64) if a[x,y]!=o[x,y]]
assert all(any(inbox(b,x,y) for b in BOX.values()) for x,y in ch)
assert all(a[x,y]==B for x,y in ch)
assert all(a[x,y]==o[x,y] for x,y in BELT if not (y==41 and x>40))
op=[(x,y) for y in range(64) for x in range(64) if a[x,y]!=0]
assert op==[(x,y) for y in range(64) for x in range(64) if o[x,y]!=0]  # silhouet gelijk
rep=[]
tot=len(op); b0=sum(a[p]==B for p in op); b1=sum(o[p]==B for p in op)
for z,bx in BOX.items():
    n0=sum(a[x,y]==B for x in range(bx[0],bx[2]+1) for y in range(bx[1],bx[3]+1) if (x,y) not in BELT)
    n1=sum(o[x,y]==B for x in range(bx[0],bx[2]+1) for y in range(bx[1],bx[3]+1) if (x,y) not in BELT)
    rep.append((z,bx,n0,n1,len(ZONES[z])))
print('gewijzigd',len(ch),'pixels; buiten zones 0; alle van zwart; silhouet gelijk; riem/gesp 0')
for r in rep: print(r)
print('zwart totaal %d/%d = %.1f%% -> %d/%d = %.1f%%'%(b0,tot,100*b0/tot,b1,tot,100*b1/tot))
# afbeeldingen
k=8
out.convert('RGB').resize((512,512),0).save('gnomad_8x.png')
A=im.convert('RGB').resize((512,512),0); R=out.convert('RGB').resize((512,512),0)
D=out.convert('RGB').resize((512,512),0); d=ImageDraw.Draw(D)
for x,y in ch: d.rectangle([x*k,y*k,x*k+k-1,y*k+k-1],outline=(0,255,255),width=2)
V=Image.new('RGB',(512*3+32,512),'white'); V.paste(A,(0,0)); V.paste(R,(528,0)); V.paste(D,(1056,0)); V.save('vergelijk_8x.png')

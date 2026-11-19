"""Werkvel: OW-frames 0/2/4 uitvergroot (16x) met rooster en absolute coordinaten.
python3 rooster_ow.py uit.png soort"""
import sys,numpy as np
from PIL import Image,ImageDraw
from laad_ow import frame,pal,rgba
def blok(a,Z):
    W=H=32; M=22
    img=Image.new('RGB',(W*Z+M,H*Z+M),(255,255,255)); bg=Image.new('RGB',(W*Z,H*Z),(150,210,180))
    im=Image.fromarray(a).resize((W*Z,H*Z),Image.NEAREST); bg.paste(im,(0,0),im); img.paste(bg,(M,M)); d=ImageDraw.Draw(img)
    for i in range(W+1):
        X=M+i*Z; d.line([(X,M),(X,M+H*Z)],fill=(0,0,0) if i%2==0 else (110,110,110),width=2 if i%10==0 else 1)
        if i%2==0 and i<32: d.text((X+3,6),str(i),fill=(200,0,0))
    for j in range(H+1):
        Y=M+j*Z; d.line([(M,Y),(M+W*Z,Y)],fill=(0,0,0) if j%2==0 else (110,110,110),width=2 if j%10==0 else 1)
        if j%2==0 and j<32: d.text((2,Y+3),str(j),fill=(200,0,0))
    return img
if __name__=='__main__':
    sp=sys.argv[2]; P=pal(sp); Z=int(sys.argv[3]) if len(sys.argv)>3 else 14
    B=[blok(rgba(frame(sp,k),P),Z) for k in (0,2,4)]
    img=Image.new('RGB',(sum(b.width for b in B)+40,B[0].height),(255,255,255)); x=0
    for b in B: img.paste(b,(x,0)); x+=b.width+20
    img.save(sys.argv[1])
def detail(sp,k,Z=26):
    """frame k bijgesneden, Z-voudig, met index per pixel en coordinaten"""
    ix=frame(sp,k); P=pal(sp); a=rgba(ix,P)
    ys,xs=np.nonzero(ix); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
    c=a[y0:y1,x0:x1]; H,W=c.shape[:2]; M=24
    img=Image.new('RGB',(W*Z+M,H*Z+M),(255,255,255)); bg=Image.new('RGB',(W*Z,H*Z),(150,210,180))
    im=Image.fromarray(c).resize((W*Z,H*Z),Image.NEAREST); bg.paste(im,(0,0),im); img.paste(bg,(M,M)); d=ImageDraw.Draw(img)
    for i in range(W+1): d.line([(M+i*Z,M),(M+i*Z,M+H*Z)],fill=(90,90,90))
    for j in range(H+1): d.line([(M,M+j*Z),(M+W*Z,M+j*Z)],fill=(90,90,90))
    for i in range(W): d.text((M+i*Z+6,6),str(x0+i),fill=(200,0,0))
    for j in range(H): d.text((2,M+j*Z+8),str(y0+j),fill=(200,0,0))
    for j in range(H):
        for i in range(W):
            v=ix[y0+j,x0+i]
            if v: L=sum(P[v]); d.text((M+i*Z+9,M+j*Z+8),'%x'%v,fill=(255,255,255) if L<380 else (0,0,0))
    return img

# r16: linker rupsband horizontaal indrukken (factor F, verankerd rechts op XR) en het witte uiteinde omkleuren naar het rechter uiteinde.
# Gebruik: python3 rups_kort.py F [XR YTOP]
import sys; from PIL import Image; import numpy as np
F=float(sys.argv[1]); XR=int(sys.argv[2]) if len(sys.argv)>2 else 520; YT=int(sys.argv[3]) if len(sys.argv)>3 else 694; XL=140
im=Image.open('gemini/r16_P4.png').convert('RGB'); a=np.asarray(im).copy(); bg=tuple(int(v) for v in a[5,5])
H=a.shape[0]
blk=im.crop((XL,YT,XR,H)); nw=round((XR-XL)*F)
blk=blk.resize((nw,H-YT),Image.NEAREST)
o=im.copy(); o.paste(bg,(XL,YT,XR,H)); o.paste(blk,(XR-nw,YT))
o=np.asarray(o).copy()
# tentakel die boven de rupsband doorloopt tot onder YT terugzetten
for x in range(XL,XR-nw):
    y=YT; run=[]
    while y<YT+24 and a[y,x].min()<235 and int(a[y,x][1])<120 and int(a[YT-1,x][1])<120 and a[YT-1,x].min()<235:
        run.append(y); y+=1
    if len(run)>=6:
        for y in run: o[y,x]=a[y,x]
x0,x1=XR-nw,XR-nw+round(200*F)
reg=o[YT:,x0:x1].astype(int); r,g,b=reg[...,0],reg[...,1],reg[...,2]
isbg=(r>250)&(g>250)&(b>250)
white=(r>200)&(g>190)&(b>165)&~isbg
pinkl=(r>185)&(g>130)&(g<=200)&~white&~isbg
reg[white]=(168,62,80); reg[pinkl]=(214,140,150)
# donkere omlijning waar het uiteinde aan de achtergrond grenst (blokdikte 7 px)
nb=np.zeros_like(isbg)
for dy in range(-7,8):
    for dx in range(-7,8):
        nb|=np.roll(np.roll(isbg,dy,0),dx,1)
edge=nb&~isbg&(white|pinkl|((r>120)&(g>60)))
reg[edge]=(34,10,16)
o[YT:,x0:x1]=reg.astype('uint8')
Image.fromarray(o).save('samenvoeg/r16_kort.png')
Image.fromarray(o).crop((120,600,900,860)).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/edb145cf-71a4-55a5-8012-167050278397/scratchpad/k16.png')

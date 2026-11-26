"""Variant: pointer valt een paar bytes NAAST een echte LZ77-frontsprite in de ROM.
De BIOS leest dan midden in de stroom: echte spritepatronen door elkaar, met de
doorzichtigheid van echte sprites (dus een onregelmatige omtrek). Palet: index 0 (?).
Gebruik: python3 gen3_missingno_scheef.py ROM UITMAP [aantal]"""
import sys, os, random, re
from PIL import Image, ImageDraw
sys.path.insert(0,os.path.dirname(__file__))
from gen3_missingno import lz77, render, pal_none
rom=open(sys.argv[1],'rb').read(); uit=sys.argv[2]; aantal=int(sys.argv[3]) if len(sys.argv)>3 else 40
os.makedirs(uit,exist_ok=True); pal=pal_none()
heads=[m.start() for m in re.finditer(rb'\x10\x00(\x08|\x10)\x00',rom) if m.start()%4==0]
r=random.Random(3); r.shuffle(heads); kand=[]
for h in heads:
    for off in r.sample(range(1,48),3):
        buf,size=lz77(rom,h+off); im=render(buf,pal)
        a=sum(1 for p in im.getdata() if p[3])/4096
        if 0.1<a<0.55: kand.append((h,off,a,im))
    if len(kand)>=aantal*3: break
r.shuffle(kand); kand=kand[:aantal]
cols=8; rows=(len(kand)+cols-1)//cols
sh=Image.new('RGB',(cols*76,rows*84),(255,255,255)); d=ImageDraw.Draw(sh)
with open(f'{uit}/kandidaten.txt','w') as fh:
    for i,(h,off,a,im) in enumerate(kand):
        x,y=(i%cols)*76+6,(i//cols)*84+4; sh.paste(im,(x,y),im); d.text((x,y+66),str(i+1),fill=(200,0,0))
        im.save(f'{uit}/k{i+1:02d}.png'); fh.write(f'{i+1}\tsprite@0x{h:X}\t+{off}\tvulling={a:.2f}\n')
sh.resize((sh.size[0]*2,sh.size[1]*2),Image.NEAREST).save(f'{uit}/vel.png'); print(len(heads),len(kand))

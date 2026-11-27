# Vel r9: r9 1x op wit en donker, r9 8x, r8 8x, diff-overlay (gewijzigde pixels rood omkaderd op r9 8x).
import numpy as np, os
from PIL import Image, ImageDraw
HIER=os.path.dirname(os.path.abspath(__file__))
r9=Image.open(HIER+'/kuiken_r9.png'); r8=Image.open(HIER+'/../r8/kuiken_r8.png')
d=np.argwhere(np.array(r9)!=np.array(r8))
def op(im,bg,k=1):
    b=Image.new('RGBA',(64,64),bg); b.alpha_composite(im.convert('RGBA')); return b.resize((64*k,64*k),Image.NEAREST)
K=8; W=64*K; vel=Image.new('RGB',(64*2+16+W*3+48,W+40),(255,255,255)); dr=ImageDraw.Draw(vel)
vel.paste(op(r9,(255,255,255,255)),(8,30)); vel.paste(op(r9,(40,40,48,255)),(8,30+72))
x0=64+16+16
for i,(im,t) in enumerate(((r9,'r9 8x'),(r8,'r8 8x'),(r9,'diff r8->r9 (%d px)'%len(d)))):
    p=op(im,(255,255,255,255),K)
    if i==2:
        g=Image.new('RGBA',p.size,(255,255,255,140)); p=p.convert('RGBA'); p.alpha_composite(g); pd=ImageDraw.Draw(p)
        for y,x in d: pd.rectangle([x*K,y*K,x*K+K-1,y*K+K-1],outline=(230,0,0),width=2)
        p=p.convert('RGB')
    vel.paste(p,(x0+i*(W+16),30)); dr.text((x0+i*(W+16),10),t,fill=(0,0,0))
dr.text((8,10),'r9 1x',fill=(0,0,0))
vel.save(HIER+'/vel.png')

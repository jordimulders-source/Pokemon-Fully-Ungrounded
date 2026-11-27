# Vel ek1: ek1 | r3 | model op 8x; daaronder ek1, spearow, taillow op 1x en 4x op licht en donker
import numpy as np; from PIL import Image, ImageDraw
G='../../../../../../graphics/pokemon/'
def gba(n):
    im=Image.open(G+n+'/anim_front_gba.png').convert('P'); pal=[int(v) for v in open(G+n+'/normal_gba.pal').read().split()[3:]]
    im.putpalette(pal); a=np.array(im); A=np.array(im.convert('RGBA')); A[...,3]=np.where(a==0,0,255); return Image.fromarray(A).crop((0,0,64,64))
def op(im,bg,k):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.resize((im.width*k,im.height*k),Image.NEAREST)
ek=Image.open('kuiken_ek1.png').convert('RGBA'); r3=Image.open('../sprite_r3/kuiken_r3_M_i_a.png').convert('RGBA')
m=Image.open('../gemini/model_kandidaat.png').convert('RGBA').resize((512,512),Image.LANCZOS)
sp=gba('spearow'); ta=gba('taillow')
LI,DO=(240,240,232),(48,52,60)
W=Image.new('RGBA',(1576,24+512+20+64+20+256+10),(255,255,255,255)); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(op(ek,(255,255,255),8),'ek1'),(op(r3,(255,255,255),8),'r3 (gekozen)'),(m,'model')]):
    W.paste(im,(i*532,24)); d.text((i*532+4,6),t,fill=(0,0,0))
y=24+512+20; x=10
for bg in (LI,DO):
    for im in (ek,sp,ta): W.paste(op(im,bg,1),(x,y)); x+=68
    x+=20
d.text((x+10,y+24),'1x: ek1, spearow, taillow (licht | donker)',fill=(0,0,0))
y+=84; x=10
for bg in (LI,DO):
    for im in (ek,sp,ta): W.paste(op(im,bg,4),(x,y)); x+=260
W.save('vel.png'); op(ek,(255,255,255),8).save('kuiken_ek1_8x.png')

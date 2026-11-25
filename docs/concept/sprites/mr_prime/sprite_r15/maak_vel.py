import numpy as np; from PIL import Image, ImageDraw
LICHT=(220,220,220); DONKER=(40,44,52)
def sp(p,bg=LICHT):
    o=Image.open(p); o.info['transparency']=0; s=o.convert('RGBA'); b=Image.new('RGBA',s.size,bg+(255,)); b.alpha_composite(s); return b.convert('RGB')
def label(im,t):
    W=Image.new('RGB',(im.width,im.height+22),(255,255,255)); W.paste(im,(0,22)); ImageDraw.Draw(W).text((4,5),t,fill=(0,0,0)); return W
box=(26,0,64,26); z=12
kop=[label(sp(p).crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),0),t) for p,t in
     [('variant_A.png','A: Rime-zijhaar achter de kop (gekozen)'),('variant_B2.png','B: hoed+vleugels 1 links, 1 omlaag'),('../sprite_r14/mr_prime.png','r14')]]
rime=sp('../../../../../graphics/pokemon/mr_rime/front.png').crop((19,3,57,29)); kop.append(label(rime.resize((rime.width*z,rime.height*z),0),'Mr. Rime front.png (zelfde uitsnede t.o.v. de hoed)'))
s=[]
for bg in (LICHT,DONKER):
    a=sp('mr_prime.png',bg); s+=[a,a.resize((128,128),0)]
strip=Image.new('RGB',(64*2+128*2+50,150),(255,255,255)); x=10
for im in s: strip.paste(im,(x,10)); x+=im.width+10
rows=[kop,[label(strip,'r15 (A) 1x / 2x licht en donker')]]
W=max(sum(i.width for i in r)+20*(len(r)-1) for r in rows)+20; H=sum(max(i.height for i in r) for r in rows)+20*len(rows)+10
V=Image.new('RGB',(W,H),(255,255,255)); y=10
for r in rows:
    x=10
    for im in r: V.paste(im,(x,y)); x+=im.width+20
    y+=max(i.height for i in r)+20
V.save('vel.png'); sp('mr_prime.png').resize((512,512),0).save('mr_prime_8x.png')

from PIL import Image, ImageDraw
S=8
s=Image.open('staryu/sprite_r1/staryu_r1.png').convert('RGB')
m=Image.open('gemini/r3_staryu.png').convert('RGB').crop((143,122,902,902))
M=Image.new('RGB',(64,64),(255,255,255))
mm=Image.new('RGB',(64*S,64*S),(255,255,255)); mm.paste(m.resize((41*S,43*S),Image.LANCZOS),(11*S,12*S))
im=Image.open('../../../../graphics/pokemon/staryu/anim_front_gba.png').crop((0,0,64,64))
p=[]
for l in open('../../../../graphics/pokemon/staryu/normal_gba.pal').read().split('\n')[3:19]: p+=[int(v) for v in l.split()]
im.putpalette(p); g3=im.convert('RGB')
W=Image.new('RGB',(64*S*3+40,64*S+150),(255,255,255))
W.paste(s.resize((64*S,64*S),0),(0,0)); W.paste(mm,(64*S+20,0)); W.paste(g3.resize((64*S,64*S),0),(2*64*S+40,0))
d=ImageDraw.Draw(W)
punten={1:[(11,29),(12,30)],2:[(24,32),(24,33)],3:[(20,36),(29,46)],4:[(29,15),(29,16),(30,13),(31,13),(31,14)],5:[(26,35)]}
kl={1:(255,0,255),2:(0,90,255),3:(0,170,0),4:(255,140,0),5:(120,120,120)}
for n,pts in punten.items():
    for off in (0,64*S+20):
        for x,y in pts: d.rectangle((off+x*S,y*S,off+x*S+S-1,y*S+S-1),outline=kl[n],width=2)
        x,y=pts[0]; d.text((off+x*S-14,y*S-4),str(n),fill=kl[n])
# 1x
for i,bg in enumerate([(255,255,255),(248,240,216),(40,40,48)]):
    t=Image.new('RGB',(64,64),bg); a=Image.open('staryu/sprite_r1/staryu_r1.png').convert('RGBA')
    import numpy as np
    A=np.array(Image.open('staryu/sprite_r1/staryu_r1.png')); al=Image.fromarray(((A!=0)*255).astype('uint8'))
    t.paste(s,(0,0),al); W.paste(t,(10+i*80,64*S+20))
W.paste(m.resize((41,43),Image.BOX),(260,64*S+30)); W.paste(g3,(330,64*S+20))
d.text((10,64*S+100),'1 lijn-tip (om en om)  2 chip raakt juweel  3 chipbruin als barst  4 bovenarm licht/schaduw  5 juweelring (optioneel)',fill=(0,0,0))
d.text((10,64*S+5),'sprite r1 8x | model zelfde schaal | Gen 3 Staryu 8x',fill=(0,0,0))
W.save('staryu/keuring_r1/vel.png')

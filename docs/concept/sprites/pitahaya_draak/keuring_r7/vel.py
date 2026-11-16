# vel.png: r7 | sim MOET | model op 8x met gemarkeerde punten; daaronder r6 | r7 | sim op 1x en 2x (licht en donker)
import numpy as np; from PIL import Image, ImageDraw
def rgb(f,bg):
    a=Image.open(f); i=np.array(a); r=np.array(a.convert('RGB')); r[i==0]=bg; return Image.fromarray(r)
nat=Image.open('../sprite_r7/natief.png').convert('RGB')
model=nat.crop((4,6,196,198)).resize((512,512),Image.NEAREST)
Z=8; L=(205,212,222); D=(40,44,56)
pan=[rgb('../sprite_r7/pitahaya_r7.png',L),rgb('sim_moet_sprite.png',L)]
MARK={1:[(37,37),(38,38)],2:[(42,37)],3:[(35,53),(36,53),(38,53),(39,53)],4:[(35,54)]}
W=Image.new('RGB',(3*512+40,512+160),(255,255,255)); d=ImageDraw.Draw(W)
for k,p in enumerate(pan+[model]):
    W.paste(p if k==2 else p.resize((512,512),Image.NEAREST),(k*532,0))
    for n,pts in MARK.items():
        for x,y in pts: d.rectangle([k*532+x*Z,y*Z,k*532+x*Z+Z-1,y*Z+Z-1],outline=(255,0,0) if k<2 else (0,120,255))
        x,y=pts[0]; d.text((k*532+x*Z-12,y*Z-2),str(n),fill=(255,0,0))
for k,t in enumerate(['r7','sim MOET','model (natief, zelfde uitsnede)']): d.text((k*532+4,500),t,fill=(0,0,0))
x0=0
for j,f in enumerate(['../sprite_r7/pitahaya_r6.png','../sprite_r7/pitahaya_r7.png','sim_moet_sprite.png']):
    W.paste(rgb(f,L),(x0,520)); W.paste(rgb(f,D),(x0,590)); W.paste(rgb(f,L).resize((128,128),Image.NEAREST),(x0+70,520)); W.paste(rgb(f,D).resize((128,128),Image.NEAREST),(x0+205,520))
    d.text((x0,650),['r6','r7','sim'][j],fill=(0,0,0)); x0+=350
W.save('vel.png')

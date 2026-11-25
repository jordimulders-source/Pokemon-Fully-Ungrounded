# Regionale Jynx r5 = eindkeuring (schaduw, kleurtinten, lijnen) op r4 variant B (Jordi koos B: "rechts beter").
# Uitkomst van de keuring: geen pixel aantoonbaar beter te maken binnen "alleen uitvoering" (zie EINDKEURING.md),
# dus r5 = r4 B, 0 px gewijzigd. Dit script bewijst dat en maakt de 8x-versie en het vel.
# Bouwen: cd docs/concept/sprites/jynx_regional && python3 sprite_r5/bouw.py
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
BRON='sprite_r4/jynx_regional_r4_B_zonder_lijn.png'; R4='sprite_r4/jynx_regional_r4.png'; UIT='sprite_r5/jynx_regional_r5.png'
src=Image.open(BRON); b=np.asarray(src).astype(int); o=b.copy()
WIJZIGINGEN=[]          # (x, y, nieuwe index): bewust leeg, zie EINDKEURING.md
for X,Y,k in WIJZIGINGEN: o[Y,X]=k
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(src.getpalette()); p.save(UIT,transparency=0)
q=Image.open(UIT); oq=np.asarray(q).astype(int)
assert q.mode=='P' and q.info.get('transparency')==0 and q.size==(64,64)
assert ((oq>0)==(b>0)).all(), 'silhouet gewijzigd'
assert len(set(oq.ravel()))<=16
print(UIT,'| anders dan r4 B: %d px | silhouet-diff 0 | kleuren %d'%((oq!=b).sum(),len(set(oq.ravel()))))
def rgb_from(path,bg=(255,255,255)):
    im=Image.open(path).convert('RGBA').crop((0,0,64,64)); c=Image.new('RGBA',(64,64),bg+(255,)); c.alpha_composite(im); return c.convert('RGB')
def gba(n,bg):
    im=Image.open(f'../../../../graphics/pokemon/{n}/anim_front_gba.png').crop((0,0,64,64))
    pal=[int(v) for l in open(f'../../../../graphics/pokemon/{n}/normal_gba.pal').read().split('\n')[3:19] for v in l.split()]
    a=np.asarray(im); img=np.zeros((64,64,3),'uint8'); img[:]=bg; P=np.array(pal).reshape(-1,3)
    for k in range(1,16): img[a==k]=P[k]
    return Image.fromarray(img)
s5,s4=rgb_from(UIT),rgb_from(R4); m=model_op_schaal()
s5.resize((512,512),Image.NEAREST).save('sprite_r5/jynx_regional_r5_8x.png')
M=Image.open(MODEL).convert('RGB')
def mcrop(x0,y0,x1,y1,z):
    u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
    f=lambda u,ph:ph+0.5+10.24*u
    return M.crop((int(f(u0,9.25)),int(f(v0,9.20)),int(f(u1,9.25)),int(f(v1,9.20)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
z=12; rows=[]
for n,x0,y0,x1,y1 in [('gezicht + haar',10,5,48,36),('rok',5,34,56,63),('vleugel rechts',38,6,60,31)]:
    ps=[s5.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),mcrop(x0,y0,x1,y1,z)]
    r=Image.new('RGB',(sum(p.width+8 for p in ps),ps[0].height+18),'white'); d=ImageDraw.Draw(r); d.text((2,2),n+'  (r5 | model)',fill=(0,0,0)); x=0
    for p in ps: r.paste(p,(x,18)); x+=p.width+8
    rows.append(r)
top=[s5.resize((512,512),Image.NEAREST),s4.resize((512,512),Image.NEAREST),m.resize((512,512),Image.NEAREST)]
W=max(1560,max(r.width for r in rows)); H=530+sum(r.height+8 for r in rows)+300
v=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(v)
for i,pp in enumerate(top): v.paste(pp,(i*520,0)); d.text((i*520+4,514),['r5 (= r4 B)','r4 (met rokvouwlijn)','model op schaal'][i],fill=(0,0,0))
y=530
for r in rows: v.paste(r,(0,y)); y+=r.height+8
d.text((4,y),'1x en 2x: r5 | Skinguin | Dundragoon | Jynx (Gen 3 gba)  op licht en donker',fill=(0,0,0)); y+=16
x=0
for bg in [(255,255,255),(40,48,56)]:
    for qq in [rgb_from(UIT,bg),rgb_from('../skinguin/af/skinguin.png',bg),rgb_from('../dundragoon/af/dundragoon.png',bg),gba('jynx',bg)]: v.paste(qq,(x,y)); x+=68
    x+=12
y+=72; x=0
for bg in [(255,255,255),(40,48,56)]:
    for qq in [rgb_from(UIT,bg),rgb_from('../skinguin/af/skinguin.png',bg),rgb_from('../dundragoon/af/dundragoon.png',bg),gba('jynx',bg)]: v.paste(qq.resize((128,128),Image.NEAREST),(x,y)); x+=136
v=v.crop((0,0,W,y+136)); v.save('sprite_r5/vel.png'); print('vel',v.size)

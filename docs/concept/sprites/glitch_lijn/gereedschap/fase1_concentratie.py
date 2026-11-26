"""Fase 1 na Jordi: Gengar start +13 als basis; dichtheid hoger, middenstuk geconcentreerd,
rest "sparkt" eromheen. Dichter: tweede uitlezing (ander startadres) vult de gaten van de eerste,
alsof twee frames over elkaar in de buffer zijn geschreven. Concentratie: kans om een pixel te
houden daalt met de afstand tot het midden; buiten de kern alleen losse vonkjes (1-2 px).
Gebruik: python3 fase1_concentratie.py UITMAP"""
import sys, os, random, math
from PIL import Image, ImageDraw
sys.path.insert(0,os.path.dirname(__file__))
from gen3_missingno import pal_none, REPO
from gen3_afmeting import tiles4bpp, lees
uit=sys.argv[1]; os.makedirs(uit,exist_ok=True)
data,eig=tiles4bpp(os.path.join(REPO,'graphics/pokemon/gengar/anim_front_gba.png'))
pn=pal_none()
def maak(pal,tweede,kern,rand,seed,vul=0.5):
    a=lees(data,pal,8,13); b=lees(data,pal,8,tweede) if tweede is not None else None
    r=random.Random(seed); out=Image.new('RGBA',(64,64),(0,0,0,0)); pa,po=a.load(),out.load()
    pb=b.load() if b else None
    cx,cy=32,34
    for y in range(64):
        for x in range(64):
            p=pa[x,y]
            if p[3]==0 and pb and r.random()<vul: p=pb[x,y]
            if p[3]==0: continue
            ang=math.atan2(y-cy,x-cx); k2=kern*(1+0.35*math.sin(3*ang+seed)+0.2*math.sin(5*ang+2*seed))
            d=math.hypot(x-cx,y-cy)
            keep=1.0 if d<k2 else max(0.0,1-(d-k2)/rand)*0.35
            if r.random()<keep: po[x,y]=p
    return out
vars=[(None,18,14),(29,18,14),(29,22,12),(45,16,16),(45,20,10),(77,20,14)]
sh=Image.new('RGB',(len(vars)*72+8,2*72+8),(255,255,255))
for j,(t,k,rd) in enumerate(vars):
    for q,pal in enumerate((eig,pn)):
        im=maak(pal,t,k,rd,j); sh.paste(im,(8+j*72,8+q*72),im)
        im.save(f'{uit}/c{j+1}_{"eigen" if q==0 else "vraag"}.png')
sh.resize((sh.size[0]*3,sh.size[1]*3),Image.NEAREST).save(f'{uit}/vel.png')

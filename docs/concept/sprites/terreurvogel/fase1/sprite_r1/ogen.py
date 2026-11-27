# Oogvarianten op r1_basis: oog 1-op-1 uit een Gen 3-sprite, omgekleurd (K->zwart, wit->oog geel, ring->bruin donker), glans = oog wit (14)
import numpy as np; from PIL import Image, ImageDraw
from lib import *
K=np.load('kaal.npy'); BASIS=np.load('r1_basis.npy'); ALPHA=K>0
def bron(soort): return np.array(Image.open('../../../../../../graphics/pokemon/%s/anim_front_gba.png'%soort))[:64]
OGEN={ # naam: (soort, bronpixels, kleurmap bronindex -> onze index, verschuiving, glans)
 'A':('spearow',[(25,22),(26,22),(22,23),(23,23),(24,23),(25,23),(26,23),(23,24),(24,24),(25,24),(26,24),(24,25),(25,25)],{15:1,1:15,9:5},(5,4),None),
 'B':('spearow',[(25,22),(26,22),(22,23),(23,23),(24,23),(25,23),(26,23),(23,24),(24,24),(25,24),(26,24),(24,25),(25,25)],{15:1,1:15,9:5},(5,4),(29,28)),
 'C':('pidgeot',[(13,23),(14,23),(15,23),(12,24),(13,24),(14,24),(15,24),(11,25),(12,25),(13,25),(14,25),(15,25),(11,26),(12,26),(13,26),(14,26),(15,26),(11,27),(12,27),(13,27)],{15:1,14:5,1:15,2:15},(17,2),None),
 'D':('pidgeot',[(13,23),(14,23),(15,23),(12,24),(13,24),(14,24),(15,24),(11,25),(12,25),(13,25),(14,25),(15,25),(11,26),(12,26),(13,26),(14,26),(15,26),(11,27),(12,27),(13,27)],{15:1,14:5,1:15,2:15},(17,2),(29,28)),
}
# E: geen bronsprite; modeloog als ronde vorm (dikdik-methode, GEMINI.md): ring native x44-49,y31-36 -> sprite x28-32,y25-29; pupil 1x2, glans linksonder
E=['.KKK.','KYYYK','KYKYK','KWKYK','.KKK.']
OUD=[(x,y) for y in range(25,30) for x in range(28,33) if K[y,x] in (1,15) or BASIS[y,x] in (1,15)]
def maak(naam):
    S=BASIS.copy()
    if naam=='E':
        NIEUW={(28+i,25+j):{'K':1,'Y':15,'W':14}[c] for j,r in enumerate(E) for i,c in enumerate(r) if c!='.'}; gl=None
    else:
        soort,px,cm,(dx,dy),gl=OGEN[naam]; a=bron(soort)
        NIEUW={(x+dx,y+dy):cm[int(a[y,x])] for (x,y) in px}
    for (x,y) in OUD:
        if (x,y) in NIEUW: continue
        tel={}
        for ddy in (-1,0,1):
            for ddx in (-1,0,1):
                q=(x+ddx,y+ddy)
                if q in OUD or q in NIEUW: continue
                v=S[y+ddy,x+ddx]
                if v>1: tel[v]=tel.get(v,0)+1
        S[y,x]=max(tel,key=tel.get) if tel else 6
    for (x,y),v in NIEUW.items(): S[y,x]=v
    if gl: S[gl[1],gl[0]]=14
    assert ((S>0)==ALPHA).all()
    return S
if __name__=='__main__':
    from modelover import modelbeeld
    k=16; box=(24,22,37,32)
    vel=Image.new('RGBA',(6*(13*k+10),10*k+30+80),(255,255,255,255)); d=ImageDraw.Draw(vel)
    for i,n in enumerate('ABCDE'):
        S=maak(n); opslaan(S,'oog_%s.png'%n)
        im=rgba(S,k=k); bg=Image.new('RGBA',im.size,(236,236,236,255)); bg.alpha_composite(im)
        s1=rgba(S); b1=Image.new('RGBA',(64,64),(236,236,236,255)); b1.alpha_composite(s1); vel.paste(b1.crop((8,10,52,50)),(i*(13*k+10),10*k+34))
        vel.paste(bg.crop((box[0]*k,box[1]*k,box[2]*k,box[3]*k)),(i*(13*k+10),24)); d.text((i*(13*k+10),4),'oog_%s'%n+('' if n=='E' else ' (%s%s)'%(OGEN[n][0],' + glans' if OGEN[n][4] else '')),fill=(0,0,0))
    m=modelbeeld(k).convert('RGBA'); vel.paste(m.crop((box[0]*k,box[1]*k,box[2]*k,box[3]*k)),(5*(13*k+10),24)); d.text((5*(13*k+10),4),'model',fill=(0,0,0))
    vel.save('vel_ogen.png')

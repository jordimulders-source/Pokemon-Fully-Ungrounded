# vel.png: vier varianten 8x naast het (gespiegelde, geschrapte) model op dezelfde schaal; kop en buik 12x; 1x licht/donker;
# 4x naast de regionale Poliwhirl (af), Poliwrath (gba) en Dundragoon (af).
import numpy as np; from PIL import Image, ImageDraw
from palet import PAL
V=['O1S1','O1S2','O2S1','O2S2']; R={v:np.load('r1_%s.npy'%v) for v in V}; H,W=R[V[0]].shape
z=np.load('geschrapt.npz'); MOD=z['N'].astype('uint8').copy(); MOD[z['air']]=255
def rgb(a,bg=(255,255,255)):
    o=np.zeros(a.shape+(3,),'uint8'); o[:]=bg
    for k in range(1,16): o[a==k]=PAL[k]
    return Image.fromarray(o)
def gba(n):
    a=np.array(Image.open('../../../../../graphics/pokemon/%s/anim_front_gba.png'%n))[:64]
    p=open('../../../../../graphics/pokemon/%s/normal_gba.pal'%n).read().split()[3:]
    cols=[tuple(map(int,p[i*3:i*3+3])) for i in range(16)]
    o=np.zeros((64,64,3),'uint8'); o[:]=255
    for k in range(1,16): o[a==k]=cols[k]
    return Image.fromarray(o)
def png(p,bg=(255,255,255)):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
def rij(ims,gap=16):
    c=Image.new('RGB',(sum(i.size[0]+gap for i in ims),max(i.size[1] for i in ims)),'white'); x=0
    for i in ims: c.paste(i,(x,0)); x+=i.size[0]+gap
    return c
def big(a,s): return a.resize((a.size[0]*s,a.size[1]*s),Image.NEAREST)
rows=[]
rows.append(('8x: O1S1 | O1S2 | model (gespiegeld, geschrapt; zelfde schaal)',rij([big(rgb(R[v]),8) for v in V[:2]]+[big(Image.fromarray(MOD),8)])))
rows.append(('8x: O2S1 | O2S2 | model',rij([big(rgb(R[v]),8) for v in V[2:]]+[big(Image.fromarray(MOD),8)])))
def close(c0,c1,r0,r1,s=12):
    return rij([big(rgb(R[v][r0:r1+1,c0:c1+1]),s) for v in V]+[big(Image.fromarray(MOD[r0:r1+1,c0:c1+1]),s)])
rows.append(('kop 12x: O1S1 | O1S2 | O2S1 | O2S2 | model',close(12,46,0,18)))
rows.append(('buik 12x: O1S1 | O1S2 | O2S1 | O2S2 | model',close(18,42,22,40)))
one=[]
for v in V:
    S=np.array(Image.open('poliwrath_regional_r1_%s.png'%v))
    one.append(rij([rgb(S,bg) for bg in [(255,255,255),(232,232,216),(48,48,64),(20,20,28)]],8))
rows.append(('1x licht/donker: O1S1 | O1S2 | O2S1 | O2S2',rij(one,30)))
ref=[big(rgb(np.array(Image.open('poliwrath_regional_r1_%s.png'%v))),4) for v in ('O2S2','O1S1')]
ref+=[big(png('../../poliwhirl_regional/af/poliwhirl_regional.png'),4),big(gba('poliwrath'),4),big(png('../../dundragoon/af/dundragoon.png'),4)]
rows.append(('4x (64x64): O2S2 | O1S1 | regionale Poliwhirl (af) | Poliwrath (gba) | Dundragoon (af)',rij(ref)))
Wt=max(im.size[0] for _,im in rows); Ht=sum(im.size[1]+30 for _,im in rows)
vel=Image.new('RGB',(Wt,Ht),'white'); d=ImageDraw.Draw(vel); y=0
for t,im in rows:
    d.text((4,y+8),t,fill=(0,0,0)); vel.paste(im,(0,y+26)); y+=im.size[1]+30
vel.save('vel.png'); print(vel.size)
# los kijkvel voor de maker
rij([big(rgb(R[v]),6) for v in V]).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/69f8bd02-12fa-5158-8b3d-050571a7a83d/scratchpad/v4.png')

"""vel_vergelijk.png: front (4x) | icoon frame 1 (8x) | onze drie aanzichten (8x), en daaronder
drie echte overworldsprites (rattata, eevee, sentret; voor/achter/opzij 8x) als maatstaf. Ook alles op 1x rechtsboven."""
import sys,os,numpy as np
from PIL import Image,ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H); from ow_pal import *
R=os.path.abspath(os.path.join(H,'../../../../../..')); V=R+'/docs/concept/sprites/viscacha/'
BG=(152,208,160)
def pal(p): return [tuple(int(v) for v in l.split()[:3]) for l in open(p).read().split('\n')[3:19]]
def img(a,P,z): return rgba(a,P,BG).resize((a.shape[1]*z,a.shape[0]*z),Image.NEAREST)
fr=np.array(Image.open(V+'af/viscacha.png'))[:64]; front=img(fr,pal(V+'af/normal.pal'),4)
ic=np.array(Image.open(V+'icoon/af/icon.png'))[:32]; icp=Image.open(V+'icoon/af/icon.png').getpalette()[:48]
icon=img(ic,[tuple(icp[i*3:i*3+3]) for i in range(16)],8)
ow=np.array(Image.open(V+'overworld_eigen/af/overworld.png'))
rows=[[front,icon]+[img(ow[:,k*32:k*32+32],PAL,8) for k in (0,2,4)]]
for s in ('rattata','eevee','sentret'):
    o=np.array(Image.open(R+f'/graphics/pokemon/{s}/overworld.png')); P=pal(R+f'/graphics/pokemon/{s}/overworld_normal.pal')
    rows.append([None,None]+[img(o[:,k*32:k*32+32],P,8) for k in (0,2,4)])
W=256+256+3*256+5*10; Hh=len(rows)*266; out=Image.new('RGB',(W,Hh),(235,235,228)); d=ImageDraw.Draw(out)
for r,row in enumerate(rows):
    x=0
    for t in row:
        if t is not None: out.paste(t,(x,r*266))
        x+=256+10
d.text((4,270),'echte OW: rattata / eevee / sentret ->',fill=(0,0,0))
# 1x
small=Image.new('RGB',(200,40),BG); small.paste(rgba(ow,PAL,BG),(4,4))
out.paste(small,(256+10,266*1+60))
out.save(V+'overworld_eigen/af/vel_vergelijk.png'); print('ok')

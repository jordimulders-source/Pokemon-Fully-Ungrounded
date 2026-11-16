# Opschoning frame 2 van combi_c (16 nov): alleen rotatie-artefacten in de gedraaide bol.
# Niets getekend: ogen en grijns zijn letterlijk uit frame 1 (lijf_zonder_manen_v15) overgenomen,
# de grijns in 4 starre stroken (naden op de tandscheidingen) met de verschuiving van de 10°-rotatie
# per strook; daarna een handvol losse randpixels. Manen, frame 1, silhouet (op 3 px na) en palet ongewijzigd.
# Draaien vanuit de repo-root: python3 docs/concept/sprites/gengas/frame2/schoon/schoon.py
import math,numpy as np
from PIL import Image,ImageDraw
B='docs/concept/sprites/gengas/'
O=B+'frame2/schoon/'
im=Image.open(B+'frame2/combi_c_anim_front.png');pal=im.getpalette()
A=np.array(im);f1=A[:64].copy();f2=A[64:].copy()
lijf=np.array(Image.open(B+'sprite_v15/lijf_zonder_manen_v15.png'))
lab=np.load(B+'frame2/manen_lab.npy')
MANEN={1:(-14,9),2:(-8,-7),5:(10,11),11:(8,-7)}
M=np.zeros((64,64),bool)
for k,(mx,my) in MANEN.items():
    ys,xs=np.where(lab==k);M[ys+my,xs+mx]=True
# gedraaide bol zonder manen (zoals combi_c.py)
L=Image.fromarray(lijf,'P');L.putpalette(pal)
R=np.array(L.rotate(-10,resample=Image.NEAREST,center=(32,34),fillcolor=0))
bol=np.zeros_like(R);ys,xs=np.where(R!=0);bol[ys-3,xs]=R[ys,xs]
def rand(g):  # pixels met een transparante buur (8-buren): omlijning, niet aankomen
    op=g!=0;p=np.pad(op,1);t=np.zeros_like(op)
    for dy in(-1,0,1):
        for dx in(-1,0,1):t|=~p[1+dy:65+dy,1+dx:65+dx]
    return t&op
Rf=rand(np.where(M,1,bol));Rl=rand(lijf)
c=f2.copy()
def neem_over(y0,y1,x0,x1,dy,dx):
    """lijf[y0:y1,x0:x1] letterlijk naar (y+dy,x+dx); nooit op omlijning, manen of transparant."""
    for y in range(y0,y1):
        for x in range(x0,x1):
            Y,X=y+dy,x+dx
            if Rl[y,x] or Rf[Y,X] or M[Y,X] or bol[Y,X]==0:continue
            c[Y,X]=lijf[y,x]
# ogen: letterlijk, op de plek waar de rotatie ze zet (links (−6,0), rechts (−4,0))
neem_over(30,38,10,17,-6,0)
neem_over(29,38,24,32,-4,0)
# grijns: 4 starre stroken, naden vlak voor de tandscheidingen; dy volgt de 10°-helling, dx = -1
for x0,x1,y0,dy in [(8,20,39,-6),(20,25,39,-5),(25,35,38,-4),(35,37,37,-3)]:
    neem_over(y0,50,x0,x1,dy,-1)
# losse reparaties (y,x): waarde
FIX={
 (37,8):6,   # dubbele omlijning links naast de grijns
 (40,10):5,  # randpixel naast de grijns (zoals frame 1: 1-5-5)
 (43,11):1,(44,11):1,  # gat in de omlijning linksonder
 (46,46):1,(49,16):1,(51,40):1,  # gaten in de omlijning onderaan (trap zonder hoekpixel)
 (30,52):1,  # deuk/gat in de omlijning rechts
 (10,53):1,(12,54):1,  # oorpunt rechts: omlijning sluit weer (zoals frame 1)
 (18,59):6,(18,61):0,  # los zwevend gaspluimpje: 1 px naar links, weer vast aan de gasarm
 (37,34):5,  # dubbele lijn in de rechter mondhoek (naad strook 3/4)
 (43,24):2,  # tandscheiding stak door de onderlip (naad strook 2/3)
}
for (y,x),v in FIX.items():c[y,x]=v
# controles
assert (A[:64]==f1).all()
assert (c[M]==f2[M]).all(),'manen gewijzigd'
assert set(np.unique(c))<=set(np.unique(A)),'nieuwe paletindex'
d=np.argwhere(c!=f2)
sil=((c!=0)!=(f2!=0)).sum()
print('gewijzigd',len(d),'pixels; silhouet',sil,'px')
out=Image.fromarray(np.vstack([f1,c]),'P');out.putpalette(pal);out.save(O+'combi_c_anim_front_schoon.png')
with open(O+'gewijzigd.txt','w') as fh:
    for y,x in d:fh.write('%d,%d: %d -> %d\n'%(y,x,f2[y,x],c[y,x]))
# voor/na-vel
def rgb(x,Z,crop=None,grid=False):
    if crop:y0,y1,x0,x1=crop;x=x[y0:y1,x0:x1]
    x=np.ascontiguousarray(x);o=Image.fromarray(x,'P');o.putpalette(pal);a=np.array(o.convert('RGB'));a[x==0]=(255,255,255)
    h,w=x.shape;o=Image.fromarray(a).resize((w*Z,h*Z),Image.NEAREST)
    if grid:
        dr=ImageDraw.Draw(o)
        for i in range(w+1):dr.line([(i*Z,0),(i*Z,h*Z)],fill=(200,200,200))
        for j in range(h+1):dr.line([(0,j*Z),(w*Z,j*Z)],fill=(200,200,200))
    return o
def kader(x,crop):  # wijzigingen in rood omlijnd
    y0,y1,x0,x1=crop;o=rgb(x,16,crop,True);dr=ImageDraw.Draw(o)
    for y,xx in d:
        if y0<=y<y1 and x0<=xx<x1:dr.rectangle([(xx-x0)*16,(y-y0)*16,(xx-x0)*16+15,(y-y0)*16+15],outline=(255,0,0))
    return o
rows=[]
r1=[rgb(f1,8),rgb(f2,8),rgb(c,8)]
rows.append(r1)
for crop in [(24,45,5,37),(8,15,44,58),(16,24,52,63),(28,53,4,54)]:
    rows.append([rgb(f2,16,crop,True),kader(c,crop)])
W=max(sum(i.width for i in r)+12*len(r) for r in rows);H=sum(max(i.height for i in r)+30 for r in rows)
vel=Image.new('RGB',(W,H),'white');dr=ImageDraw.Draw(vel);y=0
kop=[['frame 1','frame 2 voor','frame 2 na'],['gezicht voor','gezicht na (rood = gewijzigd)'],['oorpunt rechts voor','na'],['gaspluim rechts voor','na'],['randen onder/rechts voor','na']]
for r,k in zip(rows,kop):
    x=0
    for i,t in zip(r,k):dr.text((x+2,y+4),t,fill=(0,0,0));vel.paste(i,(x,y+20));x+=i.width+12
    y+=max(i.height for i in r)+30
vel.save(O+'voor_na.png')
# gif zoals combi_c.py (render met vslide), met het opgeschoonde frame
def rgba(x):
    o=Image.fromarray(x,'P');o.putpalette(pal);q=np.array(o.convert('RGBA'));q[x==0,3]=0;return Image.fromarray(q)
F=[rgba(f1),rgba(c)]
SIN=lambda i,amp:int(math.sin(2*math.pi*(i%256)/256)*amp)
def vslide(t):return (0,-SIN(t*384//40,6) if t<=40 else 0,0)
def render(anim,naam,start=6,eind=40,Z=5):
    imgs=[];dur=[]
    for t in range(0,70,2):
        dx,dy,rot=anim(t);f=1 if start<=t<eind else 0
        s=F[f].rotate(rot*360/65536,resample=Image.NEAREST,center=(32,32))
        cv=Image.new('RGBA',(96,96),(255,255,255,255));cv.alpha_composite(s,(16+dx,16+dy))
        imgs.append(cv.convert('RGB').resize((96*Z,96*Z),Image.NEAREST));dur.append(33)
    dur[-1]=1000
    imgs[0].save(O+naam,save_all=True,append_images=imgs[1:],duration=dur,loop=0)
render(vslide,'combi_c_v_slide_schoon.gif')

# r22: verschil tussen verre (boven) en nabije (onder) vleugel. Alleen vleugelpixels (index 9-12), silhouet gelijk.
# Lichte scheidingslijn (index 10) waar de nabije vleugel over de verre valt (Jordi: "misschien lijn met lichte kleur");
# de bestaande binnenrand r21 x40-46 wordt doorgetrokken naar de wortel (richting uit het model, lengtes 4-3-3-3-7).
# Buitenrand (r19 x53-55, r20 x47-52) blijft selout: geen lichte kleur op de buitenrand.
import sys
from PIL import Image, ImageDraw
sys.path.insert(0,'../keuring_r20'); import refs
K='../keuring_r20/'
LIJN={25:range(27,31),24:range(31,34),23:range(34,37),22:range(37,40),21:range(40,47)}
lijnrij={x:y for y,xs in LIJN.items() for x in xs}
def lijn_y(x):  # bovengrens nabije vleugel per kolom
    if x in lijnrij: return lijnrij[x]
    return 25 if x<27 else 20
VLEUGEL={9,10,11,12}
def maak(src,var):
    im=Image.open(src); px=im.load()
    for y in range(14,29):
        for x in range(23,57):
            c=px[x,y]
            if c not in VLEUGEL: continue
            if lijnrij.get(x)==y: px[x,y]=10; continue
            if y<lijn_y(x) and x<=46:          # verre vleugel (binnenvlak; omlijning 9 blijft)
                if var=='V1': px[x,y]={10:11,11:12}.get(c,c)
                else:         px[x,y]={10:12,11:12}.get(c,c)
    px[31,25]=10 if px[31,25]==12 else px[31,25]   # donker veinpixel direct onder de lichte lijn -> nabije vleugel licht
    return im
def rgba(p,bg=None):
    pal=p.getpalette(); q=p.load(); o=Image.new('RGBA',p.size,bg or (0,0,0,0)); oo=o.load()
    for y in range(64):
        for x in range(64):
            if q[x,y]: oo[x,y]=tuple(pal[3*q[x,y]:3*q[x,y]+3])+(255,)
    return o
base=Image.open(K+'vlieg_r21.png'); bp=base.load()
uit={}
for var in ('V1','V2'):
    for suf,src in (('',K+'vlieg_r21.png'),('_lichter',K+'vlieg_r21_lichter.png')):
        im=maak(src,var); n=f'vlieg_r22_{var}{suf}'
        im.save(n+'.png',transparency=0)
        Image.alpha_composite(Image.new('RGBA',(64,64),(255,255,255,255)),rgba(im)).resize((512,512),Image.NEAREST).save(n+'_8x.png')
        q=im.load(); d=[(x,y) for y in range(64) for x in range(64) if q[x,y]!=bp[x,y]]
        buiten=[p for p in d if not(bp[p] in VLEUGEL and 14<=p[1]<=28)]
        sil=[(x,y) for y in range(64) for x in range(64) if (q[x,y]==0)!=(bp[x,y]==0)]
        print(n,'gewijzigd',len(d),'buiten vleugels',len(buiten),'silhouet',len(sil))
        uit[n]=im
# vel
r21=rgba(base); r21l=rgba(Image.open(K+'vlieg_r21_lichter.png'))
rij=[('r21',r21)]+[(n[6:],rgba(uit[n])) for n in ('vlieg_r22_V1','vlieg_r22_V2','vlieg_r22_V1_lichter','vlieg_r22_V2_lichter')]
S=8; w=64*S; c=Image.new('RGBA',(5*(w+10),w+30+17*12+40+220),(255,255,255,255)); d=ImageDraw.Draw(c)
for i,(t,s) in enumerate(rij):
    X=i*(w+10); d.text((X+4,4),t+' 8x',fill=(0,0,0,255)); c.alpha_composite(s.resize((w,w),Image.NEAREST),(X,20))
    vl=s.crop((22,14,58,31)).resize((36*12,17*12),Image.NEAREST); c.alpha_composite(vl,(X,w+40))
Y=w+40+17*12+20
for k,bg in enumerate(((255,255,255,255),(40,40,48,255))):
    d.rectangle([0,Y+k*100-6,c.width,Y+k*100+90],fill=bg)
    for i,(t,s) in enumerate(rij+[('ninjask',refs.load('ninjask'))]): c.alpha_composite(s,(20+i*90,Y+k*100))
d.text((4,w+24),'vleugels 12x',fill=(0,0,0,255)); d.text((4,Y-18),'1x licht/donker: r21 | V1 | V2 | V1 lichter | V2 lichter | ninjask',fill=(0,0,0,255))
c.convert('RGB').save('vel.png')

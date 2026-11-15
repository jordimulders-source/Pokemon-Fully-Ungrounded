# Gezicht-opties Hauntflare (Jordi 15 nov): linkeroog = gespiegeld rechteroog (+ hoekvarianten), mond lager en meer naar links.
import numpy as np; from PIL import Image, ImageDraw, ImageFont
im=Image.open('sprite_v6/hauntflare_v6.png'); pal=im.getpalette(); V6=np.array(im)
LIJN={1,2,14}
def doos(a,x0,x1,y0,y1,vals): return [(x,y) for y in range(y0,y1+1) for x in range(x0,x1+1) if a[y,x] in vals]
R=doos(V6,27,37,22,29,LIJN)                      # rechteroog (lijnen + oogwit)
L=doos(V6,17,25,19,30,LIJN)                      # huidig linkeroog
M=doos(V6,24,40,30,37,LIJN|{10})                 # huidige mond (lijnen, binnenkant)
M+= [(x,y) for y in range(31,38) for x in range(24,41) if V6[y,x]==8 and any(V6[y+dy,x+dx] in (1,10) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
def wis(a,pts):
    for x,y in pts:   # bolkleur uit de rij: dichtstbijzijnde bolpixel (5..9) links of rechts
        for d in range(1,15):
            for xx in (x-d,x+d):
                if 0<=xx<64 and a[y,xx] in (6,7,8,9) and (xx,y) not in pts: a[y,x]=a[y,xx]; break
            else: continue
            break
def oog_gespiegeld(a,rechts_x,dy=0,schuif=None,smal=0):
    xs=[p[0] for p in R]; x0,x1=min(xs),max(xs)
    pts={}
    for x,y in R:
        mx=x0+x1-x            # spiegel binnen de eigen doos
        pts[(mx,y)]=V6[y,x]
    # pupil(len) = zwarte pixels binnen het oogwit: terug naar de linkerkant (kijkt naar links, zoals het rechteroog)
    pup=[(x,y) for (x,y) in R if V6[y,x]==1 and V6[y,x-1]==14 or (V6[y,x]==1 and V6[y,x+1]==14 and V6[y,x-1]==14)]
    for x,y in pup:
        mx=x0+x1-x; pts[(mx,y)]=14
    PUP=[(x,y) for (x,y) in R if V6[y,x]==1 and 0<x and V6[y,x-1]==14 and V6[y,x+1]==14]
    for x,y in PUP:
        # zelfde afstand tot de linkerrand van het oogwit als in het rechteroog
        wl=min(xx for (xx,yy) in R if yy==y and V6[yy,xx]==14)
        wl2=min(xx for (xx,yy) in pts if yy==y and pts[(xx,yy)]==14)
        pts[(wl2+(x-wl),y)]=1
    # smaller (perspectief): kolommen weg aan de buitenkant (links)
    for k in range(smal):
        cx=min(p[0] for p in pts); pts={ (x+ (1 if x<cx+ (x1-x0)//2 else 0) if False else x,y):v for (x,y),v in pts.items() if x!=cx+1+2*k}
    w=max(p[0] for p in pts)
    out={}
    for (x,y),v in pts.items():
        sx=0 if schuif is None else schuif(y)
        out[(x-w+rechts_x+sx,y+dy)]=v
    for (x,y),v in out.items(): a[y,x]=v
MOND=["K.............K",
      ".KKKKKKKKKKKKK.",
      ".KPPPDPPPDPPPK.",
      ".KDPDDDPDDDPDK.",
      "..KDDPDDDPDDK..",
      "...KPPPDPPPK...",
      "....KKKKKKK...."]
def mond(a,x0,y0,breed=None):
    # met de hand gezet (Jordi: mond mag getekend worden: donkere opening, V-tanden in de kleur van het hoofd)
    k={'K':1,'D':10,'P':8}
    for j,r in enumerate(MOND):
        for i,c in enumerate(r):
            if c in k: a[y0+j,x0+i]=k[c]
def bouw(naam,oogargs,mondpos):
    a=V6.copy(); wis(a,L+M)
    oog_gespiegeld(a,**oogargs); mond(a,*mondpos)
    o=Image.fromarray(a.astype('uint8'),'P'); o.putpalette(pal); o.save(f'gezicht_v7/{naam}.png',transparency=0); return o
opts=[('A_spiegel',dict(rechts_x=25),(21,32)),
      ('B_spiegel_schuin',dict(rechts_x=25,schuif=lambda y:(y-22)//3),(21,32)),
      ('C_spiegel_omhoog',dict(rechts_x=25,dy=-1),(21,32)),
      ('D_spiegel_steiler',dict(rechts_x=24,schuif=lambda y:-(y-22)//3),(21,32))]
ims=[(n,bouw(n,o,m)) for n,o,m in opts]
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
S=10; v=Image.new('RGB',(len(ims)*(36*S+20)+20+300,30*S+70),'white'); d=ImageDraw.Draw(v)
def rgb(o):
    o.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/931d0048-d45a-55a4-a2ad-8ad05568e8ad/scratchpad/t.png',transparency=0)
    r=Image.open('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/931d0048-d45a-55a4-a2ad-8ad05568e8ad/scratchpad/t.png').convert('RGBA'); bg=Image.new('RGBA',r.size,(255,255,255,255)); bg.alpha_composite(r); return bg.convert('RGB')
for i,(n,o) in enumerate(ims):
    x=20+i*(36*S+20); v.paste(rgb(o).crop((8,12,44,42)).resize((36*S,30*S),Image.NEAREST),(x,40)); d.text((x,8),n,fill='black',font=f)
v.save('gezicht_v7/opties.png')
# vel met hele sprites (6x) + 1x
S2=6; vv=Image.new('RGB',(len(ims)*(64*S2+20)+20,64*S2+130),'white'); dd=ImageDraw.Draw(vv)
for i,(n,o) in enumerate(ims):
    x=20+i*(64*S2+20); r=rgb(o); vv.paste(r.resize((64*S2,64*S2),Image.NEAREST),(x,40)); dd.text((x,8),n,fill='black',font=f)
    vv.paste(r,(x,64*S2+50)); vv.paste(r.resize((128,128),Image.NEAREST),(x+80,64*S2+50) if False else (x+80,64*S2+50))
vv.save('gezicht_v7/opties_heel.png')

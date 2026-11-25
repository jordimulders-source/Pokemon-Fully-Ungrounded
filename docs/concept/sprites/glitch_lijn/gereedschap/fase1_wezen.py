"""Jordi (25 nov): "maak eens wat variaties van de 2e waar je vaag een vorm in ziet die we in fase 2
willen maken maar echt geglitcht". Fase 2-vorm (Jordi): "een vorm zonder benen ... simpele ronde vorm
maar niet volledig rond, bovenkant wat puntiger ... heeft wel twee armen maar die zijn wat aan de
dunne kant". Zelfde vulling (ROM-data als 2-bitspatroon, donker gezichtsvlak + grijs lijf, ogen
als lichtere rommel) en dezelfde kapotmaak-stap als de 2e (eigen_missingno_kapot.py, geen kleurbaan).
Gebruik: python3 fase1_wezen.py ROM UITMAP"""
import sys, os, random, math
from PIL import Image
sys.path.insert(0,os.path.dirname(__file__))
rom=open(sys.argv[1],'rb').read(); uit=sys.argv[2]; os.makedirs(uit,exist_ok=True)
ns={}; exec(open(os.path.join(os.path.dirname(__file__),'eigen_missingno_kapot.py')).read().split('ims=[]')[0].replace("uit=sys.argv[1]; os.makedirs(uit,exist_ok=True); bases=[Image.open(p).convert('RGBA') for p in sys.argv[2:]]",""),ns)
kapot=ns['kapot']
TD=[(40,40,48),(58,58,68),(78,78,90)]; TG=[(96,98,104),(136,140,146),(176,180,186),(212,214,218)]; LIJN=(16,16,20)
def vorm(r,armen,tilt,breed,sc=1.0):
    """masker: 0 leeg, 1 lijf, 2 gezichtsvlak, 3 arm"""
    m=[[0]*64 for _ in range(64)]; cx,cy=32,40; rx,ry=breed*sc,15*sc
    for y in range(64):
        for x in range(64):
            if ((x-cx)/rx)**2+((y-cy)/ry)**2<1: m[y][x]=1
            # puntige bovenkant: driehoek van de lijftop naar een punt, iets scheef
            top=cy-ry+3; tipx,tipy=cx+tilt*sc,cy-ry-11*sc
            if tipy<=y<=top:
                f=(y-tipy)/(top-tipy); hw=f*rx*0.75; mid=tipx+(cx-tipx)*f
                if abs(x-mid)<=hw: m[y][x]=1
            if ((x-cx)/(rx*0.72))**2+((y-(cy-5))/(ry*0.55))**2<1: m[y][x]=2
    T=lambda x,y:(round(cx+(x-32)*sc),round(cy+(y-38)*sc))
    for (sx,sy),(ex,ey) in [(T(*a),T(*b)) for a,b in armen]:   # dunne armen (2 px) met kleine hand
        n=int(max(abs(ex-sx),abs(ey-sy)))+1
        for k in range(n):
            x=round(sx+(ex-sx)*k/n); y=round(sy+(ey-sy)*k/n)
            for a in (0,1):
                if 0<=x+a<64 and 0<=y<64 and m[y][x+a]==0: m[y][x+a]=3
        for a in range(-1,2):
            for b in range(-1,2):
                if 0<=ex+a<64 and 0<=ey+b<64 and m[ey+b][ex+a]==0 and r.random()<0.8: m[ey+b][ex+a]=3
    return m
def vul(m,r,base,ogen):
    im=Image.new('RGBA',(64,64),(0,0,0,0)); px=im.load()
    for y in range(64):
        for x in range(64):
            z=m[y][x]
            if not z: continue
            # omlijning: rand van het masker
            rand=any(not (0<=x+a<64 and 0<=y+b<64) or m[y+b][x+a]==0 for a,b in ((1,0),(-1,0),(0,1),(0,-1)))
            if z==3: px[x,y]=(TD[0] if (x+y)%3 else TD[1])+(255,); continue
            if rand: px[x,y]=LIJN+(255,); continue
            bt=rom[base+(y*32+x//4)%4096]; v=(bt>>((x%4)*2))&3
            if z==2:
                col=TD[min(2,v)]
                for ex,ey in ogen:
                    d=math.hypot(x-ex,(y-ey)*1.15)
                    if d<3.2:
                        k=1-d/3.2
                        if r.random()<0.35+0.65*k: col=TG[min(3,1+int(k*3)+(v>1))]
                px[x,y]=col+(255,)
            else: px[x,y]=TG[v]+(255,)
    return im
ARMEN=[ [((15,38),(8,24)),((49,38),(56,24))],      # beide omhoog
        [((15,40),(5,36)),((49,40),(59,36))],      # opzij
        [((15,38),(7,26)),((49,42),(58,48))],      # een omhoog, een omlaag
        [((16,36),(10,22)),((48,36),(55,30))] ]
SC=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
ims=[]
for i in range(8):
    r=random.Random(100+i); breed=r.choice([15,17,18]); tilt=r.choice([-4,-2,2,4,6])
    m=vorm(r,ARMEN[i%4],tilt,breed,SC); base=0x300000+r.randrange(0,0x4000)*4
    ogen=[(round(32-6*SC),round(40-5*SC)+r.choice([0,1])),(round(32+6*SC),round(40-5*SC))]
    im=vul(m,r,base,ogen); im=kapot(im,21+i,'breek',True,False); ims.append(im); im.save(f'{uit}/w{i+1}.png')
sh=Image.new('RGB',(4*68+4,2*68+4),(255,255,255))
for i,im in enumerate(ims): sh.paste(im,(4+(i%4)*68,4+(i//4)*68),im)
sh.resize((sh.size[0]*4,sh.size[1]*4),Image.NEAREST).save(f'{uit}/vel.png')

"""Jordi (25 nov): kleiner voor fase 1; "ik denk dat het silhouet wel het beste uit de verf komt
zonder dingen eruit te knippen". Zelfde stappen als beste_hap_linksonder.png, maar het Gemini-
silhouet eerst op een kleinere maat (zones per blok met meerderheid, niets weggeknipt), dan vullen
(ROM-data 2-bit, cel 2, ogen als lichtere rommel), kapot (seed 21, breek, lek, geen kleurbaan) en
de hap linksonder met rafelrand.
Gebruik: python3 fase1_klein.py GEMINI.png ROM UITMAP schaal1 schaal2 ..."""
import sys, os, random, math
from collections import Counter
from PIL import Image
VAST_OOG=os.environ.get("VAST_OOG")=="1"   # ogen even groot als op de grote versie
G=sys.argv[1]; rom=open(sys.argv[2],'rb').read(); uit=sys.argv[3]; schalen=[float(a) for a in sys.argv[4:]]
os.makedirs(uit,exist_ok=True)
ns={}; exec(open(os.path.join(os.path.dirname(__file__),'eigen_missingno_kapot.py')).read().split('ims=[]')[0].replace("uit=sys.argv[1]; os.makedirs(uit,exist_ok=True); bases=[Image.open(p).convert('RGBA') for p in sys.argv[2:]]",""),ns)
kapot=ns['kapot']
src=Image.open(G).convert('RGB'); px=src.load(); W,H=src.size; P=10
xs=[x for x in range(W) for y in range(0,H,8) if sum(px[x,y])<600]; ys=[y for y in range(H) for x in range(0,W,8) if sum(px[x,y])<600]
x0,y0=min(xs),min(ys); nw,nh=(max(xs)-x0)//P+1,(max(ys)-y0)//P+1
def zone(c):
    r,g,b=c; l=(r+g+b)/3; sat=max(c)-min(c)
    if l>235 and sat<20: return None
    if sat>60: return 'kleur'
    if l<28: return 'lijn'
    if l<75: return 'donker'
    return 'grijs'
nat=[[None]*nw for _ in range(nh)]; natc=[[None]*nw for _ in range(nh)]
for j in range(nh):
    for i in range(nw):
        cs=[px[min(W-1,x0+i*P+a),min(H-1,y0+j*P+b)] for a in (3,5,7) for b in (3,5,7)]
        c=sorted(cs,key=sum)[4]; nat[j][i]=zone(c); natc[j][i]=c
OGEN=[(33.1,18.6),(17.5,18.375)]
TINT={'donker':[(40,40,48),(58,58,68),(78,78,90)],'grijs':[(96,98,104),(136,140,146),(176,180,186),(212,214,218)],'lijn':[(16,16,20)]}
def verklein(s):
    w,h=max(1,round(nw*s)),max(1,round(nh*s)); z=[[None]*w for _ in range(h)]; c=[[None]*w for _ in range(h)]
    for j in range(h):
        for i in range(w):
            a0,a1=int(i/s),max(int(i/s)+1,int((i+1)/s)); b0,b1=int(j/s),max(int(j/s)+1,int((j+1)/s))
            vs=[(nat[b][a],natc[b][a]) for b in range(b0,min(nh,b1)) for a in range(a0,min(nw,a1))]
            cnt=Counter(v[0] for v in vs)
            # rand behouden: lijn wint als hij aan de buitenkant ligt, kleurpixels blijven bestaan
            if cnt.get('kleur'): k='kleur'
            elif cnt.get(None,0)>len(vs)/2: k=None
            elif cnt.get('lijn') and cnt.get(None): k='lijn'
            else: k=max((x for x in cnt if x),key=lambda x:cnt[x],default=None)
            z[j][i]=k; c[j][i]=next((v[1] for v in vs if v[0]==k),None)
    return z,c,w,h
def maak(s,hap=True):
    z,c,w,h=verklein(s); r=random.Random(9); base=0x100000+r.randrange(0,0x400)*4
    im=Image.new('RGBA',(64,64),(0,0,0,0)); po=im.load(); ox,oy=(64-w)//2,64-h-1
    ogen=[(ex*s,ey*s) for ex,ey in OGEN]; rad=3.2*1.1*(1 if VAST_OOG else max(0.7,s))
    for j in range(h):
        for i in range(w):
            k=z[j][i]
            if k is None: continue
            if k=='kleur': po[ox+i,oy+j]=c[j][i]+(255,); continue
            if k=='lijn': po[ox+i,oy+j]=TINT['lijn'][0]+(255,); continue
            ci,cj=i//2,j//2; b=rom[base+(cj*32+ci//4)%4096]; v=(b>>((ci%4)*2))&3
            col=TINT[k][v if k=='grijs' else min(2,v)]
            if k=='donker':
                for ex,ey in ogen:
                    d=math.hypot(i-ex,(j-ey)*1.15)
                    if d<rad:
                        q=1-d/rad
                        if r.random()<0.35+0.65*q: col=TINT['grijs'][min(3,1+int(q*3)+(v>1))]
            po[ox+i,oy+j]=col+(255,)
    if not hap:
        im=kapot(im,21,'breek',True,False)
        if VAST_OOG:   # ogen na het kapotmaken nog eens op dezelfde manier oplichten, zodat de verschuivingen ze niet uitwissen
            q=im.load(); r3=random.Random(5); D=set(TINT['donker'])
            for ex,ey in ogen:
                for yy in range(int(oy+ey-5),int(oy+ey+6)):
                    for xx in range(int(ox+ex-5),int(ox+ex+6)):
                        if not (0<=xx<64 and 0<=yy<64): continue
                        pp=q[xx,yy]
                        if pp[3]==0 or pp[:3] not in D: continue
                        d=math.hypot(xx-(ox+ex),(yy-(oy+ey))*1.15)
                        if d<rad:
                            k=1-d/rad; v=TINT['donker'].index(pp[:3])
                            if r3.random()<0.35+0.65*k: q[xx,yy]=TINT['grijs'][min(3,1+int(k*3)+(v>1))]+(255,)
        return im
    # hap linksonder (op het silhouet zelf, vóór het kapotmaken): vanaf middenlinks, zelfde verhouding als op de grote (x tot 47 %, y vanaf 54 %)
    bb=im.getbbox(); hx=bb[0]+int((bb[2]-bb[0])*0.47); hy=bb[1]+int((bb[3]-bb[1])*0.54)
    p=im.load(); rr=random.Random(4); ZW=(16,16,20,255); KL=[(60,220,230,255),(232,60,200,255),(240,220,40,255)]
    for y in range(hy,64):
        for x in range(0,hx): p[x,y]=(0,0,0,0)
    def raf(x,y):
        if 0<=x<64 and 0<=y<64: p[x,y]=rr.choice(KL) if rr.random()<0.08 else ZW
    for y in range(hy,63):
        if p[hx,y][3]:
            for kk in range(rr.choice([1,1,2])):
                if rr.random()<0.8: raf(hx-kk if rr.random()<0.5 else hx+kk,y)
    for x in range(bb[0],hx):
        if p[x,hy-1][3] and rr.random()<0.75: raf(x,hy-1 if rr.random()<0.6 else hy)
    return kapot(im,21,'breek',True,False)
rijen=[]
for hap in (False,True):
    rij=[]
    for s in schalen:
        im=maak(s,hap); rij.append(im); im.save(f'{uit}/klein_{int(s*100)}_{"hap" if hap else "heel"}.png')
    rijen.append(rij)
sh=Image.new('RGB',(len(schalen)*68+4,2*68+4),(255,255,255))
for j,rij in enumerate(rijen):
    for i,im in enumerate(rij): sh.paste(im,(4+i*68,4+j*68),im)
sh.resize((sh.size[0]*4,sh.size[1]*4),Image.NEAREST).save(f'{uit}/vel.png')

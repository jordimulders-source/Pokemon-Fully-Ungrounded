"""Fase 1, poging na Jordi (25 nov): Gemini-silhouet ("het is geen sprite, maar wel misschien een
silhouet die jij met glitch kan invullen"), "laten we onze eigen missingno ervan maken, met
organische ogen (niet erop getekend) de ogen heel neutraal". Geen kaartassets meer.
1) Gemini-beeld terug naar het eigen raster (±10 px per pixel) -> masker + zones (omlijning,
   donker gezichtsvlak, grijze banen, losse kleurpixels).
2) Zones vullen met MissingNo-achtige rommeldata: ROM-bytes (trainerdata, zoals MissingNo)
   als bitpatronen, in grove cellen, alleen de tinten van die zone.
3) Ogen: niet getekend; in het donkere vlak wordt de rommel op twee plekken geleidelijk lichter
   (zelfde data, lichtere tinten), rond en neutraal.
Gebruik: python3 eigen_missingno.py GEMINI.png ROM UITMAP"""
import sys, os, random, math
from PIL import Image
src=Image.open(sys.argv[1]).convert('RGB'); rom=open(sys.argv[2],'rb').read(); uit=sys.argv[3]
os.makedirs(uit,exist_ok=True)
P=10; px=src.load(); W,H=src.size
xs=[x for x in range(W) for y in range(0,H,8) if sum(px[x,y])<600]; ys=[y for y in range(H) for x in range(0,W,8) if sum(px[x,y])<600]
x0,y0=min(xs),min(ys); nw,nh=(max(xs)-x0)//P+1,(max(ys)-y0)//P+1
nat=Image.new('RGB',(nw,nh)); npx=nat.load()
for j in range(nh):
    for i in range(nw):
        cs=[px[min(W-1,x0+i*P+a),min(H-1,y0+j*P+b)] for a in (3,5,7) for b in (3,5,7)]
        npx[i,j]=sorted(cs,key=sum)[4]
nat.save(f'{uit}/natief.png')
def zone(c):
    r,g,b=c; l=(r+g+b)/3; sat=max(c)-min(c)
    if l>235 and sat<20: return None          # achtergrond
    if sat>60: return 'kleur'
    if l<28: return 'lijn'
    if l<75: return 'donker'
    return 'grijs'
# oogcentra uit het Gemini-beeld: lichte vlekken binnen het donkere vlak
lichte=[(i,j) for j in range(nh) for i in range(nw) if zone(npx[i,j])=='grijs' and all(zone(npx[min(nw-1,max(0,i+a)),min(nh-1,max(0,j+b))]) in ('donker','grijs') for a in (-2,2) for b in (-2,2)) and sum(1 for a in (-2,2) for b in (-2,2) if zone(npx[min(nw-1,max(0,i+a)),min(nh-1,max(0,j+b))])=='donker')>=3]
def clusters(pts):
    cl=[]
    for p in pts:
        for c in cl:
            if abs(c[0][0]-p[0])<4 and abs(c[0][1]-p[1])<4: c.append(p); break
        else: cl.append([p])
    return [(sum(a for a,b in c)/len(c),sum(b for a,b in c)/len(c)) for c in sorted(cl,key=len,reverse=True)[:2]]
OGEN=clusters(lichte); print('ogen',OGEN)
TINT={'donker':[(40,40,48),(58,58,68),(78,78,90)],'grijs':[(96,98,104),(136,140,146),(176,180,186),(212,214,218)],'lijn':[(16,16,20)]}
def maak(seed,bron,cel=1,oogsterkte=1.0):
    r=random.Random(seed); base=bron+r.randrange(0,0x400)*4
    out=Image.new('RGBA',(64,64),(0,0,0,0)); po=out.load(); ox,oy=(64-nw)//2,(64-nh)//2
    for j in range(nh):
        for i in range(nw):
            z=zone(npx[i,j])
            if z is None: continue
            if z=='kleur': po[ox+i,oy+j]=npx[i,j]+(255,); continue
            if z=='lijn': po[ox+i,oy+j]=TINT['lijn'][0]+(255,); continue
            ci,cj=i//cel,j//cel
            b=rom[base+(cj*32+ci//4)%4096]; v=(b>>((ci%4)*2))&3     # 2 bits per cel, zoals Gen 1-2bpp
            t=TINT[z]; idx=v if z=='grijs' else min(2,v)
            if z=='donker':
                for ex,ey in OGEN:
                    d=math.hypot(i-ex,(j-ey)*1.15)
                    if d<3.2*oogsterkte:
                        k=1-d/(3.2*oogsterkte)
                        if r.random()<0.35+0.65*k: idx=None; col=TINT['grijs'][min(3,1+int(k*3)+(v>1))]
                if idx is None: po[ox+i,oy+j]=col+(255,); continue
            po[ox+i,oy+j]=t[idx]+(255,)
    return out
bronnen=[0x651000,0x653800,0x656000,0x300000,0x100000]
ims=[]
for s,(b,cel,o) in enumerate([(bronnen[k%5],c,o) for k in range(5) for c,o in ((1,1.0),(2,1.1))]):
    im=maak(s,b,cel,o); ims.append(im); im.save(f'{uit}/m{s+1:02d}.png')
sh=Image.new('RGB',(5*68+4,2*68+4),(255,255,255))
for i,im in enumerate(ims): sh.paste(im,(4+(i%5)*68,4+(i//5)*68),im)
sh.resize((sh.size[0]*3,sh.size[1]*3),Image.NEAREST).save(f'{uit}/vel.png')

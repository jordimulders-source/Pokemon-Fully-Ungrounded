# Eindkeuring zandloper fase 2 (Dragonfly Cave): schaduw + belijning + tinten, reproduceerbaar vanaf r4.
# Alleen kleur van bestaande pixels; alpha (silhouet) en ogen (x22-37, y20-27) blijven gelijk.
# 1) belijning, outline shadow vs outline base: zwarte pixels die NIET aan transparant grenzen (4-buren) zijn
#    trapjeshoekjes/binnenlijnen (lijn plaatselijk 2 px zwart). Ze krijgen de outline base van hun onderdeel
#    (zand -> 2, glas -> 7, hout -> 11); de buitenste 1 px blijft zwart. Dikte en vorm blijven gelijk (Jordi: "niet dunner, kleur").
#    Uitzondering zoals fase 3: de zwarte knik in de hals van de zandloper (fase 3 heeft daar ook binnen-zwart).
# 2) outline highlights: op de lichtkant (transparant alleen boven/links) een zandlijnpixel waarvan de binnenbuur
#    de lichtste zandtint is -> zand-donker (3), zoals de gids ("shadow/outline highlight color on the outlines in
#    the very most highlighted parts ... on the inside of the outline").
# 3) tinten: palet ongewijzigd (zand en glas = fase 3, hout = fase 1).
import os, numpy as np
from PIL import Image
from collections import Counter
H=os.path.dirname(os.path.abspath(__file__))
src=Image.open(os.path.join(H,'../sprite/r4/zandloper_fase2_r4.png'))
o=np.asarray(src).copy(); a=o.copy(); pal=src.getpalette()[:48]
SAND={2,3,4,5,6,14}; GLAS={7,8,9,10}; HOUT={11,12,13}
EYE=np.zeros_like(a,bool); EYE[20:28,22:38]=True
HALS={(23,51),(24,52)}                       # (x,y) knik tussen de twee glasbollen, zwart zoals in fase 3
P=np.pad(o,1); T=lambda dy,dx: P[1+dy:65+dy,1+dx:65+dx]==0
op=o>0; e4=op&(T(0,1)|T(1,0)|T(0,-1)|T(-1,0))
def onderdeel(y,x):
    c=Counter()
    for r in (1,2):
        for dy in range(-r,r+1):
            for dx in range(-r,r+1):
                yy,xx=y+dy,x+dx
                if 0<=yy<64 and 0<=xx<64:
                    v=int(o[yy,xx]); w=1.0/(abs(dy)+abs(dx)+0.5)
                    if v in SAND: c['zand']+=w
                    elif v in GLAS: c['glas']+=w
                    elif v in HOUT: c['hout']+=w
        if c: break
    return c.most_common(1)[0][0]
BASE={'zand':2,'glas':7,'hout':11}
log=Counter(); zones=Counter()
def zone(y,x):
    if y>=43 and x<38 and y>=44: return 'zandloper (glas/kappen)'
    if x<=21 and 17<=y<=36: return 'vraagteken-hand + arm'
    if x>=46 and y<=37: return 'uitroepteken + rechterhand'
    if y<=27: return 'brein'
    return 'lijf/staart'
for y in range(64):
    for x in range(64):
        if o[y,x]==1 and not e4[y,x] and not EYE[y,x] and (x,y) not in HALS:
            d=onderdeel(y,x); a[y,x]=BASE[d]; log['binnen-zwart -> outline base %s'%d]+=1; zones[zone(y,x)]+=1
# 2) outline highlights
for y in range(64):
    for x in range(64):
        if o[y,x]!=2 or not e4[y,x] or EYE[y,x]: continue
        up,lf,rt,dn=T(-1,0)[y,x],T(0,-1)[y,x],T(0,1)[y,x],T(1,0)[y,x]
        if rt or dn or not (up or lf): continue
        inn=[]
        if up and y+1<64: inn.append(o[y+1,x])
        if lf and x+1<64: inn.append(o[y,x+1])
        if inn and all(v in (6,14) for v in inn):
            a[y,x]=3; log['outline highlight zand (2 -> 3)']+=1; zones[zone(y,x)]+=1
out=Image.fromarray(a,'P'); out.putpalette(pal+[0]*(768-48))
out.save(os.path.join(H,'zandloper_fase2_ek.png'),transparency=0)
out.convert('RGBA').resize((512,512),Image.NEAREST).save(os.path.join(H,'zandloper_fase2_ek_8x.png'))
print(dict(log)); print('per zone',dict(zones))
print('alpha-diff',int(((a>0)!=(o>0)).sum()),' ogen-diff',int((a!=o)[EYE].sum()),' totaal gewijzigd',int((a!=o).sum()))
print('kleuren (zonder transparant)',len(set(a[a>0].tolist())))

# vel.png: 8x model op spriteschaal | r4 | ek | fase 3 af | fase 1 af, daaronder 1x op licht en donker
from PIL import ImageDraw
G={'T':12.8,'cx':191.5,'cy':199.6,'ox':7,'oy':8}      # sprite/r1/geo_0.80.json
mdl=Image.open(os.path.join(H,'../model.png')).convert('RGB')
x0=(0-G['ox'])*G['T']+G['cx']-G['T']/2; y0=(0-G['oy'])*G['T']+G['cy']-G['T']/2
mcrop=mdl.crop((int(x0),int(y0),int(x0+64*G['T']),int(y0+64*G['T']))).resize((512,512),Image.LANCZOS)
paden=[os.path.join(H,'../sprite/r4/zandloper_fase2_r4.png'),os.path.join(H,'zandloper_fase2_ek.png'),
       os.path.join(H,'../../fase3/af/zandloper_fase3.png'),os.path.join(H,'../../fase1/af/zandloper_fase1.png')]
titels=['model (spriteschaal)','r4','eindkeuring','fase 3 af','fase 1 af']
def opbg(p,bg,z):
    r=Image.open(p).convert('RGBA'); b=Image.new('RGBA',r.size,bg); b.alpha_composite(r)
    return b.resize((64*z,64*z),Image.NEAREST).convert('RGB')
W=Image.new('RGB',(5*522+10,20+512+20+2*74),(255,255,255)); d=ImageDraw.Draw(W)
for i,t in enumerate(titels):
    d.text((10+i*522,4),t,fill=(0,0,0))
    W.paste(mcrop if i==0 else opbg(paden[i-1],(200,210,200,255),8),(10+i*522,20))
for i,p in enumerate(paden):
    W.paste(opbg(p,(240,240,232,255),1),(10+i*74,560)); W.paste(opbg(p,(40,44,52,255),1),(10+i*74,634))
d.text((320,590),'1x op licht en donker: r4 | ek | fase 3 | fase 1',fill=(0,0,0))
W.save(os.path.join(H,'vel.png'))

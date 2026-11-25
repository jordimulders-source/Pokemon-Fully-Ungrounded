# Bouwt rN: kale reductie (kaal_lab/avg/lf) -> omkleuren per zone (rangorde, brons/dof ijzer/licht hout)
# = "kaal gemapt" -> oog uit het natieve model -> benoemde reparaties (extra_rN.json) -> ontkorrelen -> buitenlijn/selout.
# Elke afwijking van "kaal gemapt" wordt per zone geteld en gelogd.
import numpy as np, sys, json, colorsys
from collections import Counter
from PIL import Image
RN=sys.argv[1] if len(sys.argv)>1 else 'r1'
PAL={'.':(0,0,0),'0':(24,16,20),
     'D':(64,32,16),'S':(104,56,26),'M':(156,90,38),'L':(204,132,66),   # brons (vacht)
     'C':(244,221,190),'c':(212,174,132),                                 # creme
     'N':(106,76,64),'n':(140,110,94),                                    # neus
     'H':(132,102,70),'h':(184,148,106),                                  # licht hout
     'I':(62,66,78),'J':(86,92,104),'K':(110,116,128)}                    # dof ijzer
ORDER=list(PAL)
L=np.load('kaal_mode_lab.npy'); A=np.load('kaal_avg.npy'); H,W=L.shape   # basis: per cel meest voorkomende modelkleur
def lum(c): return 0.299*c[0]+0.587*c[1]+0.114*c[2]
zone=[['' for _ in range(W)] for _ in range(H)]
g=[['.' for _ in range(W)] for _ in range(H)]
FUR={0:'0',1:'D',2:'D',3:'S',4:'S',5:'S',6:'S',7:'S',8:'M',9:'M',10:'M',11:'L',12:'L',13:'L',14:'L',15:'C'}
for y in range(H):
    for x in range(W):
        v=L[y,x]
        if v<0: continue
        z='vacht'
        if (v in (5,15) or (v==14 and y<=8)) and ((13<=x<=18 and y<=8 and not (x==13 and y==6)) or (22<=x<=28 and 3<=y<=9)): z='ijzer'
        elif v in (14,7,2,3) and ((6<=y<=10 and 11<=x<=14 and 19<=x+y<=22) or (9<=y<=15 and 18<=x<=25 and 32<=x+y<=35)): z='hout'
        elif x<=5 and 26<=y<=33 and v!=0: z='neus'
        elif v==15: z='creme'
        zone[y][x]=z
        if v==0: g[y][x]='0'; continue
        if z=='vacht': g[y][x]=FUR[v]
        elif z=='creme': g[y][x]='C'
        elif z=='ijzer': l=lum(A[y,x]); g[y][x]='I' if l<95 else 'J' if l<125 else 'K'
        elif z=='hout': g[y][x]='h' if v==14 else 'H'
        elif z=='neus': g[y][x]={7:'N',1:'D',2:'D'}.get(v,'N')
kaal=[r[:] for r in g]
log=[]
def put(zn,x,y,c,why):
    old=g[y][x]
    if old!=c: g[y][x]=c; log.append((zn,x,y,old,c,why))
# --- oog: 7x7 uit het natieve modeloog (12x12, natief x36-47 y36-47), per subblok gelezen (zie oog.txt; '-' = vacht laten) ---
EX,EY=json.load(open('oog.json'))[:2]
for j,row in enumerate(open('oog.txt').read().split()):
    for i,c in enumerate(row):
        if c!='-': put('oog',EX+i,EY+j,c,'oog uit natief model (subblok)')
# --- ontkorrelen: tintvlakjes <3 px nemen de meest voorkomende buurtint uit dezelfde kleurgroep ---
GROUPS=['DSML','Cc','Nn','Hh','IJK']
PROT=json.load(open('beschermd.json'))   # [[x0,y0,x1,y1],...] oog/neus/details
def prot(x,y): return any(a<=x<=b and c<=y<=d for a,c,b,d in PROT)
def comps():
    seen=set(); res=[]
    for y in range(H):
        for x in range(W):
            if (x,y) in seen or g[y][x] in '.0': continue
            v=g[y][x]; st=[(x,y)]; seen.add((x,y)); cc=[]
            while st:
                cx,cy=st.pop(); cc.append((cx,cy))
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=cx+dx,cy+dy
                    if 0<=nx<W and 0<=ny<H and (nx,ny) not in seen and g[ny][nx]==v: seen.add((nx,ny)); st.append((nx,ny))
            res.append((v,cc))
    return res
for _ in range(3):
    for v,cc in comps():
        if len(cc)>=3 or (v=='D' and (len(cc)>=2 or cc[0][1]>17)): continue
        if any(prot(x,y) or (13<=x<=18 and y<=8) or (22<=x<=28 and 3<=y<=9) for x,y in cc): continue   # oog/neus/ijzerpunten niet ontkorrelen
        grp=[G for G in GROUPS if v in G][0]
        nb=Counter(g[y+dy][x+dx] for x,y in cc for dx,dy in((1,0),(-1,0),(0,1),(0,-1))
                   if 0<=x+dx<W and 0<=y+dy<H and g[y+dy][x+dx] in grp and g[y+dy][x+dx]!=v)
        if nb:
            for x,y in cc: put('ontkorrel',x,y,nb.most_common(1)[0][0],'tintvlakje <3 px naar buurtint')
# --- binnenlijnen: modellijn binnen het silhouet -> donkerste eigen tint (geen zwart) ---
def opaque(x,y): return 0<=x<W and 0<=y<H and g[y][x]!='.'
DARK={'vacht':'D','creme':'D','hout':'H','ijzer':'I','neus':'0'}
for y in range(H):
    for x in range(W):
        if g[y][x]!='0' or zone[y][x]=='' or prot(x,y): continue
        if all(opaque(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1))):
            put('binnenlijn',x,y,DARK[zone[y][x]],'binnenlijn in donkerste eigen tint')
# --- buitenlijn dicht + gekleurde selout aan de lichtkant (boven/links) ---
SEL={'vacht':'D','creme':'c','hout':'H','ijzer':'I','neus':'D'}
for y in range(H):
    for x in range(W):
        if g[y][x]=='.' or prot(x,y): continue
        if any(not opaque(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) and g[y][x]!='0':
            put('lijn',x,y,'0','buitenlijn dicht')
for y in range(H):
    for x in range(W):
        if g[y][x]!='0' or prot(x,y): continue
        up=not opaque(x,y-1); lf=not opaque(x-1,y); dn=not opaque(x,y+1); rt=not opaque(x+1,y)
        if (up or lf) and not dn and not rt and zone[y][x]:
            zz=zone[y][x]
            if (13<=x<=18 and y<=8) or (22<=x<=28 and 3<=y<=9 and not (x<=23 and y==9)): zz='ijzer'
            put('lijn',x,y,SEL[zz],'selout lichtkant')
# --- benoemde reparaties (laatste laag, naar het model) ---
try: extra=json.load(open(f'extra_{RN}.json'))
except FileNotFoundError: extra=[]
for zn,x,y,c,why in extra: put(zn,x,y,c,why)
# --- naar 64x64, onderaan gecentreerd ---
OX=(64-W)//2; OY=58-H
img=np.zeros((64,64),'uint8')
for y in range(H):
    for x in range(W): img[OY+y,OX+x]=ORDER.index(g[y][x])
pal=[]
for k in ORDER: pal+=PAL[k]
pal+=[0,0,0]*(16-len(ORDER))
im=Image.fromarray(img,'P'); im.putpalette(pal)
im.save(f'{RN}/dikdik_{RN}.png',transparency=0)
im2=Image.open(f'{RN}/dikdik_{RN}.png').convert('RGBA'); im2.resize((512,512),Image.NEAREST).save(f'{RN}/dikdik_{RN}_8x.png')
json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g],'kaal':[''.join(r) for r in kaal]},open(f'{RN}/grid.json','w'),indent=0)
cnt=Counter(z for z,*_ in log)
print(RN,'afwijkingen per zone:',dict(cnt),'totaal',len(log),'van',sum(c!='.' for r in g for c in r),'px; kleuren',len(set(c for r in g for c in r)))
with open(f'{RN}/log.txt','w') as f:
    for e in log: f.write('%s (%d,%d) %s->%s  %s\n'%e)
print('\n'.join('%2d '%j+''.join(r) for j,r in enumerate(g)))

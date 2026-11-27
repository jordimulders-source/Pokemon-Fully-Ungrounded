# r14 = eindkeuring DC (uitvoering) op r13. Geen vorm veranderd: alleen lijnkleur (0 -> eigen donkerste tint aan de lichtkant
# en op binnenlijnen), 2 open randen dicht (M -> lijn), 2 paletttinten (K warmer, D 1 stap lichter). Zie r14/NOTITIES.md.
import math, numpy as np
from PIL import Image
P={'302418':'0','F8D888':'L','D8A850':'M','A07030':'D','D8AC30':'l','B08824':'m','7C5A10':'d','4A4A52':'A','8A8A92':'3',
   'C8C8CC':'4','FFFFFF':'W','E0A090':'R','B06A58':'r','5C4434':'K'}
a=np.array(Image.open('r13/kudu_r13.png').convert('RGBA'))
g=np.array([['.' if a[y,x,3]==0 else P['%02X%02X%02X'%tuple(a[y,x,:3])] for x in range(64)] for y in range(64)])
g0=g.copy(); H=W=64
# --- bevroren gezicht: oog K4 (x16-18 y22-23 + rand) en neus/mond; daar geen enkele pixel aanraken behalve de open rand (10,25)
GEZICHT=np.zeros((H,W),bool); GEZICHT[20:25,14:20]=True; GEZICHT[25:30,8:13]=True
GROEP={**{c:'v' for c in 'LMDKRr'},**{c:'h' for c in 'lmd'},**{c:'s' for c in 'A34'}}
BASIS={'v':'K','h':'K','s':'A'}  # goud (vacht + manen) deelt één lijnbasis, zoals Stantler '5'; d is te licht als lijn (stap 45 op m)
def opaak(x,y): return 0<=x<W and 0<=y<H and g0[y,x]!='.'
def groep(x,y):
    for r in (1,2):
        tel={}
        for dy in range(-r,r+1):
            for dx in range(-r,r+1):
                X,Y=x+dx,y+dy
                if not opaak(X,Y): continue
                c=g0[Y,X]
                if c=='W':  # wit: staal als er staal naast ligt, anders vacht (strepen, snuit)
                    c='A' if any(opaak(X+u,Y+v) and g0[Y+v,X+u] in 'A34' for u in (-1,0,1) for v in (-1,0,1)) else 'M'
                if c in GROEP: tel[GROEP[c]]=tel.get(GROEP[c],0)+1
        if tel: return max(tel,key=tel.get)
    return 'v'
# --- 1. buitenlijn: lichtkant (normaal naar links/boven, 20..215 graden) -> eigen donkerste tint; schaduwkant blijft zwart
buiten={}; HOEK={}
for y in range(H):
    for x in range(W):
        if g0[y,x]!='0' or GEZICHT[y,x]: continue
        nx=ny=0
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if (dx or dy) and not opaak(x+dx,y+dy): nx+=dx; ny+=dy
        if not any(not opaak(x+u,y+v) for u,v in ((1,0),(-1,0),(0,1),(0,-1))): continue
        if nx==0 and ny==0: buiten[(x,y)]=False; continue
        th=math.degrees(math.atan2(-ny,nx))%360
        buiten[(x,y)]= 35<th<215
        HOEK[(x,y)]=round(th)
# geen zwart/donker om en om: een lijnpixel waarvan alle buren op de rand de andere klasse hebben, volgt de buren
for _ in range(2):
    nieuw=dict(buiten)
    for (x,y),k in buiten.items():
        bur=[buiten[(x+u,y+v)] for u in (-1,0,1) for v in (-1,0,1) if (u or v) and (x+u,y+v) in buiten]
        if len(bur)>=2 and all(b!=k for b in bur): nieuw[(x,y)]=not k
    buiten=nieuw
REDEN={}
for (x,y),k in buiten.items():
    if k: g[y,x]=BASIS[groep(x,y)]; REDEN[(x,y)]='buitenlijn lichtkant -> '+g[y,x]
# --- 2. binnenlijnen (niet zwart): eigen donkerste tint van het voorste vlak
# automatisch: elke 0 die nergens aan transparant grenst (buiten het gezicht). Voorste vlak: manen (franje/manen liggen
# over hals, borst en lijf) > staal (hoorn over kop/oor) > vacht. Kleur = donkerste eigen tint van dat vlak.
def buren4(x,y): return [g0[y+v,x+u] for u,v in ((1,0),(-1,0),(0,1),(0,-1)) if opaak(x+u,y+v)]
for y in range(H):
    for x in range(W):
        if g0[y,x]!='0' or GEZICHT[y,x] or (x,y) in buiten: continue
        if any(not opaak(x+u,y+v) for u,v in ((1,0),(-1,0),(0,1),(0,-1))): continue
        b=set(buren4(x,y))
        if b&set('lmd'): c,r='K','manen/franje over hals, borst of lijf'
        elif b&set('A34'): c,r='A','hoorn over kop of oor'
        elif b&set('LMDKRrW'): c,r='K','vacht over vacht (oor/kaak)'
        else: continue
        g[y,x]=c; REDEN[(x,y)]='binnenlijn: '+r
# handmatig (redenen): schoft x34-39 y29-31 = 1 lijn vacht (K), manenpunt (35,29) d; hoornvoet/oortop rechts
for (x,y),c,r in [((35,29),'K','manenpunt'),((36,29),'K','schoftlijn'),((37,30),'K','schoftlijn'),((36,31),'K','schoftlijn'),
                  ((25,25),'K','bovenlijn manen achter de kop (was als vacht geteld)'),((15,17),'A','rechterlijn linkerhoorn waar hij over de kop valt'),
                  ((24,15),'A','onderlijn rechterhoorn boven het oor'),((25,15),'A','onderlijn rechterhoorn boven het oor'),((26,15),'A','onderlijn rechterhoorn boven het oor')]:
    assert g0[y,x]=='0',(x,y); g[y,x]=c; REDEN[(x,y)]='handmatig: '+r
# --- 3. open randen (lichte vacht op de buitenrand) dicht
for (x,y),r in [((10,25),'snuitrug: M op de buitenrand'),((22,18),'kop tussen hoorn en oor: M op de buitenrand')]:
    assert g0[y,x]=='M'; g[y,x]='K'; REDEN[(x,y)]='open rand dicht: '+r
# --- palet (15 kleuren + transparant)
HEX={'0':'302418','L':'F8D888','M':'D8A850','D':'A87432','l':'D8AC30','m':'B08824','d':'7C5A10','A':'4A4A52','3':'8A8A92',
     '4':'C8C8CC','W':'FFFFFF','R':'E0A090','r':'B06A58','K':'6E4614'}
ORDE=['0','K','A','d','r','D','m','3','l','M','R','4','L','W']
assert set(np.unique(g))-{'.'}<=set(ORDE)
idx=np.zeros((H,W),np.uint8)
for i,c in enumerate(ORDE): idx[g==c]=i+1
im=Image.fromarray(idx,'P'); pal=[0,0,0]
for c in ORDE: pal+=[int(HEX[c][i:i+2],16) for i in (0,2,4)]
im.putpalette(pal+[0]*(768-len(pal))); im.info['transparency']=0
im.save('r14/kudu_r14.png',transparency=0)
im.convert('RGBA').resize((512,512),Image.NEAREST).save('r14/kudu_r14_8x.png')
with open('r14/normal.pal','w') as f:
    f.write('JASC-PAL\n0100\n16\n'); f.write('0 0 0\n')
    for c in ORDE: f.write('%d %d %d\n'%tuple(int(HEX[c][i:i+2],16) for i in (0,2,4)))
    f.write('0 0 0\n')
np.save('r14/grid.npy',g)
with open('r14/pixels.txt','w') as f:
    for (x,y),r in sorted(REDEN.items(),key=lambda t:(t[0][1],t[0][0])): f.write('(%d,%d) %s -> %s  %s\n'%(x,y,g0[y,x],g[y,x],r))
print('px veranderd:',(g!=g0).sum(),'redenen:',len(REDEN))
print('   '+''.join(str(x%10) for x in range(64)))
for y in range(64): print('%2d '%y+''.join(g[y]))

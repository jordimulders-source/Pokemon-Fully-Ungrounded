# r5: achtersteven heel (natief 78-84 = lokaal 65-71 onaangeroerd). Basis = model met alleen de halskolommen 16/18
# geschrapt (72 breed, r5/bouw5.py = r4-opbouw), daarop links van natief 74 de r4-pixels 1-op-1 (bevroren),
# daarna 8 kolommen eruit met NADEN: per rij precies 1 modelpixel weg, aangrenzende rijen max. 1 px verspringend
# (kolomverschuiving per onderdeel; niets getekend, elke pixel blijft een r4/modelpixel).
#  A: 8 naden in romp/rand/water vóór de achtersteven (lokaal 49-64 = natief 62-77), nooit door ventje of bombilla.
#  B: 2 naden in het midden van het yerba-vak (lokaal 19-25 = natief 32-38, waar de zilveren rand recht loopt)
#     + 6 naden zoals A.
from PIL import Image; import numpy as np, subprocess
D='docs/concept/sprites/mate_fase2/sprite/'
subprocess.run(['python3',D+'r5/schrap5.py'],check=True,capture_output=True)
subprocess.run(['python3',D+'r5/bouw5.py'],check=True,capture_output=True)
idx=np.load(D+'r5/idx72.npy'); H,W=idx.shape
g=np.asarray(Image.open(D+'r5/geschrapt72.png').convert('RGB')).astype(int); L=.3*g[...,0]+.59*g[...,1]+.11*g[...,2]
r4=Image.open(D+'r4/mate2.png'); a4=np.asarray(r4).astype(int); pal=np.array(r4.getpalette()[:48]).reshape(16,3)
# 1. bevroren: lokaal 0-60 (natief t/m 73) = r4
idx[:,0:61]=a4[15:63,0:61]
# 2. waterval (lokaal >= 61): buitenrand water -> donkere modelrand (tint 15), schuim = modelpixels L>=220 -> wit
log={}
def zet(n,y,x,v):
    if idx[y,x]!=v: log.setdefault(n,[]).append((x,y,int(idx[y,x]),int(v))); idx[y,x]=v
isbg=lambda y,x: not(0<=y<H and 0<=x<W) or idx[y,x]==0
rand=[(y,x) for y in range(H) for x in range(61,W) if idx[y,x] in (13,14) and any(isbg(y+dy,x+dx) for dy,dx in((1,0),(-1,0),(0,1),(0,-1)))]
for y,x in rand: zet('waterrand',y,x,15)
for y in range(H):
    for x in range(61,W):
        if idx[y,x] in (13,14) and L[y,x]>=220: zet('schuim',y,x,12)
# lichte waterpixels die in bouw5 als zilver geclassificeerd zijn (alleen in het water rechts, lokaal >= 61) -> licht water
for y in range(13,30):
    for x in range(61,W):
        if 10<=idx[y,x]<=12 and L[y,x]<220: zet('zilver->water',y,x,14)
for k,v in log.items(): print(k,len(v),v)
base=idx.copy()
# verboden zones voor naden
verboden=np.zeros((H,W),bool)
verboden[:,65:]=idx[:,65:]>0                           # achtersteven + waterval (alleen achtergrond ernaast mag weg)
grp=lambda i: 'g' if 6<=i<=9 else 's' if 10<=i<=12 else 'o' if i==1 else 'w' if i in(13,14,15) else 'b' if 2<=i<=5 else '.'
for y in range(H):
    for x in range(W):
        if grp(idx[y,x]) in 'gs': verboden[y,x]=True      # ventje, yerba, bombilla's, rand
# omlijning die aan ventje/zilver grenst ook verboden (lijn om bombilla/ventje)
v2=verboden.copy()
for y in range(H):
    for x in range(W):
        if idx[y,x]==1 and any(0<=y+dy<H and 0<=x+dx<W and grp(idx[y+dy,x+dx]) in 'gs' for dy in(-1,0,1) for dx in(-1,0,1)): v2[y,x]=True
verboden=v2
def kleur(i): return np.array([255,255,255]) if i==0 else pal[i]
def naad(im,x0,x1,verb):
    h,w=im.shape; INF=1e9
    C=np.full((h,w),INF)
    rgb=np.array([[kleur(i) for i in row] for row in im]).astype(float)
    for y in range(h):
        for x in range(x0,x1+1):
            if verb[y,x]: continue
            l=rgb[y,x-1]; r=rgb[y,x+1]
            C[y,x]=np.abs(l-r).sum()+ (60 if im[y,x]==1 else 0)
    M=C.copy(); B=np.zeros((h,w),int)
    for y in range(1,h):
        for x in range(x0,x1+1):
            if C[y,x]>=INF: continue
            best=INF; bx=-1
            for dx in(-1,0,1):
                px=x+dx
                if x0<=px<=x1 and M[y-1,px]<INF:
                    # voorwaartse energie: verspringen kost het verschil tussen de nieuwe buren in de rij erboven
                    extra=0 if dx==0 else np.abs(rgb[y-1,x]-rgb[y,x-dx]).sum()*0.5
                    if M[y-1,px]+extra<best: best=M[y-1,px]+extra; bx=px
            if bx>=0: M[y,x]=C[y,x]+best; B[y,x]=bx
            else: M[y,x]=INF
    x=int(np.argmin(M[h-1,x0:x1+1]))+x0
    if M[h-1,x]>=INF:
        dood=[y for y in range(h) if (M[y,x0:x1+1]>=INF).all()]
        raise SystemExit('geen naad mogelijk, eerste dode rij %d (band %d-%d)'%(dood[0],x0,x1))
    pad=[x]
    for y in range(h-1,0,-1): x=B[y,x]; pad.append(x)
    return pad[::-1]
def weg(im,verb,pad):
    return (np.array([np.delete(im[y],pad[y]) for y in range(im.shape[0])]),
            np.array([np.delete(verb[y],pad[y]) for y in range(im.shape[0])]))
def maak(nA,nB,naam):
    im=base.copy(); vb=verboden.copy(); naden=[]
    # yerba-vak: alleen pixels in de vakrij-zone (rand recht) mogen; zilver/groen daar wel toegestaan (vak korter)
    for k in range(nB):
        vy=vb.copy(); vy[:, :19]=True; vy[:, 26-k:]=True
        for y in range(H):
            for x in range(19,26-k):
                if 16<=y<=29: vy[y,x]=False   # het vak zelf (rand, yerba, lijnen ervan) en de rij eronder
        p=naad(im,19,25-k,vy); naden.append(('vak',p)); im,vb=weg(im,vb,p)
    sh=nB
    for k in range(nA):
        x0,x1=49-sh,W-2-sh-k
        va=vb.copy(); va[:, :x0]=True; va[:, x1+1:]=True
        p=naad(im,x0,x1,va); naden.append(('romp',p)); im,vb=weg(im,vb,p)
    assert im.shape==(48,64)
    full=np.zeros((64,64),int); full[15:63,:]=im
    o=Image.fromarray(full.astype('uint8'),'P'); o.putpalette(r4.getpalette()); o.save(D+'r5/'+naam,transparency=0)
    return naden
for nm,(na,nb) in {'mate2_A.png':(8,0),'mate2_B.png':(6,2)}.items():
    nd=maak(na,nb,nm)
    print(nm)
    for soort,p in nd: print('  naad',soort,'x per rij (lokaal, na eerdere naden):',min(p),'-',max(p),p)

# controle bevroren delen
a4s=a4[15:63]
for nm in ('mate2_A.png','mate2_B.png'):
    s_=np.asarray(Image.open(D+'r5/'+nm)).astype(int)[15:63]
    print(nm,'gelijk aan r4 links van lokaal 49 (A) / 19 (B):',(s_[:,:49]==a4s[:,:49]).all() if nm.endswith('A.png') else (s_[:,:19]==a4s[:,:19]).all())
sB=np.asarray(Image.open(D+'r5/mate2_B.png')).astype(int)[15:63]
print('B: ventje/bombilla (r4 lokaal 26-48) 2 px naar links verschoven gelijk:',(sB[:,24:47]==a4s[:,26:49]).all())

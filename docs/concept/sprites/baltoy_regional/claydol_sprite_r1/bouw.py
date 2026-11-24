# Claydol-regional r1: samengesteld model -> schrappen -> technisch opschonen. Niets getekend; elke stap telt zijn pixels.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'claydol_sprite_r1'); from klassen import klasse, PAL
RIJEN=[16,25,27,44,52,59,63,74,79]          # natieve rijen die vervallen
KOLOMMEN=[15,19,32,52,60,64,68,72,80]      # natieve kolommen die vervallen
k,a=klasse()
kk=np.delete(np.delete(k,RIJEN,0),KOLOMMEN,1); ys,xs=np.where(kk>0); kk=kk[ys.min():ys.max()+1,xs.min():xs.max()+1]
h,w=kk.shape; S=np.zeros((64,64),int); oy=64-h; ox=(64-w)//2; S[oy:oy+h,ox:ox+w]=kk
kaal=S.copy(); np.save('claydol_sprite_r1/kaal.npy',kaal)
G={2:'L',3:'L',4:'L',5:'M',6:'M',7:'M',8:'D',9:'D',10:'K',11:'R',12:'R',13:'R'}
def buren(S,y,x):
    return [S[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if 0<=y+dy<64 and 0<=x+dx<64]
log={}
# A) ruis: losse pixel (geen enkele 4-buur met dezelfde index) binnen een vlak van dezelfde kleurgroep -> meest voorkomende buurtint uit die groep
T=S.copy()
for y in range(64):
    for x in range(64):
        v=S[y,x]
        if v==0 or G[v] in 'KR': continue
        b=[u for u in buren(S,y,x) if u>0]
        if v in b: continue
        zg=[u for u in b if G[u]==G[v]]
        if len(zg)>=3:
            vals,c=np.unique(zg,return_counts=True); T[y,x]=vals[c.argmax()]; log.setdefault('ruis',[]).append((x,y,v,T[y,x]))
S=T
# B) buitenlijn: elke pixel die aan transparant grenst moet omlijning zijn (geen lichte kleur op de buitenrand)
T=S.copy()
for y in range(64):
    for x in range(64):
        v=S[y,x]
        if v==0: continue
        rand=[(dy,dx) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if not(0<=y+dy<64 and 0<=x+dx<64) or S[y+dy,x+dx]==0]
        if not rand: continue
        boven_links=all(d in ((-1,0),(0,-1)) for d in rand)
        doel=7 if boven_links else 10            # gekleurde selout aan de lichtkant (zoals Baltoy r19: 6/7), zwart aan de schaduwkant
        if G[v]=='R': doel=13
        if v!=doel and (v in (8,9,10) or G[v] in 'LM' or v==7):
            if boven_links and v in (8,9): continue   # donkere modelpixel boven/links laten (vorm-schaduw)
            T[y,x]=doel; log.setdefault('buitenlijn',[]).append((x,y,v,doel))
S=T
np.save('claydol_sprite_r1/sprite.npy',S)
im=Image.fromarray(S.astype('uint8'),'P'); pal=[c for p in PAL for c in p]; pal+= [0]*(48-len(pal)); im.putpalette(pal)
im.save('claydol_sprite_r1/claydol_r1.png',transparency=0)
for n,l in log.items(): print(n,len(l))
print('kleuren',sorted(set(S.ravel())),'formaat figuur',w,h,'offset',ox,oy)

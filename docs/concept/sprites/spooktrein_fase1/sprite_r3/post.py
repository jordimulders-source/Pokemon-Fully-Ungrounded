# Stap 4: technisch opschonen (sprite-niveau). Middenzone: tintvlekjes < MINC px en korte losse lijnstukjes (< LMIN px,
# niet vast aan de buitenlijn) nemen de meest voorkomende buurtint aan (zelfde kleurgroep) -> minder, grotere stukken.
# Wiel: alleen vlekjes < 3 px. Buitenrand, schoorsteen, rail: bevroren.
import sys,numpy as np
WCL=False
MINC=int(sys.argv[1]) if len(sys.argv)>1 else 6; LMIN=int(sys.argv[2]) if len(sys.argv)>2 else 5
out=np.load('basis.npy'); WZ,SZ,RZ,MZ=np.load('z64.npy')
G=lambda v:0 if v==0 else (3 if v==1 else (1 if v<=6 else (4 if v==11 else 2)))
fgm=out>0; pad=np.pad(fgm,1); edge=fgm&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
N4=((1,0),(-1,0),(0,1),(0,-1)); N8=[(a,b) for a in (-1,0,1) for b in (-1,0,1) if a or b]
def comps(mask,val,nbrs):
    seen=np.zeros((64,64),bool); res=[]
    for y,x in zip(*np.where(mask)):
        if seen[y,x]: continue
        v=out[y,x]; comp=[(y,x)]; seen[y,x]=True; i=0
        while i<len(comp):
            cy,cx=comp[i]; i+=1
            for dy,dx in nbrs:
                ny,nx=cy+dy,cx+dx
                if 0<=ny<64 and 0<=nx<64 and val(out[ny,nx],v) and not seen[ny,nx]: seen[ny,nx]=True; comp.append((ny,nx))
        res.append(comp)
    return res
def fill(comp,v):
    nb=[out[cy+dy,cx+dx] for cy,cx in comp for dy,dx in N4 if out[cy+dy,cx+dx]>1 and out[cy+dy,cx+dx]!=v and (v==1 or G(out[cy+dy,cx+dx])==G(v))]
    if not nb: nb=[out[cy+dy,cx+dx] for cy,cx in comp for dy,dx in N4 if out[cy+dy,cx+dx]>1 and out[cy+dy,cx+dx]!=v]
    if not nb: return 0
    u,c=np.unique(nb,return_counts=True)
    for cy,cx in comp: out[cy,cx]=u[c.argmax()]
    return len(comp)
ch={'lijn':0,'vlek_mid':0,'vlek_wiel':0}
for it in range(3):
    for comp in comps(MZ&(out==1)&~edge,lambda a,b:a==1,N8):
        if len(comp)<LMIN and not any(edge[cy+dy,cx+dx] for cy,cx in comp for dy,dx in N8): ch['lijn']+=fill(comp,1)
    for comp in comps(MZ&(out>1)&~edge,lambda a,b:a==b,N4):
        if out[comp[0]] in (2,7) and len(comp)>=3: continue
        if len(comp)<MINC and all(MZ[p] for p in comp): ch['vlek_mid']+=fill(comp,out[comp[0]])
    for comp in comps(WZ&(out>1)&~edge,lambda a,b:a==b,N4):
        if WCL and len(comp)<3 and all(WZ[p] for p in comp): ch['vlek_wiel']+=fill(comp,out[comp[0]])
print('opgeschoonde px',ch)
np.save('post.npy',out)

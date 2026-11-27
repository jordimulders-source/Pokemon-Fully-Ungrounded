# puntig.py (exec vanuit bouw.py, alleen versie B): elke achterpunt puntiger BINNEN zijn eigen modelsilhouet.
# Per punt: as = juweelmidden -> zwaartepunt van de punt (richting van het model); tip = de silhouetpixel met de grootste
# lengte langs de as (bij gelijke lengte de pixel het dichtst bij de as); voet = de twee uiterste pixels (loodrecht op de as)
# die aan de voorste ster grenzen. Alles buiten de twee zijden tip-voet wordt weggehaald (transparant); geen pixel erbij.
# Kleur: facet aan de kant naar linksboven = koek midden, andere facet = oranje (zoals de licht/donker-vlakken van de
# Gen 3 Starmie); chips uit het model die blijven staan, blijven.
GEMC=np.array([31.0,30.0]); PUNTWEG={}; PUNTINFO={}
lbP,nP=label(BM&~fm)
for i in range(1,nP+1):
    P=np.argwhere(lbP==i)
    if len(P)<10: continue
    pts=P[:,::-1].astype(float)+0.5          # (x,y) pixelmiddens
    c=pts.mean(0); ax=(c-GEMC)/np.linalg.norm(c-GEMC); pe=np.array([-ax[1],ax[0]])
    d=pts-GEMC; t=d@ax; s=d@pe
    tmax=t.max(); kand=np.where(t>=tmax-0.5)[0]; tip=pts[kand[np.argmin(np.abs(s[kand]-s.mean()))]]
    voet=[j for j,(y,x) in enumerate(P) if any(fm[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))]
    sv=s[voet]; A=pts[voet][np.argmin(sv)]; Bv=pts[voet][np.argmax(sv)]
    def kant(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    tri=[tip,A,Bv]; sg=np.sign(kant(*tri))
    nm=('links' if c[0]<31 else 'rechts')+('boven' if c[1]<30 else 'onder')
    weg=0; tol=0.5*1.0
    licht_s=1 if pe@np.array([-1,-1])>0 else -1
    stip=(tip-GEMC)@pe
    for (y,x),p in zip(P,pts):
        binnen=all(sg*kant(tri[k],tri[(k+1)%3],p)/np.linalg.norm(tri[(k+1)%3]-tri[k])>=-tol for k in (0,2))   # alleen de twee zijden tip-voet; de voetlijn snijdt niet
        if not binnen:
            zet(x,y,0,'puntig weg'); weg+=1; continue
        if o[y,x]==CHOC: continue
        # facet: kant van de lijn voetmidden -> tip
        m=(A+Bv)/2; side=np.sign(kant(m,tip,p))*np.sign(kant(m,tip,m+pe*licht_s))
        zet(x,y,5 if side>0 else 4,'puntig facet')
    PUNTWEG[nm]=weg; PUNTINFO[nm]=dict(tip=tuple(tip-0.5),voet=(tuple(A-0.5),tuple(Bv-0.5)),richting=round(float(np.degrees(np.arctan2(-ax[1],ax[0]))),1),lengte=round(float(tmax),1),px=len(P))
BM=BM&(o>0)
print('puntig: weg per punt',PUNTWEG); print('puntig: punten',PUNTINFO)

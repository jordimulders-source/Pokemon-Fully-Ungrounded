# hulpmiddel ronde 6: per onderdeel een bolnormaal -> lichtwaarde -> harde drempels (alleen als SCHETS voor het tekstraster;
# daarna met de hand bijgewerkt). Geen middeling: elke pixel krijgt één paletkleur.
import numpy as np
yy,xx=np.mgrid[0:64,0:64]
LD=np.array([-0.55,-0.65,0.52]); LD/=np.linalg.norm(LD)
def licht(cx,cy,rx,ry):
    u=(xx+0.5-cx)/rx; v=(yy+0.5-cy)/ry; r2=np.clip(u*u+v*v,0,0.98)
    n=np.stack([u,v,np.sqrt(1-r2)]); return (n*LD[:,None,None]).sum(0)
def tint(L,drempels):
    """drempels: lijst (grens,tint) van licht naar donker; laatste tint voor alles daaronder"""
    T=np.full(L.shape,drempels[-1][1])
    for g,t in reversed(drempels[:-1]): T[L>=g]=t
    return T

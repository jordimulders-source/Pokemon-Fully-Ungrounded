# meet.py: tentakelrichtingen en -punten van de voorste anemonen (VL, VR) in het model (natief), voor r8.
# Licht (R3) per hoekvak rond het mondje; pieken = tentakels; punt = verste lichte pixel in dat vak (natief),
# omgerekend naar spritecoordinaten. Alleen meten, niets tekenen.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; from anemonen import *; from gemeen import *
a,c,L=klassen(); H,W=c.shape
def meet(i, rmin=4.0, bins=72, tmin=None):
    cx,cy=MOND[i][0],MOND[i][1]
    vs,us=np.where(c==5)
    own=np.array([eigenaar(u+.5,v+.5) for u,v in zip(us,vs)])
    m=(own==i)
    us,vs=us[m],vs[m]
    t=np.arctan2(vs+.5-cy,us+.5-cx); r=np.hypot(us+.5-cx,vs+.5-cy)
    k=r>rmin+0*MOND[i][2]
    k&=~np.array([in_mond(i,u+.5,v+.5,0.8) for u,v in zip(us,vs)])
    t,r,us,vs=t[k],r[k],us[k],vs[k]
    h=np.histogram(t,bins=bins,range=(-np.pi,np.pi))[0].astype(float)
    hs=np.array([h[(j-1)%bins]+2*h[j]+h[(j+1)%bins] for j in range(bins)])/4
    pk=[j for j in range(bins) if hs[j]>=hs[(j-1)%bins] and hs[j]>hs[(j+1)%bins] and hs[j]>=2]
    out=[]
    for j in pk:
        tm=-np.pi+(j+.5)*2*np.pi/bins; w=np.abs((t-tm+np.pi)%(2*np.pi)-np.pi)<2*np.pi/bins*1.5
        if w.sum()<3: continue
        q=np.argmax(r[w]); u,v=us[w][q],vs[w][q]
        out.append((round(np.degrees(tm)),round(float(hs[j]),1),round(float(r[w].max()),1),round(X0+(u+.5-U0)*S,1),round(Y0+(v+.5-V0)*S,1)))
    return out
if __name__=='__main__':
    for i in (0,1):
        res=meet(i); print(AN[i][0],len(res))
        for x in res: print('  hoek %4d  gewicht %5.1f  r_nat %5.1f  punt sprite (%5.1f,%5.1f)'%x)

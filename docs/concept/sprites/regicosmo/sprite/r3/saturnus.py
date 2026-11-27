# Saturnus r2: ronde bol + schuine elliptische ring, beide gemeten in het natieve model (zie meet()); geen vorm verzonnen.
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from scipy import ndimage; import gemeen as g, kaal as kl
a,deel,dot=g.natief(); C=kl.C
SAT=deel==2; RING=SAT&np.isin(C,[1,6,13,11]); PLAN=SAT&~RING
def meet():
    # bol: cirkelfit (kleinste kwadraten) op de planeetpixels die aan de achtergrond grenzen
    e=PLAN&ndimage.binary_dilation(deel<0,np.ones((3,3)))
    yy,xx=np.where(e); xx=xx+0.5; yy=yy+0.5
    A=np.c_[2*xx,2*yy,np.ones(len(xx))]; cx,cy,c=np.linalg.lstsq(A,xx**2+yy**2,rcond=None)[0]; r=np.sqrt(c+cx**2+cy**2)
    # ring: de twee uiterste ringpunten (punt links-onder, punt rechts-boven) geven as, kanteling en halve lengte;
    # de halve korte as = afstand van het ringmidden voor de bol (grijze middenlijn onder het centrum) tot de lange as.
    ys,xs=np.where(RING); P=np.c_[xs+0.5,ys+0.5]
    d=P[:,0]-P[:,1]*0.5          # ruwe richting langs de lange as
    L=P[np.argmin(d)]; R=P[np.argmax(d)]
    ce=(L+R)/2; v=R-L; ang=np.arctan2(v[1],v[0]); amaj=np.hypot(*v)/2
    gr=np.where(SAT&np.isin(C,[13,11])); G=np.c_[gr[1]+0.5,gr[0]+0.5]-ce
    u=G[:,0]*np.cos(ang)+G[:,1]*np.sin(ang); w=-G[:,0]*np.sin(ang)+G[:,1]*np.cos(ang)
    voor=(np.abs(u)<3)&(w>0)    # grijze middenlijn recht onder/voor het centrum
    bmin=np.median(w[voor])
    return (cx,cy,r),(ce,ang,amaj,bmin),(L,R)
def naar(xn,yn): return kl.OX+(xn-kl.X0)*kl.s, kl.OY+(yn-kl.Y0)*kl.s   # continue coordinaten (randen)
if __name__=='__main__':
    (cx,cy,r),(ce,ang,amaj,bmin),(L,R)=meet()
    print('bol natief c=(%.2f,%.2f) r=%.2f -> sprite c=(%.2f,%.2f) r=%.2f'%(cx,cy,r,*naar(cx,cy),r*kl.s))
    print('ring natief punten L',L,'R',R,'centrum',ce.round(2),'hoek %.1f gr'%np.degrees(ang),'a=%.2f b=%.2f -> sprite a=%.2f b=%.2f centrum (%.2f,%.2f)'%(amaj,bmin,amaj*kl.s,bmin*kl.s,*naar(*ce)))

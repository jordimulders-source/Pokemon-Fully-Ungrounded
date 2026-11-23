# reductie_ice.py: de gedeelde reductie (reductie_gedeeld.py, ongewijzigde geometrie P=8,1, zelfde verschuiving/uitsnede) met het
# Ice-figuurmasker (masker.py) i.p.v. "achtergrond = min(R,G,B) >= 235" (ijswit is zelf >= 235). Gebruik: python3 reductie_ice.py
import numpy as np; from PIL import Image
from reductie_gedeeld import bron, DREMPEL
from masker import masker
MODEL='../r3/gemini_r3_lijf.png'
def reduceer_m(a,fg):
    gem=np.zeros((64,64,3)); dek=np.zeros((64,64))
    for Y in range(64):
        for X in range(64):
            acc=np.zeros(3); tw=0; fw=0
            for u,v,w in bron(X,Y,a.shape[1],a.shape[0]):
                tw+=w
                if fg[v,u]: acc+=w*a[v,u]; fw+=w
            if tw: dek[Y,X]=fw/tw
            if fw: gem[Y,X]=acc/fw
    return gem,dek
def laad():
    a,fg=masker(MODEL); return a.astype(float),fg
if __name__=='__main__':
    a,fg=laad(); gem,dek=reduceer_m(a,fg); m=dek>=DREMPEL
    yy,xx=np.where(m); print('Ice kale reductie: figuur x%d-%d y%d-%d, %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),m.sum()))
    r=np.asarray(Image.open('../../gnometrotter_rock/sprite/kaal.png'))>0; print('Rock kaal %d px; verschil silhouet %d px'%(r.sum(),(r^m).sum()))

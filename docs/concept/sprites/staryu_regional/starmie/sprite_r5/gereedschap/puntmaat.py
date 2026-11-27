# puntmaat.py: meet punten (tiphoek, breedte op d px van de tip, lengte/voet) op Gen 3 Starmie en op de sprite.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import laad_g3, punt_van
def maat(mask, kern, rest=None):
    """mask: pixels van een punt; kern: (x,y) middelpunt. Breedte loodrecht op de as kern->tip."""
    ys,xs=np.where(mask); p=np.stack([xs+0.5,ys+0.5],1); c=np.array(kern)
    d=np.hypot(*(p-c).T); tip=p[np.argmax(d)]; ax=(tip-c)/np.linalg.norm(tip-c); pe=np.array([-ax[1],ax[0]])
    t=(p-c)@ax; s=(p-c)@pe; T=t.max(); out={}
    for k in (1,2,3,4,6,8):
        m=(t>T-k-0.5)&(t<=T-k+0.5)
        out[k]=round(float(s[m].max()-s[m].min()+1),1) if m.any() else 0
    # tiphoek uit de breedte op 2 en 6 px
    hoek=np.degrees(2*np.arctan((out[6]-out[2])/2/4)) if out[6] and out[2] else 0
    return out,round(float(hoek),0),round(float(T),1)
if __name__=='__main__':
    g,_=laad_g3(); C=(31.5,30.0)
    lab=np.full((64,64),'',object)
    for y,x in zip(*np.where(g>0)): lab[y,x]=punt_van(x,y)
    for n in ('tl','tr','rl','b','ll','top','r','br','bl','l'):
        m=(lab==n)&np.isin(g,[1,2,3,4,14])
        w,h,T=maat(m,C); print('Gen3',n,'breedte op d px van de tip',w,'tiphoek ±%d°'%h)

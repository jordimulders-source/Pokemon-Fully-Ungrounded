# Samengesteld natief model -> paletindex (dichtstbijzijnde kleur uit het palet van de regionale Baltoy r19, zelfde lijn).
# 0 = transparant (achtergrond: min(RGB) >= 225 en verbonden met de rand).
import numpy as np; from PIL import Image
PAL=[(255,255,255),(246,240,222),(230,222,198),(212,202,176),(196,186,162),(178,168,146),(154,145,128),(128,120,110),
     (104,97,92),(80,72,70),(40,32,36),(240,140,124),(220,90,86),(166,52,60)]
def klasse(pad='claydol_model/model_natief_samengesteld.png'):
    a=np.asarray(Image.open(pad).convert('RGB')).astype(int); H,W=a.shape[:2]
    P=np.array(PAL); d=((a[:,:,None]-P[None,None,1:])**2).sum(3); k=d.argmin(2)+1
    bg=a.min(2)>=225
    # achtergrond = vloedvulling vanaf de rand door bg-pixels
    vis=np.zeros((H,W),bool); st=[(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)]
    while st:
        y,x=st.pop()
        if 0<=y<H and 0<=x<W and not vis[y,x] and bg[y,x]:
            vis[y,x]=True; st+= [(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    k[vis]=0; return k,a
if __name__=='__main__':
    k,a=klasse(); print(np.bincount(k.ravel(),minlength=14))
    ys,xs=np.where(k>0); print('bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max())

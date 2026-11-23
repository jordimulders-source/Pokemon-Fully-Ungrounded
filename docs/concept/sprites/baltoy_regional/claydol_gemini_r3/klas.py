# Natief model r3 -> paletindex. Palet = Baltoy r19 (zelfde lijn). Steen: per modeltoon (drempels tussen de k-means-niveaus); rood: dichtstbijzijnde roodkleur.
import numpy as np; from PIL import Image
PAL=[(255,255,255),(246,240,222),(230,222,198),(212,202,176),(196,186,162),(178,168,146),(154,145,128),(128,120,110),
     (104,97,92),(80,72,70),(40,32,36),(240,140,124),(220,90,86),(166,52,60)]
LUM=lambda c:np.asarray(c)@[0.299,0.587,0.114]
def klasse(pad='natief.png',verschuif=0):
    a=np.asarray(Image.open(pad).convert('RGB')).astype(int); H,W=a.shape[:2]
    L=LUM(a)+verschuif; P=np.array(PAL)
    # modeltonen (1D k-means op het model: 2 / 80 / 106 / 132 / 158 / 176 / 190 / 212) -> één paletindex per modeltoon; de 106-tussentoon (antialias) gaat grotendeels naar het vlak (7), drempel 105
    st=np.select([L<45,L<105,L<146,L<167,L<184,L<200],[10,8,7,6,5,4],2)
    red=(a[:,:,0]-a[:,:,1]>45)
    rd=((a[:,:,None]-P[None,None,11:14])**2).sum(3).argmin(2)+11
    k=np.where(red,rd,st)
    bg=a.min(2)>=225
    vis=np.zeros((H,W),bool); s=[(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)]
    while s:
        y,x=s.pop()
        if 0<=y<H and 0<=x<W and not vis[y,x] and bg[y,x]:
            vis[y,x]=True; s+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    k[vis]=0; return k,a
SYM='.123456789KrRD'
def dump(k,y0=0,x0=0):
    print('    '+''.join(str((x+x0)%10) for x in range(k.shape[1])))
    for y in range(k.shape[0]): print('%3d '%(y+y0)+''.join(SYM[v] for v in k[y]))
if __name__=='__main__':
    import sys; v=float(sys.argv[1]) if len(sys.argv)>1 else 0
    k,a=klasse(verschuif=v); print(np.bincount(k.ravel(),minlength=14)); dump(k[10:86,11:88],10,11)

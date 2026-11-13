# onderlaag: meting -> letters (alleen basis; daarna handwerk in zones).
# Lijn = fractie zwart (L<20) + fractie donkerpaars (model-selout) >= T; letter o of d naar wat overheerst. Silhouetrand altijd o of d.
# Zwart materiaal (model L 20-50 basis, 50-95 licht) -> m basis, d licht (zoals de charlatan-Alakazam; k = schaduw, met de hand).
import numpy as np,sys
d=np.load('meet.npz'); cov,fo,fk,fw,fr,fd,med,sil=[d[k] for k in('cov','fo','fk','fw','fr','fd','med','sil')]
T=float(sys.argv[1]) if len(sys.argv)>1 else .34
pad=np.pad(sil,1)
edge=sil&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
C=np.load('cellen.npy')
out=[]
for y in range(64):
    r=''
    for x in range(64):
        if not sil[y,x]: r+='.'; continue
        c=cov[y,x]; o_,k_,w_,d_,r_=fo[y,x]/c,fk[y,x]/c,fw[y,x]/c,fd[y,x]/c,fr[y,x]/c
        l=med[y,x].mean()
        if r_>=.4: r+='r'
        elif k_>=.5: r+='o' if (edge[y,x] and o_>=.2) else ('m' if l<50 else 'n')
        elif o_+d_>=T and w_<.6 or (edge[y,x] and w_<.5): r+='o' if o_>=d_ else 'd'
        elif w_>=.5: r+='w'
        elif o_+k_>=.6: r+='o' if o_>k_ else 'm'
        elif l>=176: r+='a'      # model licht (187) -> a
        elif l>=125: r+='b'      # model middentoon (148) -> b; c = schaduw, met de hand (zoals de charlatan-Alakazam: lijf b, schaduw c)
        else: r+='c'
    out.append(r)
open('onderlaag.txt','w').write('\n'.join(out)+'\n'); print('\n'.join('%2d '%i+l for i,l in enumerate(out)))

# Bewaakt r6 t.o.v. r5: silhouet gelijk; meldt buitenrand- en patroonwijzigingen (positie), kleurtelling, helderheidsstappen.
import numpy as np, sys
r5=np.load('welp_r5.npy'); a=np.load('welp_r6.npy'); F=np.load('FIN6.npy'); edge=np.load('edge.npy'); H,W=a.shape
CH='.KdSMLPQRgWCTGH'
sil=int(((a>0)!=(r5>0)).sum())
ed=[(x,y,CH[r5[y,x]],CH[a[y,x]]) for y in range(H) for x in range(W) if edge[y,x] and a[y,x]!=r5[y,x]]
pat=lambda z: np.isin(z,[6,7,8,11])  # lila + creme (lijfpatronen)
kop=np.zeros((H,W),bool); kop[0:24,0:26]=True
pm_lijf=[(x,y,CH[r5[y,x]],CH[a[y,x]]) for y in range(H) for x in range(W) if not kop[y,x] and pat(a)[y,x]!=pat(r5)[y,x]]
fig=(a>0).sum(); n=len(set(a.ravel()))
L=lambda i: 0.299*F[i][0]+0.587*F[i][1]+0.114*F[i][2]
print('silhouet-diff:',sil)
print('buitenrand gewijzigd:',ed)
print('patroon (lila/creme) buiten de kop gewijzigd:',pm_lijf)
print('kleuren incl. transparant:',n,'| zwart %.1f%% lijnbruin %.1f%%'%(100*(a==1).sum()/fig,100*(a==2).sum()/fig))
print('bruin d/S/M/L/H helderheid:',[round(L(i)) for i in (2,3,4,5,14)],'stappen',[round(L(j)-L(i)) for i,j in ((2,3),(3,4),(4,5),(5,14))])
print('aandeel S/M/L/H: ',{CH[i]:round(100*(a==i).sum()/fig,1) for i in (3,4,5,14)},' r5:',{CH[i]:round(100*(r5==i).sum()/fig,1) for i in (3,4,5)})
sys.exit(0 if sil==0 and n<=16 else 1)

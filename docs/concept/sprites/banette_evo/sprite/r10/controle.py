# Controle: kleuren, losse clusters, zwarte pixels los in een vlak, gaten, buitenlijn
import sys,numpy as np; from scipy import ndimage as nd
g=np.load(sys.argv[1]) if sys.argv[1].endswith('.npy') else np.array(__import__('PIL.Image',fromlist=['Image']).open(sys.argv[1]))
print('kleuren gebruikt:',sorted(set(g.ravel())),'aantal incl. transparant:',len(set(g.ravel())))
fig=g>0
# gaten: transparante componenten die de rand niet raken
lab,n=nd.label(~fig)
rand=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1])
gaten=[(k,int((lab==k).sum()),tuple(np.argwhere(lab==k)[0][::-1])) for k in range(1,n+1) if k not in rand]
print('ingesloten transparante gebieden (x,y van eerste pixel):',[(s,p) for k,s,p in gaten])
# buitenlijn: figuurpixels die aan transparant grenzen moeten omlijning zijn
OMLIJN={1,4,7,14,12,13}   # 13 = touwtjes (1 px lijnen)
P=np.pad(fig,1); edge=fig&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
bad=[(i,j,int(g[j,i])) for j,i in zip(*np.where(edge)) if g[j,i] not in OMLIJN]
print('randpixels zonder omlijningskleur:',len(bad),bad[:40])
# kleine clusters per kleur (4-buren), behalve zwart/draad
small=[]
for c in set(g.ravel())-{0}:
    lab,n=nd.label(g==c,structure=np.ones((3,3)))
    for k in range(1,n+1):
        s=(lab==k).sum()
        if s<3:
            j,i=np.argwhere(lab==k)[0]; small.append((int(i),int(j),int(c),int(s)))
print('clusters < 3 px (x,y,kleur,grootte):',len(small)); print(small)
# zwart dat nergens aan transparant of aan andere zwarte pixel grenst (los in een vlak)
k1=(g==1); lab,n=nd.label(k1,structure=np.ones((3,3)))
los=[]
for k in range(1,n+1):
    m=lab==k; dm=nd.binary_dilation(m,structure=np.ones((3,3)))
    if not (dm&~fig).any() and m.sum()<4: los.append((tuple(np.argwhere(m)[0][::-1]),int(m.sum())))
print('losse zwarte groepjes < 4 px midden in een vlak:',los)

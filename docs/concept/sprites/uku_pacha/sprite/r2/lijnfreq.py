# Lijnfrequentie meten: binnenlijnen (donkerste tinten, niet aan de buitenrand) en de lengte van de
# vlakstukken ertussen langs rijen en kolommen (alleen stukken die aan beide kanten door een
# binnenlijn begrensd zijn). Arbok (Gen 3, anim_front_gba.png bovenste 64x64) vs Uku Pacha r2.
import numpy as np, sys
from PIL import Image
def meet(A, lijn, naam):
    H,W=A.shape; inn=A>=0
    def rand(y,x): return any(not(0<=y+b<H and 0<=x+a<W) or not inn[y+b,x+a] for a,b in ((0,1),(0,-1),(1,0),(-1,0)))
    L=np.zeros_like(inn)
    for y in range(H):
        for x in range(W):
            if inn[y,x] and lijn(A[y,x]) and not rand(y,x): L[y,x]=True
    gaps=[]
    for M in (L, L.T):
        I=inn if M is L else inn.T
        for r in range(M.shape[0]):
            x=0
            while x<M.shape[1]:
                if M[r,x]:
                    x2=x+1
                    while x2<M.shape[1] and I[r,x2] and not M[r,x2]: x2+=1
                    if x2<M.shape[1] and M[r,x2] and x2-x-1>=1: gaps.append(x2-x-1)
                    x=x2
                else: x+=1
    gaps=np.array(gaps)
    print(f'{naam}: binnenlijnpx {L.sum()} van {inn.sum()} ({100*L.sum()/inn.sum():.0f}%), '
          f'vlakstuk tussen lijnen: mediaan {np.median(gaps):.1f}, gemiddeld {gaps.mean():.1f} px (n={len(gaps)})')
    return L
im=Image.open('../../../../../../graphics/pokemon/arbok/anim_front_gba.png'); a=np.array(im)[:64].astype(int); a[a==0]=-1
pal=np.array(im.getpalette()[:48]).reshape(16,3); lum=pal.mean(1)
meet(a, lambda v: v in (8,12), 'Arbok (lijnen = zwart 8 + donkerpaars 12)')
import raster2png
R=raster2png.lees('raster_af.txt'); b=np.array([[-1 if c=='.' else 'KnD'.find(c) if c in 'Kn' else 5 for c in r] for r in R])
meet(b, lambda v: v in (0,1), 'Uku Pacha r2')

# Variant B2: verre poot + ski dichter naar de nabije ski (vooral omlaag).
# Rechte verschuiving omlaag botst meteen met de opgebogen punt van de nabije ski (kolom 25-27), dus:
#  - been (rij 41-45): rij 44 verdubbeld (modelpixels uit A) -> been 1 px langer, dij-aansluiting (rij 41-43) onaangeroerd
#  - ski (rij >= 46): kolomgewijs omlaag, dy(x) = 1 + round(K*(x-PIV)): bij de voet 1 px, staart verder omlaag, punt iets omhoog
#    (= lichte draaiing om de voet, zodat de ski's evenwijdiger worden en de wig ertussen smaller)
import sys, numpy as np; from PIL import Image
sys.argv=[sys.argv[0]]+sys.argv[1:]
K=float(sys.argv[1]) if len(sys.argv)>1 else 0.2; PIV=int(sys.argv[2]) if len(sys.argv)>2 else 25; DX=int(sys.argv[3]) if len(sys.argv)>3 else 0
A=np.loadtxt('A.txt',dtype=int); m=np.load('poot_masker.npy'); H,W=A.shape
# werk op canvas 64 breed (raster kolom c -> canvas c+1) zodat de punt 1 px links mag
CA=np.zeros((64,64),int); CA[3:,1:62]=A; M=np.zeros((64,64),bool); M[3:,1:62]=m
B2=CA.copy(); B2[M]=0
dy=lambda x: 1+int(np.floor(K*(x-1-PIV)+0.5))
for y,x in zip(*np.where(M)):
    r=y-3
    if r<=43: B2[y,x]=CA[y,x]
    elif r==44: B2[y,x]=CA[y,x]; B2[y+1,x]=CA[y,x]        # verdubbelde beenrij
    elif r==45: B2[y+1,x]=CA[y,x]
    else:
        ny=y+dy(x)
        if B2[ny,x+DX]!=0 and not M[ny,x+DX] and CA[ny,x+DX]!=0: print('botsing',ny,x)
        B2[ny,x+DX]=CA[y,x]
# controle: buiten de verre poot (oud en nieuw) niets veranderd
nieuw=(B2!=0)&(CA==0) | (B2!=CA)
d=np.argwhere(B2!=CA); buiten=[(y,x) for y,x in d if not M[y,x] and CA[y,x]!=0]
print('diff',len(d),'waarvan op pixels van de rest van de sprite:',len(buiten))
np.savetxt('B2.txt',B2,fmt='%d')
# tussenruimte meten (verticaal, kolommen waar de nabije ski onder de verre ligt) + vrije afstand (Chebyshev-1)
near=(CA>0)&~M; near[:44]=False
far=(B2>0)&~((CA>0)&~M)  # alles van B2 dat niet de rest is
far[:44]=False
def meet(F):
    fy,fx=np.where(F); ny,nx=np.where(near)
    D=np.maximum(np.abs(fy[:,None]-ny[None]),np.abs(fx[:,None]-nx[None])).min()-1
    g=[]
    for x in range(64):
        a=fy[fx==x]; b=ny[nx==x]
        if len(a) and len(b):
            bb=b[b>a.max()]
            if len(bb): g.append(int(bb.min()-a.max()-1))
    return D,g
Mf=M.copy(); Mf[:47]=False
print('A : vrij %d gaten %s gem %.1f'%(meet(Mf)[0],meet(Mf)[1],np.mean(meet(Mf)[1])))
Ff=far.copy(); Ff[:47]=False
D,g=meet(Ff); print('B2: vrij %d gaten %s gem %.1f'%(D,g,np.mean(g)))
PAL=[tuple(map(int,l.split())) for l in open('normal.pal').read().split('\n')[3:19]]
im=Image.fromarray(B2.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]); im.save('skinguin_B2.png',transparency=0,bits=4)
im=Image.open('skinguin_B2.png').convert('RGBA'); im.resize((512,512),Image.NEAREST).save('skinguin_B2_8x.png')

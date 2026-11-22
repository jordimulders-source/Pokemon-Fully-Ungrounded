# r9 basis: rollenraster van r8-P1 inlezen, armcorrectie toepassen (linker bovenarm-aanzet 1 rij omhoog).
import numpy as np; from PIL import Image
KL={'.':(0,0,0),'K':(16,14,22),'1':(30,28,44),'2':(48,46,70),'3':(76,74,108),'g':(128,126,166),
    'L':(246,236,202),'M':(228,208,158),'D':(186,156,104),'S':(126,94,54),'B':(80,120,200),'b':(44,66,140),
    'R':(214,66,58),'r':(140,36,40),'W':(248,248,248),'G':(56,160,72),'H':(40,104,56)}
INV={v:k for k,v in KL.items()}
def rollen(f):
    im=Image.open(f); pal=np.array(im.getpalette()[:3*16]).reshape(16,3)
    return np.array([INV.get(tuple(c),'?') for c in pal])[np.asarray(im)]
R8=rollen('../sprite_r8/astro_P1.png')
def r9_basis():
    R=R8.copy()
    # armcorrectie: bovenrand van de linker bovenarm loopt op rij 27 door tot de romp (was rij 28 met inkeping op x29)
    for x in (27,28,29): R[27,x]='K'
    for x,y in ((27,28),(28,28),(29,28),(30,27),(30,28)): R[y,x]='2'
    return R
if __name__=='__main__':
    R=r9_basis()
    print('   '+''.join(str(i%10) for i in range(64)))
    for y in range(24,50): print('%2d '%y+''.join(R[y,12:52]))

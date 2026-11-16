# Eindkeuring DFC pitahaya r8: meet tinten, contrast op vlakpixels, zwakke tintgrenzen, dambord, klonten, ruis, zwart, lijnkanten.
# Aanroep: python3 meet_dfc.py <sprite.png> [...]; refs: --ref (Gen 3, bovenste 64x64 anim_front)
import sys,os,numpy as np;from PIL import Image;from scipy import ndimage as nd
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','keuring_r7'))
from meet import meet
R='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def load(f):
    im=Image.open(f); o=np.asarray(im).astype(int)[:64,:64]
    P=np.array(im.getpalette()[:48]).reshape(-1,3); return o,P
def lum(P): return P@[.299,.587,.114]
def stats(f,zones=None):
    o,P=load(f); m=o>0; L=lum(P)
    blk=min(set(np.unique(o[m])),key=lambda i:L[i])
    # zwakke tintgrenzen: buurparen (4-buur) met andere index, beide in figuur
    pairs=[];
    for dy,dx in((0,1),(1,0)):
        a=o[:64-dy,:64-dx];b=o[dy:,dx:];mm=(a>0)&(b>0)&(a!=b)
        for i,j in zip(a[mm],b[mm]): pairs.append((i,j))
    dl=[abs(L[i]-L[j]) for i,j in pairs]; drgb=[np.linalg.norm(P[i]-P[j]) for i,j in pairs]
    weak=sum(d<20 for d in dl)/len(dl)*100; weak60=sum(d<60 for d in drgb)/len(drgb)*100
    # zwarte klonten: 2x2 zwart
    kl=[(x,y) for y in range(63) for x in range(63) if (o[y:y+2,x:x+2]==blk).all()]
    # index -> aantal en lum
    u,c=np.unique(o[m],return_counts=True)
    return dict(weak20=weak,weak60=weak60,klont2x2=kl,idx={int(i):(int(n),round(L[i])) for i,n in zip(u,c)},n_tint=len(u))
def zwak_paren(f):
    o,P=load(f);L=lum(P);from collections import Counter;C=Counter()
    for dy,dx in((0,1),(1,0)):
        a=o[:64-dy,:64-dx];b=o[dy:,dx:];mm=(a>0)&(b>0)&(a!=b)
        for i,j in zip(a[mm],b[mm]):
            if abs(L[i]-L[j])<20: C[tuple(sorted((int(i),int(j))))]+=1
    return C
if __name__=='__main__':
    fs=sys.argv[1:] or ['../af/pitahaya_draak.png']
    if '--ref' in fs: fs=[R+n+'/anim_front.png' for n in('treecko','cacnea','bagon','oddish','larvitar')]
    for f in fs:
        s=stats(f);r=meet(f)
        print('==',f)
        print('  tinten',s['n_tint'],'zwakke tintgrenzen <20lum %.1f%%  (RGB<60 %.1f%%)'%(s['weak20'],s['weak60']),'paren',dict(zwak_paren(f)))
        print('  zwart %.1f%% binnen %.1f%%  2x2-zwartklont %d %s'%(r['zwart'],r['zwart_binnen'],len(s['klont2x2']),s['klont2x2'][:30]))
        print('  dambord',len(r['dambord']),r['dambord'])
        print('  vulvlakjes<3',r['vulvlakjes'],'buiten gezicht',r['vul_buiten_gezicht'])
        print('  los zwart',r['los_zwart'],' lichtkant zwart/sel',r['lit_zwart'],r['lit_sel'],'schaduwkant zwart/sel',r['sh_zwart'],r['sh_sel'],'om-en-om',r['om_en_om'],'licht op rand',r['licht_op_rand'])

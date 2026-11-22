# r15: romp r13 bevroren. Shorts: getrapte zigzag (r14-S4-motief) in nieuwe kleuren L1/L2/L3.
# Armen: korte mouw (t-shirt) vanaf de schoudernaad; daaronder blote creme bovenarm (L/M/D, selout S, zoals de onderarm).
#  a) mouw rode shirtstof + blauw/rood/blauw-boord als mouwrand;  b) mouw = de strepen zelf (blauw, rood, rood, blauw als pols/enkel).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r14'); sys.path.insert(0,'../sprite_r9')
from r14 import R13, LEDE, stuk, tint, B, H, W, KL2, boord, zigzag
# mouw langs de arm: linkerarm per kolom (x, vanaf de naad x28 naar links), rechterarm per rij (vanaf de naad rij 31 omlaag)
MOUW={'a':{'LA':{27:'s',26:'s',25:'B',24:'R',23:'B'}, 'RA':{32:'s',33:'B',34:'R',35:'B'}},
      'b':{'LA':{27:'B',26:'R',25:'R',24:'B'},        'RA':{32:'B',33:'R',34:'R',35:'B'}}}
KLEUR={'s':('R','Q','Q'),'B':('B','B','b'),'R':('R','R','Q'),'c':('L','M','D')}
SEL={'s':'Q','B':'b','R':'Q','c':'S'}
BEEN={'L1':dict(g=('B','B','b'),m=('W','W','L'),o=('1','1','1'),sel='b'),
      'L2':dict(g=('Y','Y','D'),m=('1','1','1'),o=('1','1','1'),sel='D'),
      'L3':dict(g=('3','2','1'),m=('Y','Y','Y'),o=('Y','Y','D'),sel='1')}
def bouw(mouw,been):
    R=R13.copy(); mat={}
    for y in range(H):
        for x in range(W):
            if not LEDE[y,x]: continue
            s=stuk[y,x]
            if s=='LA': m=MOUW[mouw]['LA'].get(x,'c')
            elif s=='RA': m=MOUW[mouw]['RA'].get(y,'c')
            else:
                p=BEEN[been]; m2='o' if boord(y,x) else zigzag(s,y,x); R[y,x]=p[m2][tint[y,x]]; mat[(y,x)]=('been',None); continue
            R[y,x]=KLEUR[m][tint[y,x]]; mat[(y,x)]=('arm',m)
    for y in range(18,48):                      # selout lichtkant van mouw/blote arm/shorts
        for x in range(W):
            if B[y,x]!='K': continue
            nb=[(y,x+1),(y+1,x),(y,x-1),(y-1,x)]
            if any(stuk[a,b]=='RO' or (stuk[a,b] and not LEDE[a,b]) for a,b in nb): continue
            for a,b in ((y,x+1),(y+1,x)):
                if LEDE[a,b] and ((b==x+1 and B[y,x-1]=='.') or (a==y+1 and B[y-1,x]=='.' and x<=31)):
                    k,m=mat[(a,b)]; R[y,x]=BEEN[been]['sel'] if k=='been' else SEL[m]; break
    keys=['.']+sorted(set(R.ravel())-{'.'}); assert len(keys)<=16,keys
    out=Image.fromarray(np.vectorize(keys.index)(R).astype('uint8'),'P')
    flat=[c for k in keys for c in KL2[k]]; out.putpalette(flat+[0]*(768-len(flat))); out.save('astro_%s_%s.png'%(mouw,been),transparency=0)
    return R
if __name__=='__main__':
    for mouw in 'ab':
        for been in BEEN:
            R=bouw(mouw,been); print(mouw,been)
    for y in range(24,38): print('  %2d '%y+''.join(R[y,16:44]))

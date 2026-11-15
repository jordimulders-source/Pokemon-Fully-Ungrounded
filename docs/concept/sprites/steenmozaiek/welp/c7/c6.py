# c6: basis c5 (lijf) + c2-kop zonder lijnen; koplijnen per variant (koplijnen.py) en een rots-pass op het lijf (rots.py).
import sys, numpy as np
from PIL import Image
import koplijnen
C5=np.array(Image.open('../c5/welp_c5.png')); C2=np.array(Image.open('../c2/welp_c2.png'))
PAL5=Image.open('../c5/welp_c5.png').getpalette()[:48]; PALG=Image.open('../c5/welp_c5_grijs.png').getpalette()[:48]
P8=np.array(Image.open('../p8/welp_p8.png'))
from basis import bevroren_kop
FACE=bevroren_kop()
def kop(a,var):
    a=a.copy(); a[:32]=np.where(FACE[:32],a[:32],C2[:32])     # kop zonder lijnen (c2)
    for y,rij in koplijnen.VOORHOOFD.items():
        for x0,t in rij:
            for i,ch in enumerate(t):
                if a[y,x0+i] in (3,4,5) and not FACE[y,x0+i]: a[y,x0+i]=int(ch)
    base=a.copy(); G=np.zeros(a.shape,bool)
    for x,y in koplijnen.VAR[var]:
        assert not FACE[y,x] and base[y,x] in (3,4,5), ('geen kopvlak',x,y,base[y,x])
        G[y,x]=True; a[y,x]=2
    for x,y in koplijnen.VAR[var]:
        for dx,dy in ((0,1),(1,0)):
            X,Y=x+dx,y+dy
            if G[Y,X] or FACE[Y,X] or base[Y,X] not in (3,4,5): continue
            if G[min(Y+dy,63),min(X+dx,63)]: continue          # geen lip tussen groeven op 1 px
            a[Y,X]=14 if base[Y,X]==5 else 5
    return a
def bewaar(a,naam,pal):
    im=Image.fromarray(a.astype(np.uint8),'P'); im.putpalette(pal+[0]*(768-48)); im.save(naam+'.png',transparency=0)
    r=Image.open(naam+'.png').convert('RGBA'); bg=Image.new('RGBA',r.size,(255,255,255,255)); bg.alpha_composite(r)
    bg.resize((512,512),Image.NEAREST).save(naam+'_8x.png')
if __name__=='__main__':
    import rots
    for v in 'abc':
        a=rots.rots(kop(C5,v)); pal,palg=rots.palet(PAL5),rots.palet(PALG)
        bewaar(a,'welp_c6_'+v,pal); bewaar(a,'welp_c6_'+v+'_grijs',palg)

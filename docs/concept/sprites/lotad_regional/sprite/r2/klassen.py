# Materiaalklassen per natieve modelpixel (maskers uit r8/kleur_r1.py, toegepast op het natieve raster).
# 0 achtergrond, 1 zwart (lijn), 2 hoed, 3 gezicht/kop, 4 snavel, 5 kraag, 6 poten, 7 oog (wordt vervangen door het Lotad-oog)
import numpy as np; from PIL import Image
LAB=['bg','zwart','hoed','kop','snavel','kraag','poten','oog']
def lum(a): return 0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2]
def vul(m,y,x):
    out=np.zeros_like(m); st=[(y,x)]
    while st:
        y_,x_=st.pop()
        if y_<0 or x_<0 or y_>=m.shape[0] or x_>=m.shape[1] or out[y_,x_] or not m[y_,x_]: continue
        out[y_,x_]=True; st+=[(y_+1,x_),(y_-1,x_),(y_,x_+1),(y_,x_-1)]
    return out
def klassen_r8(path='natief.png'):
    a=np.asarray(Image.open(path).convert('RGB')).astype(float)
    R,G,B=a[...,0],a[...,1],a[...,2]; L=lum(a); sat=a.max(2)-a.min(2)
    H,W=L.shape; y,x=np.mgrid[0:H,0:W]
    # natieve coords: volle resolutie = 3.55+0.5+4.264/2 + i*4.264 (x), 4.0+0.5+4.264/2 + j*4.264 (y)
    X=6.18+x*4.264; Y=6.63+y*4.264
    c=np.zeros((H,W),int)
    wit=(L>222)&(sat<40); c[~wit]=-1
    ln=(L<62)&~wit
    body=(c==-1)&~ln
    hat=body&(Y<236)
    bill=body&~hat&(X>=376)&(X<=500)&(Y>=270)&(Y<=313)&~(G>R+5)
    rest=body&~hat&~bill
    legs=rest&(R>=G+7)&(B<122)&(Y>370)
    fringe=rest&~legs&((Y>=322)|(L>150)|(X>588))
    face=rest&~legs&~fringe
    # borst-V onder de kin: zelfde groen als de kop (G-R>=7, middentoon), samenhangend vanaf (106,78)
    vk=(G-R>=7)&(L>105)&(L<150)&body&~hat&~bill&~legs
    vmask=vul(vk,78,106)
    fringe=fringe&~vmask; face=face|vmask
    c[ln]=1; c[hat]=2; c[face]=3; c[bill]=4; c[fringe]=5; c[legs]=6
    for (x0,y0,x1,y1) in [(484,248,512,282),(396,248,418,278)]:
        box=(X>=x0)&(X<x1)&(Y>=y0)&(Y<y1)&(c!=2)&((c!=0)|(L>222))
        c[box]=7
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen_r8()
    col=np.array([[255,255,255],[0,0,0],[200,90,60],[120,160,120],[240,200,80],[150,140,60],[110,70,40],[255,0,255]])
    Image.fromarray(col[c].astype('uint8')).crop((70,15,170,110)).resize((800,760),Image.NEAREST).save('/tmp/claude-0/k.png')
    for k in range(8): print(LAB[k],(c==k).sum())

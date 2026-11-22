# r16: patronen als tekening op de huid van een wezen i.p.v. kleding (Jordi op r15: "het moet echt duidelijk de patronen op
# een soort alien zijn"). Basis r15-a. Masker + rode borst van r13 blijven; naden en tailleband weg; rood loopt door in de
# mouw; armband-tatoeage blauw/rood/blauw schuin getrapt; borst en shorts grijpen getrapt in elkaar; shorts lopen bij de knie
# in een punt uit in de creme huid; selout overal de donkere tint van het aangrenzende vlak, volume per lichaamsdeel over de patronen heen.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r14'); sys.path.insert(0,'../sprite_r9')
from r14 import R13, stuk, tint, B, H, W, KL2, zigzag
KLEUR={'r':('R','Q','Q'),'B':('B','B','b'),'R':('R','R','Q'),'c':('L','M','D')}
# Jordi (aanvulling): "minder zwart, minder rechte lijnen, en werk met kleurtinten en schaduw": L3-grond = diep indigo uit de
# koptinten (3/3/2) i.p.v. zwart; binnenlijn arm-over-lijf in de donkere tint van het vlak erachter (Q of de beenschaduw).
BEEN={'L1':dict(p=('B','B','b'),z=('W','W','L'),bin='b'),'L3':dict(p=('3','3','2'),z=('Y','Y','D'),bin='2')}
# rij 33 (romp) en rij 34 (dijen): getrapte grens, rood loopt in tanden naar de spleet toe, beenpatroon komt aan de buitenkant omhoog
TAND={(33,29):'p',(33,30):'r',(33,31):'r',(33,33):'r',(33,34):'r',(33,35):'p',(33,36):'p',
      (34,30):'r',(34,34):'r'}
def mat(y,x):
    s=stuk[y,x]
    if (y,x) in TAND: return TAND[(y,x)]
    if s=='RO': return None                              # r13 blijft
    if s=='LA':                                          # schuine armband: bovenste pixel van de kolom 1 kolom verder
        c=[j for j in range(H) if stuk[j,x]=='LA']; u=x+(1 if y==min(c) else 0)
        return 'r' if u>=26 else {25:'B',24:'R',23:'B'}.get(u,'c')
    if s=='RA':
        r=[i for i in range(W) if stuk[y,i]=='RA']; v=y-(x-min(r))
        return 'r' if v<=32 else {33:'B',34:'R',35:'B'}.get(v,'c')
    # dijen: zigzag; onderaan in een punt uitlopen naar de creme knie
    r=[i for i in range(W) if stuk[y,i]==s]; i=x-min(r)
    if y==47: return 'c'
    if y==46 and i!=1: return 'c'
    return 'z' if zigzag(s,y,x)=='m' else 'p'
# selout lichtkant: overal dezelfde regel, de donkerste tint van de kleur die eraan grenst (geen zwart, geen apart 'kledingstuk')
DONKER={'R':'Q','Q':'Q','B':'b','b':'b','W':'L','L':'S','M':'S','D':'S','Y':'D','3':'2','2':'2','1':'2'}
def bouw(been):
    R=R13.copy()
    for y in range(H):
        for x in range(W):
            if not stuk[y,x]: continue
            m=mat(y,x)
            if m is None: continue
            kl=BEEN[been][m] if m in ('p','z') else KLEUR[m]
            R[y,x]=kl[tint[y,x]]
    for y in range(18,48):                               # een huid: selout lichtkant overal S
        for x in range(W):
            if B[y,x]!='K' or stuk[y,x]: continue
            if B[y,x-1]=='.' and stuk[y,x+1]: R[y,x]=DONKER.get(R[y,x+1],'S')
            elif B[y-1,x]=='.' and stuk[y+1,x] and x<=31: R[y,x]=DONKER.get(R[y+1,x],'S')
            elif y>=26 and not stuk[y,x] and all(B[y+a,x+b]!='.' for a,b in ((1,0),(-1,0),(0,1),(0,-1))):   # binnenlijn, geen zwart
                R[y,x]='Q' if y<=33 else BEEN[been]['bin']
    keys=['.']+sorted(set(R.ravel())-{'.'}); assert len(keys)<=16,keys
    out=Image.fromarray(np.vectorize(keys.index)(R).astype('uint8'),'P')
    flat=[c for k in keys for c in KL2[k]]; out.putpalette(flat+[0]*(768-len(flat))); out.save('astro_a_%s.png'%been,transparency=0)
    return R,keys
if __name__=='__main__':
    for b in BEEN:
        R,k=bouw(b); print(b,len(k),'kleuren')
        for y in range(24,49): print('  %2d '%y+''.join(R[y,16:44]))

# Meting r15/r16 vs referenties: vachtgroep (vulling zonder lijn), tinten, stappen, fragmentatie, lijnen.
import sys, numpy as np
from scipy import ndimage
from laad import *
def L(c): c=np.asarray(c,float); return 0.299*c[0]+0.587*c[1]+0.114*c[2]
# (naam, loader, vachtvulling-indices, lijnindex van die vacht, crème/tweede vachtgroep vulling)
ch='.KbcdfSCeLMogWwD'; I={c:i for i,c in enumerate(ch)}
def ours(p): return ons(p)
SETS=[
 ('r15', lambda: ons('docs/concept/sprites/bibarel_evo/sprite_r15/sprite.png'), [I['c'],I['d'],I['f']], [I['C'],I['M'],I['S']]),
 ('bibarel', lambda: gen3('bibarel'), [4,2], [5,6]),
 ('ursaring', lambda: gen3('ursaring'), [1,2,6], [12,11,8]),
 ('linoone', lambda: gen3('linoone'), [2,3,4,8], [5]),
 ('furret', lambda: gen3('furret'), [3,6], [2,5,7,8]),
 ('sentret', lambda: gen3('sentret'), [7,11,9,8], []),
 ('teddiursa', lambda: gen3('teddiursa'), [2,4,3,7], [9]),
 ('swampert', lambda: gen3('swampert'), [3,4,6], [5]),
 ('alphyena', lambda: ons('docs/concept/sprites/mightyena_evo/af/alphyena.png'), [3,4,5,6,7], []),
 ('coathief', lambda: ons('docs/concept/sprites/coathief/af/coathief.png'), [6,7], [8,9,10]),
 ('gnomad', lambda: ons('docs/concept/sprites/gnomad/af/gnomad.png'), [2,3,4,5], [6,7,8]),
]
if len(sys.argv)>1: SETS.insert(1,('r16', lambda: ons('docs/concept/sprites/bibarel_evo/sprite_r16/sprite.png'), [I['c'],I['d'],I['f']], [I['C'],I['M'],I['S']]))
def stats(a,pal,fill):
    m=np.isin(a,fill); n=m.sum()
    Ls=sorted(L(pal[i]) for i in fill); steps=[round(Ls[i+1]-Ls[i]) for i in range(len(Ls)-1)]
    small=0; comps=0; sizes=[]
    for i in fill:
        lab,k=ndimage.label(a==i)   # 4-verbonden
        s=np.bincount(lab.ravel())[1:]; comps+=k; sizes+=list(s); small+=int((s<3).sum())
    # grenslengte binnen de vacht: paren buren beide in de vacht met verschillende tint
    b=0
    for dy,dx in((0,1),(1,0)):
        A=a[:a.shape[0]-dy,:a.shape[1]-dx]; B=a[dy:,dx:]
        mm=np.isin(A,fill)&np.isin(B,fill); b+=int((mm&(A!=B)).sum())
    sizes=np.array(sizes)
    return dict(n=int(n),tinten=len(fill),stappen=steps,eil_lt3=round(100*small/max(n,1),1),
                vlakken_per100=round(100*comps/max(n,1),1),
                med_vlak=int(np.median(sizes)) if len(sizes) else 0,
                gr_vlak_aandeel=round(100*sizes[sizes>=20].sum()/max(n,1)) if len(sizes) else 0,
                grens_per100=round(100*b/max(n,1),1))
def lijnen(a,pal):
    op=a>0; zw=np.array([L(pal[i])<35 if i>0 else False for i in range(len(pal))])
    pad=np.pad(op,1); rand=op&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
    ys,xs=np.nonzero(op); cy,cx=ys.mean(),xs.mean()
    ry,rx=np.nonzero(rand); isz=zw[a[ry,rx]]
    licht=(rx<cx)&(ry<cy); schaduw=(rx>=cx)|(ry>=cy+8)
    return dict(zwart_pct=round(100*zw[a][op].mean(),1), rand_zwart_licht=round(100*isz[licht].mean()), rand_zwart_schaduw=round(100*isz[schaduw].mean()))
rows=[]
for naam,ld,fur,cr in SETS:
    a,p=ld(); s=stats(a,p,fur); l=lijnen(a,p); c=stats(a,p,cr) if cr else None
    rows.append((naam,s,l,c))
    print(f"{naam:10s} vacht n={s['n']:4d} tinten={s['tinten']} stappen={s['stappen']} eil<3/100={s['eil_lt3']:4} vlakken/100={s['vlakken_per100']:4} mediaan={s['med_vlak']:3d} aandeel_vlak>=20={s['gr_vlak_aandeel']:3}% grens/100={s['grens_per100']:5} | zwart={l['zwart_pct']}% rand zwart licht/schaduw={l['rand_zwart_licht']}/{l['rand_zwart_schaduw']}%" + (f" | 2e groep n={c['n']} stappen={c['stappen']} eil<3/100={c['eil_lt3']} grens/100={c['grens_per100']}" if c else ''))

# auto.py: regelstap van r2 (Krassault-recept), uit r1 + het model. Geeft auto.png; maak_r2.py zet daarna de handwerkdata erop.
# spritepixel (x,y) = natief modelblok vanaf (2x-1, 2y-14)  (offset van half2.py, oy=0 ox=1)
from PIL import Image; import numpy as np
PAL=[(255,0,255),(14,13,22),(60,54,80),(49,48,61),(71,68,87),(89,88,103),(115,111,132),(130,126,150),(161,158,174),(180,179,191),(209,206,219)]
K,L,P1,P2,P3,S2,S,M,B,H=1,2,3,4,5,6,7,8,9,10
NAAM={0:'.',K:'K',L:'L',P1:'1',P2:'2',P3:'3',S2:'d',S:'s',M:'m',B:'b',H:'h'}
nat=np.asarray(Image.open('../kleur_r1/natief.png').convert('RGB')).astype(float)
nlum=nat@[0.299,0.587,0.114]; nbg=nat.min(2)>=215; ndrk=nlum<35
r1=np.array(Image.open('../kleur_r1/abra_r1.png')).astype(int)
def blok(x,y): return (slice(2*y-14,2*y-12),slice(2*x-1,2*x+1))
def modeltoon(x,y):
    sl=blok(x,y); m=~nbg[sl]&~ndrk[sl]
    if not m.any(): return None
    l=np.median(nlum[sl][m])
    if l<60: return P1
    if l<80: return P2
    if l<102: return P3
    if l<122: return S2
    if l<146: return S
    if l<170: return M
    if l<195: return B
    return H
def ndark(x,y): sl=blok(x,y); return int(ndrk[sl].sum())
def run():
    o=r1.copy(); Hh,Ww=o.shape
    fig=o>0
    # 1. vulling opnieuw gemeten op het model
    for y,x in zip(*np.where(fig&(o!=1))):
        t=modeltoon(x,y); o[y,x]=t if t else o[y,x]
    # 2. binnenlijnen 1 px: in elk 2x2-blok dat helemaal lijn is, de pixel met het minste model-zwart wordt vulling
    def rand(y,x):
        return any(not(0<=y+dy<Hh and 0<=x+dx<Ww) or not fig[y+dy,x+dx] for dy,dx in((0,1),(1,0),(0,-1),(-1,0)))
    for it in range(3):
        ch=0
        for y in range(Hh-1):
            for x in range(Ww-1):
                q=[(y,x),(y,x+1),(y+1,x),(y+1,x+1)]
                if all(o[p]==1 for p in q):
                    kand=[p for p in q if not rand(*p)]
                    if not kand: continue
                    p=min(kand,key=lambda p:(ndark(p[1],p[0]),-sum(o[p[0]+dy,p[1]+dx]==1 for dy in(-1,0,1) for dx in(-1,0,1) if 0<=p[0]+dy<Hh and 0<=p[1]+dx<Ww)))
                    t=modeltoon(p[1],p[0]); o[p]=t if t else S; ch+=1
        if not ch: break
    # 3. ontkorrelen vulling: clusters < 4 px (4-buren, zelfde index) nemen de meest voorkomende buurtint (zelfde materiaal) aan,
    #    BEHALVE als het model de vlek echt heeft: >= 3 van de 4 modelpixels van elk blok vallen in die tint (vlekjes/streepjes blijven)
    def tint(l):
        for th,c in ((35,K),(60,P1),(80,P2),(102,P3),(122,S2),(146,S),(170,M),(195,B)):
            if l<th: return c
        return H
    global GEHOUDEN; GEHOUDEN=[]
    for it in range(3):
        seen=np.zeros_like(o,bool); ch=0
        for y0,x0 in zip(*np.where((o>=P1))):
            if seen[y0,x0]: continue
            v=o[y0,x0]; comp=[(y0,x0)]; seen[y0,x0]=True; k=0
            while k<len(comp):
                cy,cx=comp[k]; k+=1
                for dy,dx in((0,1),(1,0),(0,-1),(-1,0)):
                    yy,xx=cy+dy,cx+dx
                    if 0<=yy<Hh and 0<=xx<Ww and not seen[yy,xx] and o[yy,xx]==v: seen[yy,xx]=True; comp.append((yy,xx))
            if len(comp)>=4: continue
            bewijs=all(sum(tint(nlum[2*cy-14+a_,2*cx-1+b_])==v for a_ in(0,1) for b_ in(0,1) if not nbg[2*cy-14+a_,2*cx-1+b_])>=3 for cy,cx in comp)
            if bewijs: GEHOUDEN.append((v,comp)); continue
            nb=[]
            for cy,cx in comp:
                for dy,dx in((0,1),(1,0),(0,-1),(-1,0)):
                    yy,xx=cy+dy,cx+dx
                    if 0<=yy<Hh and 0<=xx<Ww and o[yy,xx]>=P1 and o[yy,xx]!=v and ((o[yy,xx]<=P3)==(v<=P3)): nb.append(o[yy,xx])
            if nb:
                vv,cc=np.unique(nb,return_counts=True); n=vv[cc.argmax()]
                for p in comp: o[p]=n
                ch+=1
        if not ch: break
    # 4. lijnkleur: buitenrand open naar boven/links -> L, open naar onder/rechts -> K; binnenlijn tussen huid -> L;
    #    lijn die aan een plaat (P1-P3) grenst blijft K (L leest niet op de donkere platen)
    o2=o.copy()
    for y,x in zip(*np.where(o==1)):
        nb={}
        for dy,dx,n in((-1,0,'b'),(0,-1,'l'),(1,0,'o'),(0,1,'r')):
            yy,xx=y+dy,x+dx; nb[n]=o[yy,xx] if 0<=yy<Hh and 0<=xx<Ww else 0
        plaat=any(P1<=v<=P3 for v in nb.values())
        if plaat: continue
        if nb['o']==0 or nb['r']==0: continue
        if nb['b']==0 or nb['l']==0: o2[y,x]=L; continue
        # binnenlijn: alleen L als hij niet tussen twee schaduwvlakken ligt
        vul=[v for v in nb.values() if v>=S2]
        if vul and max(vul)>=M: o2[y,x]=L
    return o2
if __name__=='__main__':
    o=run(); im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-3*len(PAL))); im.save('auto.png',transparency=0)
    print('kleuren',len(set(o.ravel()))-1,'zwart %.1f%%'%(100*(o==1).sum()/(o>0).sum()))

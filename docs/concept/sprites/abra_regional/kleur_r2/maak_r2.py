# maak_r2.py: regionale Abra r2 (Krassault-recept). Gebruik (vanuit kleur_r2/): python3 maak_r2.py
# Bron: silhouet van r1 (bevroren, bewaakt door bewaak.py) + het model (../kleur_r1/natief.png).
# spritepixel (x,y) = natief modelblok vanaf (2x-1, 2y-14).
#  1. buitenrand = omlijning (1 px, dicht)
#  2. binnenlijnen = elk blok met >=1 zwarte modelpixel, verdund tot 1 px doorlopend (lijnen.py)
#  3. vulling = mediaan van de niet-zwarte modelpixels in het blok, op de tintenreeks per materiaal
#  4. ontkorrelen: clusters < 4 px nemen de buurtint aan, tenzij het model de vlek echt heeft (>=3/4 modelpixels in die tint)
#  5. lijnkleur: lichtkant (open naar boven/links) en binnenlijnen op de huid in lijnkleur L; schaduwkant, plaatgrenzen en ogen zwart
#  6. handwerk als data (EDITS), elk met reden in LOG.md
import numpy as np; from PIL import Image
from auto import PAL,NAAM,K,L,P1,P2,P3,S2,S,M,B,H,nlum,nbg,ndrk
from lijnen import ndk_map, verdun
CH={v:k for k,v in NAAM.items()}
def tint(l):
    for th,c in ((35,K),(60,P1),(80,P2),(102,P3),(122,S2),(146,S),(170,M),(195,B)):
        if l<th: return c
    return H
r1=np.array(Image.open('../kleur_r1/abra_r1.png')).astype(int)
EDITS="""
# zone y x0 tekens ('_' = laten, '.' = transparant: alleen in de handenzone)
# --- ogen (gesloten), op de modelplek: rechteroog model (30,28)-(29,28)-(28,29)-(28,30); linkeroog (22,30)(23,30)(23,31)
oog 28 29 Kb
oog 29 28 K
oog 30 22 KK____K
oog 31 23 K
# --- snuit/kaak links (mzoom.py 17 27 30 38): donkergrijs kaakvlak onder het linkeroog, licht snuitvlak ernaast
sn 31 21 11K
sn 32 22 1Kh
sn 33 21 1__h
sn 34 22 11h
# --- linkervoet (mzoom.py 6 45 22 58): lichte teenbovenkant, zwarte lijn onder de eerste teen, zwart blok onder de tweede
vt 48 12 hhb
vt 49 10 hKKs
vt 50 10 KK
# --- linkerhand en linkerknie (handenzone; gelezen op het model, mzoom.py 17 44 30 58)
hl 46 19 21K
hl 50 24 bKKsKK
hl 51 26 .
hl 52 20 .LsLsK
hl 53 25 K.
"""
HANDZONE=lambda x,y: 18<=x<=37 and 46<=y<=58
def bouw(fig):
    Hh,Ww=fig.shape
    p=np.pad(fig,1); rand=fig&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
    ndk=ndk_map(); T=verdun(fig&((ndk>=1)|rand),rand,ndk)
    o=np.zeros((Hh,Ww),int)
    for y,x in zip(*np.where(fig)):
        if T[y,x]: o[y,x]=K; continue
        sl=(slice(2*y-14,2*y-12),slice(2*x-1,2*x+1))
        # binnen het silhouet zijn bijna-witte modelpixels hooglicht, geen achtergrond (voet, kop: lum >= 215)
        m=~ndrk[sl] if not rand[y,x] else ~nbg[sl]&~ndrk[sl]
        o[y,x]=tint(np.median(nlum[sl][m])) if m.any() else S
    # losse binnenlijnpixels zonder aansluiting weg (ogen worden in EDITS gezet)
    for y,x in zip(*np.where((o==K)&~rand)):
        w=o[max(0,y-1):y+2,max(0,x-1):x+2]
        if (w==K).sum()==1:
            sl=(slice(2*y-14,2*y-12),slice(2*x-1,2*x+1)); m=~nbg[sl]&~ndrk[sl]
            o[y,x]=tint(np.median(nlum[sl][m])) if m.any() else S
    # ontkorrelen
    gehouden=[]
    for it in range(3):
        seen=np.zeros_like(fig); ch=0
        for y0,x0 in zip(*np.where(o>=P1)):
            if seen[y0,x0]: continue
            v=o[y0,x0]; comp=[(y0,x0)]; seen[y0,x0]=True; k=0
            while k<len(comp):
                cy,cx=comp[k]; k+=1
                for dy,dx in((0,1),(1,0),(0,-1),(-1,0)):
                    yy,xx=cy+dy,cx+dx
                    if 0<=yy<Hh and 0<=xx<Ww and not seen[yy,xx] and o[yy,xx]==v: seen[yy,xx]=True; comp.append((yy,xx))
            if len(comp)>=4: continue
            bewijs=all(sum(tint(nlum[2*cy-14+a,2*cx-1+b])==v for a in(0,1) for b in(0,1) if not nbg[2*cy-14+a,2*cx-1+b])>=3 for cy,cx in comp)
            if bewijs:
                if it==0: gehouden.append((NAAM[v],[(int(cx),int(cy)) for cy,cx in comp]))
                continue
            nb=[o[cy+dy,cx+dx] for cy,cx in comp for dy,dx in((0,1),(1,0),(0,-1),(-1,0)) if 0<=cy+dy<Hh and 0<=cx+dx<Ww and o[cy+dy,cx+dx]>=P1 and o[cy+dy,cx+dx]!=v and ((o[cy+dy,cx+dx]<=P3)==(v<=P3))]
            if nb:
                vv,cc=np.unique(nb,return_counts=True)
                for q in comp: o[q]=vv[cc.argmax()]
                ch+=1
        if not ch: break
    # lijnkleur
    o2=o.copy()
    for y,x in zip(*np.where(o==K)):
        n={nm:(o[y+dy,x+dx] if 0<=y+dy<Hh and 0<=x+dx<Ww else 0) for dy,dx,nm in((-1,0,'b'),(0,-1,'l'),(1,0,'o'),(0,1,'r'))}
        if any(P1<=v<=P2 for v in n.values()): continue          # tegen de donkerste plaattinten leest L niet: zwart
        if n['o']==0 or n['r']==0: continue                       # schaduwkant van de buitenrand: zwart
        if n['b']==0 or n['l']==0: o2[y,x]=L; continue            # lichtkant van de buitenrand: lijnkleur
        vul=[v for v in n.values() if v>=P3]
        if vul and max(vul)>=S: o2[y,x]=L                         # binnenlijn op huid: lijnkleur
    o2[o2==S2]=S   # huid: 4 tinten (schaduw s / overgang m / basis b / hooglicht h); de modeltint d (115) ligt 15 onder s en valt ermee samen
    return o2,gehouden,rand
def edits(o):
    log=[]
    for r in EDITS.strip().splitlines():
        if r.startswith('#') or not r.strip(): continue
        z,y,x0,t=r.split(); y=int(y); x0=int(x0)
        for k,c in enumerate(t):
            if c=='_': continue
            x=x0+k; v=CH[c]
            if (v==0 or o[y,x]==0) and not HANDZONE(x,y): raise SystemExit('silhouet buiten handenzone: %s %d,%d'%(z,x,y))
            if o[y,x]!=v: log.append((z,x,y,NAAM[o[y,x]],c)); o[y,x]=v
    return log
if __name__=='__main__':
    o,geh,rand=bouw(r1>0)
    Image.fromarray(o.astype('uint8'),'P').save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/e768f5de-0252-58bb-8bc9-76aca5f6423c/scratchpad/regels.png')
    log=edits(o)
    im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-3*len(PAL))); im.save('abra_r2.png',transparency=0)
    tot=(o>0).sum()
    print('kleuren',len(set(o.ravel()))-1,'| zwart %.1f%% | lijnkleur %.1f%% | edits %d'%(100*(o==K).sum()/tot,100*(o==L).sum()/tot,len(log)))
    import json; json.dump({'gehouden':geh,'edits':log},open('_maak_r2.json','w'))

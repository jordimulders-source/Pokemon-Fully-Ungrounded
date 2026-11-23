# Ronde 2 op claydol_2ogen_B: rechte rode lijn i.p.v. boog 3, rechterzijkant samenhangend, linkerstrook aaneengesloten.
import sys, os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from twee import *
HIER2=os.path.dirname(os.path.abspath(__file__))
B,_=bouw(**VARIANTEN['B']); d=4
ROOD=E[14,32]   # rood uit het rechte topstuk van boog 2

def maak(links_src, b=None, U0=7, L_off=5, Lc=37, rij11=True):
    S=B.copy()
    # 1. linkerstrook (kol 11-14, rij 19-30; rij 31 kol 13-16): blokken van 2 aaneengesloten bronkolommen
    for y in range(19,32):
        x_l=13 if y==31 else 11
        for i,c in enumerate(links_src): S[y,x_l+i]=E[y,c]
    # 2. rode lijn: boog 3 weg; V2 (19,43) loopt recht door over rij 19 tot de rand (19,50)
    #    steen boven de lijn (rij 14-18, kol 44-49) <- voorhoofd tussen V1 en boog 2 (basis rij 14-18, kol 24-28 (+28)), rood-vrij
    for y in range(14,19):
        for x in range(44,50):
            if E[y,x]==7 or E[y,x]==0 or S[y,x]==7: continue
            S[y,x]=E[y,24+min(x-44,4)]
    S[17,44]=E[17,28]               # rechterarm V2 (oude opgang boog 3) -> steen uit dezelfde bron
    S[18,50]=E[18,51]               # oude eindhaak -> koprand ernaast
    for x in range(44,51): S[19,x]=ROOD
    # 3. rechterzijkant rij 20-31 kol 44-51: boven voorhoofd-steen (basis rij U0.., kol 27..), onder onderkop-schaduw
    #    (basis rij y+L_off, kol Lc..), grens schuin langs de kopvorm (rechts hoger = schaduw)
    b=b or {44:27,45:27,46:26,47:26,48:25,49:25,50:25,51:25}
    for x in range(44,52):
        for y in range(20,32):
            if (y in (19,20) and x==51) or (y==30 and x>=51) or (y==31 and x>=48): continue
            if y<b[x]: S[y,x]=E[U0+(y-20), 27+(x-44)]
            else:      S[y,x]=E[y+L_off, Lc+(x-44)]
    # 4. naad rij 11/12: rij 9-11 ook 4 kolommen mee (kol 20 herhaald), 4 kolommen effen 4/5 geschrapt (kol 37-40)
    if rij11:
        for y in range(9,12):
            src=list(range(0,21))+[20]*d+list(range(21,37))+list(range(41,64))
            row=E[y,src]
            S[y,21:43]=row[21:43]
    return S

def check(S):
    assert ((S>0)==(E>0)).all(), 'silhouet'
    ch=S!=E; ys,xs=np.where(ch)
    assert ys.min()>=9 and ys.max()<=36 and xs.min()>=11 and xs.max()<=51
    return ch.sum()

KEUZE=dict(links_src=[10,11,40,41])
if __name__=='__main__':
    from PIL import ImageDraw
    S=maak(**KEUZE); n=check(S)
    # krans/punt/lijf/staven: buiten kop-rechthoek diff 0 (check), plus: geen kransbolletjespixel (crème 1/2 buiten de ogen) geraakt
    print('gewijzigd t.o.v. 3-ogenbasis:',n,'| t.o.v. B:',(S!=B).sum())
    save(S,os.path.join(HIER2,'claydol_2ogen_r2'))
    r2,b,e=rgba(S),rgba(B),rgba(E)
    bal=Image.open(os.path.join(HIER,'../sprite_r19/baltoy_r19.png')); bal.info.setdefault('transparency',0); bal=bal.convert('RGBA')
    items=[('r2',r2),('B (ronde 1)',b),('basis 3 ogen',e)]
    W=3*530+290; v=Image.new('RGBA',(W,18+512+12+24*12+12+90),(255,255,255,255)); dr=ImageDraw.Draw(v)
    for i,(t,im) in enumerate(items):
        x=10+i*530; dr.text((x,3),t,fill='black')
        v.alpha_composite(im.resize((512,512),Image.NEAREST),(x,16))
        v.alpha_composite(im.crop((8,8,51,32)).resize((43*12,24*12),Image.NEAREST),(x,16+512+12))
        y=16+512+12+24*12+12
        for j,bg in enumerate([(248,248,240,255),(40,40,48,255)]):
            t2=Image.new('RGBA',(80,80),bg); t2.alpha_composite(im,(8,8)); v.alpha_composite(t2,(x+j*90,y))
    x=10+3*530; dr.text((x,3),'Baltoy r19 4x / 1x; r2 4x',fill='black')
    v.alpha_composite(bal.resize((256,256),Image.NEAREST),(x,16)); v.alpha_composite(r2.resize((256,256),Image.NEAREST),(x,290))
    t2=Image.new('RGBA',(80,80),(248,248,240,255)); t2.alpha_composite(bal,(8,8)); v.alpha_composite(t2,(x,560))
    v.save(os.path.join(HIER2,'vel.png'))

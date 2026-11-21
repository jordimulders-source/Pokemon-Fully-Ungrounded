# Altaria (onweerswolk) r11: kop groter, twee varianten, vanaf sprite_r10/altaria_r10.png. Bouwen vanuit altaria/: python3 sprite_r11/bouw.py
# Jordi (21 nov): "ik denk dat de kop nog wat groter moet, want de vorm is echt raar" · "extra overlap over de wolk heen is ook niet erg".
# A = de kop van de echte Gen 3-Altaria op 100 % (graphics/pokemon/altaria/anim_front.png, X20-36 Y13-24, niets geschrapt);
# B = ±117 % (rijen Y16 en Y22 en kolommen X26, X28, X33 verdubbeld = Gengas-methode, niets hertekend).
# Kleur per laag zoals r10. Plaats: kin (Altaria Y24) direct boven de bevroren hals, Altaria's hals (X27-32) boven onze hals (X24-29);
# de bovenkant van de kop komt dan op Y18 onder de bevroren kuifstengels (Y17, X24-30): kuif hoeft niet te schuiven.
import sys, numpy as np
from PIL import Image
UIT='sprite_r11'
r10im=Image.open('sprite_r10/altaria_r10.png'); r10=np.array(r10im).astype(int); P=r10im.getpalette()
r9=np.array(Image.open('sprite_r9/altaria_r9.png')).astype(int)
PAL=[tuple(P[3*k:3*k+3]) for k in range(14)]
PU,WS,WN,WD,WT,WC,ST,VS,VD,VM,VL,VH,LW=range(1,14)
alt=np.array(Image.open('../../../../../graphics/pokemon/altaria/anim_front.png'))[:64].astype(int).copy()
# Altaria: 1 selout (72,96,144) | 2 zwart | 3 schaduw | 4 basis | 5 donkere selout | 6 hooglicht | 7 wit | 8 pluisschaduw | 9,10 lichtgrijs | 11 wolk
# leesbaarheid verre oog (Jordi r9: "het linkeroog is niet goed te zien"): kopkleur links van het oog en 1 px snuitlijn weg naast het oog
alt[19,22]=4; alt[20,22]=4; alt[20,24]=3
OOG={(23,19),(23,20),(31,19),(31,20),(32,20)}; WIT={(32,19),(23,18)}
KOPK={3,4,6}; PLUIS={7,8,9,10}; LIJN={1,2,5}
def kleur(rx,ry):
    v=alt[ry,rx]
    if (rx,ry) in OOG: return PU
    if (rx,ry) in WIT: return LW
    if v in LIJN:   # rand: tegen de kop violet-selout, tegen alleen pluis wolk-selout (kin/wangrand)
        nb=[alt[ry+dy,rx+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
        return VS if any(n in KOPK for n in nb) else WS
    if v in PLUIS and any(alt[ry+dy,rx+dx] in (0,11) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))):
        return WS    # pluis aan de buitenkant (tegen lucht/wolk): wolk-selout, zodat kin en wang niet in de wolk wegvallen
    # pluiswit -> cyaanwit (index 7, de lichtste teal, lichter dan de wolkkappen: Altaria's witte pluis valt zo niet weg in de wolk)
    return {3:VM,4:VL,6:VH,7:ST,9:WC,10:WT,8:WD}[v]
def bouw(rijen,kols,X0,Y0):
    o=r10.copy()
    oud=np.zeros((64,64),bool); oud[18:28,19:35]=True; oud&=(r10!=r9)|np.isin(r10,[VS,VM,VL,VH,LW,PU])
    nieuw=np.zeros((64,64),bool)
    for j,ry in enumerate(rijen):
        for i,rx in enumerate(kols):
            if alt[ry,rx] in (0,11): continue
            X,Y=X0+i,Y0+j; o[Y,X]=kleur(rx,ry); nieuw[Y,X]=True
    rest=oud&~nieuw                      # oude r10-kop die de nieuwe kop niet bedekt -> lucht (in r9 was dat ook kop, geen wolk)
    o[rest]=0
    # bevroren: buiten de nieuwe kop en de opgeruimde oude kop alles gelijk aan r10
    assert ((o!=r10)&~nieuw&~rest).sum()==0
    return o,nieuw,rest
A_R=list(range(13,25)); A_K=list(range(20,37))
B_R=[13,14,15,16,16,17,18,19,20,21,22,22,23,24]; B_K=[20,21,22,23,24,25,26,26,27,28,28,29,30,31,32,33,33,34,35,36]
VAR={'A':(A_R,A_K,17,18),'B':(B_R,B_K,16,18)}
def opslaan(o,p):
    im=Image.fromarray(o.astype('uint8'),'P'); pal=[x for cc in PAL for x in cc]; im.putpalette(pal+[0]*(768-len(pal))); im.save(p,transparency=0)
if __name__=='__main__':
    C='.KSndtcz=vmlhw'
    for n,(R,K,X0,Y0) in VAR.items():
        o,nieuw,rest=bouw(R,K,X0,Y0)
        print(n,'kop',len(R),'x',len(K),'op X%d-%d Y%d-%d'%(X0,X0+len(K)-1,Y0,Y0+len(R)-1),'| oude kop onbedekt:',[(int(x),int(y)) for y,x in zip(*np.where(rest))])
        opslaan(o,UIT+'/altaria_r11%s.png'%n)
        rgb=np.array(PAL,'uint8')[o]; rgb[o==0]=255
        Image.fromarray(rgb).resize((512,512),Image.NEAREST).save(UIT+'/altaria_r11%s_8x.png'%n)
        d=o!=r10
        print('   diff met r10:',int(d.sum()),'| over wolk/hals gelegd (r10 daar wolk/hals, niet kop):',int((nieuw&(r10>0)&~np.isin(r10,[VS,VM,VL,VH,LW,PU])&~((np.arange(64)[:,None]<=27)&(np.arange(64)[None,:]>=19))).sum()),
              '| alpha erbij',int(((o>0)&(r10==0)).sum()),'weg',int(((o==0)&(r10>0)).sum()),'| kleuren',len(set(o.ravel())),'| pupillen',int((o==PU).sum()))

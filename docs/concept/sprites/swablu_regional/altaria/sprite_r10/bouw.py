# Altaria (onweerswolk) r10: alleen de kop opnieuw, vanaf sprite_r9/altaria_r9.png. Bouwen vanuit altaria/: python3 sprite_r10/bouw.py
# Jordi (21 nov): "het gezicht klopt helemaal nog niet.. Linksonderin valt die helemaal weg, het linkeroog is niet goed te zien, rechts is een
# volledige rechte lijn. Sowieso klopt het gezicht in het model niet, daar mag je vanaf wijken, baseer je op de echte altaria, de wolken zijn
# nu goed gelukt".
# Methode (Gengas): de kop van de echte Gen 3-Altaria (graphics/pokemon/altaria/anim_front.png, bovenste 64x64, X20-36 Y13-24) pixel voor
# pixel overnemen per kleurlaag; naar onze kopmaat door hele rijen/kolommen te schrappen (niets hertekenen), dan per laag omkleuren naar
# ons violet (3 tinten + selout) en de witte pluizen/snavel naar onze lichte teal-tinten. Wolk, static, vleugels, hals en kuif bevroren.
import sys, os, numpy as np
from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import label
UIT='sprite_r10'
r9im=Image.open('sprite_r9/altaria_r9.png'); r9=np.array(r9im).astype(int); PALR9=r9im.getpalette()
PAL=[tuple(PALR9[3*k:3*k+3]) for k in range(14)]
PU,WS,WN,WD,WT,WC,ST,VS,VD,VM,VL,VH,LW=range(1,14)
alt=np.array(Image.open('../../../../../graphics/pokemon/altaria/anim_front.png'))[:64].astype(int)
# echte Altaria-indices: 1 (72,96,144) selout | 2 zwart | 3 (16,152,200) schaduw | 4 (88,192,248) basis | 5 (40,56,88) donkere selout |
# 6 (152,216,248) hooglicht | 7 wit (pluis/snavel, oogwit) | 8 (112,112,152) pluisschaduw | 9 (216,224,232) | 10 (168,176,192) | 11 wolk
RIJEN=[int(x) for x in os.environ.get('RIJEN','13,14,15,18,19,20,21,22,23,24').split(',')]     # Y16 en Y17 (schedel, herhaling) geschrapt
KOLS=[int(x) for x in os.environ.get('KOLS','20,21,22,23,24,25,26,27,29,30,31,32,33,35,36').split(',')]  # X28 (voorhoofd) en X34 (zijkant) geschrapt
X0=int(os.environ.get('X0','19')); Y0=int(os.environ.get('Y0','18'))
OOG={(23,19),(23,20),(31,19),(31,20),(32,20)}     # pupillen echte Altaria (zwart blijft zwart)
GLANS={(32,19),(23,18)}                            # oogglans nabij oog + oogwit boven het verre oog
MAP={1:VS,5:VS,2:VS,3:VM,4:VL,6:VH,7:WC,9:WT,10:WT,8:WD}
kop=np.zeros((64,64),int)
for j,ry in enumerate(RIJEN):
    for i,rx in enumerate(KOLS):
        v=alt[ry,rx]
        if v in (0,11): continue
        k=PU if (rx,ry) in OOG else LW if (rx,ry) in GLANS else MAP[v]
        kop[Y0+j,X0+i]=k
o=r9.copy()
KOPZONE=np.zeros((64,64),bool); KOPZONE[18:28,19:34]=True
violet=np.isin(r9,[VS,VD,VM,VL,VH,LW,PU])
# oude kop weg (alleen violet/oog/snavel van r9 in de kopzone); wolk eromheen blijft
OUDKOP=KOPZONE&(violet|((r9>0)&(np.arange(64)[None,:]>=20)&(np.arange(64)[:,None]>=24)&(np.arange(64)[:,None]<=27)&(np.arange(64)[None,:]<=33)))
o[OUDKOP]=0
o[kop>0]=kop[kop>0]
# ---- reparaties per pixel naar de echte Altaria (X19..34, Y18..27; ',' = r9 houden, '.' = transparant) ----
# Overgenomen opbouw (echte Altaria, na schrappen): hooglicht-schedel linksboven, basis licht, selout rondom (lichtkant violet midden zoals
# Altaria's blauwe '3'-rand), ver oog 2 px hoog met oogwit erboven, nabij oog 2x2 met glans rechtsboven, witte snuitpluis links en wangpluis
# rechts met grijze scheiding ertussen. Afwijkingen (Jordi/coordinator): kopkleur links van het verre oog (zodat het leest), snuitbovenlijn 1 rij
# onder het oog (bij Altaria raakt hij het oog), rechterrand rond (5 rijen recht i.p.v. 7, midden-schaduw ernaast), kin/wangrand linksonder in
# wolk-selout tegen de wolk.
KOPGRID={
18:'......mmmmms....',
19:'....mhhhhlllls..',
20:'...mhhhhhllllls.',
21:'..swllllllllllS.',
22:',slKlllllKwlllS.',
23:',slKlmmmmKKllmS.',
24:'occtccctllmmlmS.',
25:',otccccctdccts..',
26:',dotccctdccts...',
27:',,,oddtssdto....',
}
KC={'s':VS,'S':VS,'m':VM,'l':VL,'h':VH,'w':LW,'K':PU,'o':WS,'n':WN,'d':WD,'t':WT,'c':WC}
for Y,row in KOPGRID.items():
    assert len(row)==16,(Y,len(row))
    for i,ch in enumerate(row):
        X=19+i
        if ch==',': o[Y,X]=r9[Y,X]
        elif ch=='.': o[Y,X]=0
        else: o[Y,X]=KC[ch]
if __name__=='__main__':
    def opslaan(o,p):
        im=Image.fromarray(o.astype('uint8'),'P'); pal=[x for cc in PAL for x in cc]; im.putpalette(pal+[0]*(768-len(pal))); im.save(p,transparency=0)
    opslaan(o,UIT+'/altaria_r10.png')
    rgb=np.array(PAL,'uint8')[o]; rgb[o==0]=255
    Image.fromarray(rgb).resize((512,512),Image.NEAREST).save(UIT+'/altaria_r10_8x.png')
    # bevroren: alles buiten de kopzone X19-34, Y18-27 gelijk aan r9
    Z=np.zeros((64,64),bool); Z[18:28,19:35]=True
    assert ((o!=r9)&~Z).sum()==0
    d=(o!=r9)
    print('diff r10<->r9:',int(d.sum()),'(alleen kopzone)')
    print('alpha erbij:',[(int(x),int(y)) for y,x in zip(*np.where((o>0)&(r9==0)))])
    print('alpha weg:',[(int(x),int(y)) for y,x in zip(*np.where((o==0)&(r9>0)))])
    print('kleuren incl. transparant:',len(set(o.ravel())),'| pupil-pixels:',[(int(x),int(y)) for y,x in zip(*np.where(o==PU))])

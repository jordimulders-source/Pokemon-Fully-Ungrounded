# r3: alle reparaties uit sprite_v2_r2/KEURING.md, plus het besluit van Claude over de rugstekels. Werkt op de basis van bouw.py.
# Draaien vanuit docs/concept/sprites/pinsir_evo/:
#   python3 sprite_v2_r3/bouw.py A && python3 sprite_v2_r3/bouw.py B && python3 sprite_v2_r3/reparaties.py
# Elke reparatie logt hoeveel pixels hij verandert (-> reparaties.txt). Coordinaten (x,y) zijn spritepixels.
import sys, numpy as np
from scipy import ndimage as nd
from PIL import Image
D='sprite_v2_r3/'
N4=np.array([[0,1,0],[1,1,1],[0,1,0]])
PUPIL='zonder' not in sys.argv
LOG=[]
BRUIN=(3,4,5,14); ROOM=(6,7,8)

def zet(I,pts,v,als=None,naam=''):
    n=0
    for x,y in pts:
        if als is not None and I[y,x] not in als: continue
        if I[y,x]!=v: I[y,x]=v; n+=1
    LOG.append('%-58s %3d px'%(naam,n)); return I
def rect(x0,x1,y0,y1): return [(x,y) for y in range(y0,y1+1) for x in range(x0,x1+1)]

def repareer(I,var):
    I=I.copy(); SIL0=I>0
    # 0. buiklijnen: bruine modelcellen met hoge toon midden in de buik werden index 14 -> buiklijntint 6 (model 191,172,138)
    room=np.isin(I,ROOM)
    nb=sum(np.roll(room,s,a) for s,a in ((1,0),(-1,0),(1,1),(-1,1)))
    m=(I==14)&(nb>=2)
    pts=[(x,y) for y,x in zip(*np.where(m))]; zet(I,pts,6,naam='buiklijnen: 14 in de buik -> 6')

    # 0b. buik (keurder): hoofdvlak 7 (= modeltint 227,211,178); 8 alleen als hooglicht linksboven rond (23-27,36-39);
    #     6 als sikkel langs de onderkant (y >= 48, zodat de plaatlijn op y 46 leesbaar blijft) en de rechterrand. Buiklijnen (6) blijven.
    BUIK=np.zeros((64,64),bool); BUIK[33:53,17:33]=True
    vlakb=BUIK&np.isin(I,(7,8))
    zet(I,[(x,y) for y,x in zip(*np.where(vlakb))],7,naam='buik: hoofdvlak 7')
    zet(I,[(x,y) for y,x in zip(*np.where(vlakb)) if 23<=x<=27 and 36<=y<=39],8,naam='buik: hooglicht linksboven 8')
    rechts=np.zeros_like(vlakb); rechts[:,:-1]=~np.isin(I[:,1:],(6,7,8))
    rechts2=rechts|np.roll(rechts,-1,1)
    zet(I,[(x,y) for y,x in zip(*np.where(vlakb)) if y>=47 or (rechts2[y,x] and y>=40)],6,naam='buik: schaduwsikkel onder (y>=48) en rechts 6')
    # 1. kopschild horizontaal gelaagd zoals het model (keurder top 2)
    #    vlak = 5; lichte schuine bovenband 14; onderrand y19-20 = 4 over de hele breedte (ook links); rechteronderhoek 4;
    #    lichte streep op de rechteronderrand (model) 14; geen verticale streep x20-21. Stekelflanken blijven.
    SCHILD=[(x,y) for y in range(13,21) for x in range(6,38) if I[y,x] in BRUIN+(6,)]
    stek=set()
    for x,y in SCHILD:                      # stekelbinnenpixels (rij <= 14 met lucht/lijn links of rechts) niet aanraken
        if y<=14 and (I[y,x-1] in (0,1,2) or I[y,x+1] in (0,1,2)): stek.add((x,y))
    vlak=[p for p in SCHILD if p not in stek]
    zet(I,vlak,5,naam='kopschild: vlak 5 (geen effen licht/donker-blok, geen x20-21-streep)')
    zet(I,[p for p in rect(13,19,15,15)+rect(16,22,16,16)+rect(12,16,14,14) if p in vlak],14,naam='kopschild: lichte schuine bovenband 14')
    zet(I,[p for p in rect(6,37,19,20) if p in vlak],4,naam='kopschild: onderrand y19-20 -> 4 (ook links 9-13)')
    zet(I,[p for p in rect(31,37,17,18) if p in vlak],4,naam='kopschild: rechteronderhoek 4')
    zet(I,[p for p in rect(26,30,18,18) if p in vlak],14,naam='kopschild: lichte streep rechtsonder op de rand')
    zet(I,[(12,12),(12,13),(14,12),(15,13),(16,13),(19,9)],2,als=(1,),naam='kopschild: selout lichtkant 1->2')
    zet(I,[(x,y) for y in range(9,15) for x in range(6,38) if I[y,x]==6],14,naam='kopschild: stekelpunt roomtint 6 -> 14')

    # 2. ogen (recept keurder: gespiegeld, zwarte balk ertussen, pupil binnen)
    zet(I,[(19,22),(15,22),(20,22),(13,20)],1,naam='ogen: los geel/brauw -> zwart')
    if PUPIL: zet(I,[(14,22),(21,22)],1,naam='ogen: pupillen binnen')
    zet(I,[(13,21),(14,21),(13,22),(22,20),(21,21),(22,21),(22,22)]+([] if PUPIL else [(14,22),(21,22)]),13,naam='ogen: geel')
    zet(I,rect(14,21,22,22) if PUPIL else rect(15,20,22,22),1,naam='ogen: doorlopende balk')

    # 3. verre been (keurder top 4): been 4, knobbel 5 met hooglicht, modellijnen, schaduwsikkel rechts/onder, voetklauwen
    BEEN=[(x,y) for y in range(47,59) for x in range(14,25) if I[y,x] in BRUIN]
    zet(I,BEEN,4,naam='verre been: vlak 4')
    zet(I,[p for p in rect(15,17,49,53) if p in BEEN],5,naam='verre been: knieknobbel 5')
    zet(I,[(15,49),(16,49)],14,naam='verre been: knobbel hooglicht')
    for y in range(47,59):                   # sikkel: meest rechtse beenpixel per rij -> 3, onderste rij -> 3
        xs=[x for x,yy in BEEN if yy==y and I[y,x] in BRUIN]
        if xs: zet(I,[(max(xs),y)],3,naam='verre been: sikkel rechts')
    zet(I,[p for p in BEEN if p[1]==58],3,als=BRUIN,naam='verre been: sikkel onder')
    zet(I,rect(19,23,54,54),2,naam='verre been: dwarslijn (19-23,54)')
    zet(I,rect(18,18,51,53),2,naam='verre been: knobbelrand (18,51-53)')
    zet(I,[(16,59),(16,60)],1,naam='verre voet: scheiding twee klauwen')
    zet(I,[(14,59),(15,59),(17,59)],7,naam='verre voet: klauwpunten 7')
    zet(I,[(15,60),(17,60),(18,59)],6,naam='verre voet: klauwonderkant 6')

    # 4. nabije hand: drie klauwen uit het model (gemeten room-/zwartfracties per spritepixel), lijf 7, punt 8, onderkant 6, zwart rond
    HAND={41:{32:2,33:4,34:5,35:4,36:4,37:2},
          42:{32:2,33:7,34:7,35:1,36:7,37:2},
          43:{32:1,33:7,34:1,35:7,36:6,37:1},
          44:{32:8,33:1,34:1,35:6,36:1,37:1},
          45:{32:1,33:1,34:7,35:1,36:1,37:4},
          46:{33:6,34:1}}
    n=0
    for y,r in HAND.items():
        for x,v in r.items():
            if I[y,x]!=v: I[y,x]=v; n+=1
    LOG.append('%-58s %3d px'%('nabije hand: drie klauwen (geen dambord)',n))
    # verre hand in de schaduwtint
    zet(I,[(10,43),(10,44)],7,als=(8,),naam='verre hand: 8 -> 7')
    zet(I,[(11,43),(10,45)],6,als=(7,),naam='verre hand: 7 -> 6')

    # 5. kleine punten
    zet(I,[p for p in rect(37,41,52,55) if I[p[1],p[0]] in (6,14)],5,naam='knie: binnenkant 6/14 -> 5')
    zet(I,[(38,52),(39,52)],14,naam='knie: hooglicht linksboven')
    zet(I,[(40,52),(41,52),(39,54),(40,54),(41,53),(41,54),(38,55),(39,55),(40,55)]+[(x,y) for x in range(34,44) for y in (55,56,57) ],4,als=(5,14),naam='knie: onderste helft binnen de ring en rand eronder 4 (helderheid +14 -> model)')
    zet(I,[(36,53),(36,54)],5,als=(2,),naam='knie: dubbele lijn x34/x36 -> een lijn')
    zet(I,[p for p in rect(34,38,47,47)],5,als=(6,14),naam='dij: lichte strook y47 -> 5 (banding)')
    zet(I,[p for p in rect(47,54,46,47)],5,als=(6,14),naam='staart: lichte strook y46-47 -> 5 (banding)')
    zet(I,[p for p in rect(32,37,30,35) if p not in rect(32,34,30,31)],5,als=(6,14),naam='koepel: 14 -> 5 (alleen 32-34,30-31 licht)')
    zet(I,[p for p in rect(32,34,30,31)],14,als=BRUIN,naam='koepel: hooglicht')
    zet(I,rect(33,40,37,40),4,als=(5,14),naam='onderarm: 5 -> 4')
    for y in range(37,41):                   # een rij 5 langs de linkerbovenrand van de onderarm
        xs=[x for x in range(33,41) if I[y,x]==4]
        if xs: zet(I,[(min(xs),y)],5,naam='onderarm: lichtrand links')
    zet(I,[(x,37) for x in range(33,41)],5,als=(4,),naam='onderarm: lichtrand boven')
    zet(I,[(x,38) for x in range(34,40)],5,als=(4,),naam='onderarm: tweede lichte rij (helderheid arm -11 -> model)')
    zet(I,[(34,39),(35,39)],5,als=(4,),naam='onderarm: lichtrand links rij 39')
    zet(I,[(15,41),(16,41),(13,42),(14,42)],5,als=(4,),naam='verre arm: bovenkant 5 (helderheid -8 -> model)')
    zet(I,rect(9,11,19,19)+rect(10,13,20,20),4,als=(6,14,5),naam='kopschild links onder 6 -> 4')

    # 6. rugstekels (besluit Claude): ~7 driehoekige stekels op de modelplekken (toppen gemeten op het 1024-model als lokale
    #    uitsteeksels van de rugrand), 2-3 px hoog, punt 1 px, lichte flank (linksboven) en donkere flank; silhouet groeit alleen daar.
    # Toppen op het 1024-model gemeten als lokale uitsteeksels van de rugrand (sprite-coordinaten): (41.8,20.6) (46.0,22.0)
    # (50.2,24.8) (54.4,28.3) wijzen omhoog; (55.8,31.8) en (54.4,38.9) wijzen naar rechts; (39.0,21.2) is een klein stekeltje.
    # Sjabloon per stekel (punt = 1 px zwart, lichte flank 2/14/5 linksboven, donkere flank 3/1 rechtsonder); een sjabloonpixel
    # overschrijft alleen lucht of buitenlijn, nooit het lijf.
    # Werkwijze: (a) de rugrand van r1 (trapje met losse 1-px-bultjes) vervangen door een gladde rand door de inkepingen van het
    # model: bovenrand e(x) door (37,21) (41,21) (45,23) (49,26) (53,29), steile deel rechterrand x=53 (y 30-37);
    # (b) daarop de stekels als driehoekjes (punt 1 px, 3 hoog) op de gemeten modeltoppen; (c) buitenlijn opnieuw:
    # lichtkant (lucht erboven/links) lijnbruin 2, schaduwkant zwart 1, punt zwart 1; flanken: licht 14/5 links, donker 3 rechts.
    yy,xx=np.mgrid[0:64,0:64]
    sil0=I>0; sil=sil0.copy(); RAND0=sil0&~nd.binary_erosion(sil0,N4,border_value=0)
    ex=np.round(np.interp(np.arange(64),[37,41,45,49,53],[21,21,23,26,29])).astype(int)
    for x in range(37,54):
        for y in range(19,31):
            sil[y,x]= y>=ex[x]
    for y in range(29,38):
        for x in range(53,57): sil[y,x]= x<=53
    # stekels (3 hoog boven de inkeping: punt 1 px, rij van 3, rij van 4 die naar rechts leunt; de inkeping eronder wordt binnenkant): toppen op de gemeten
    # modeltoppen langs de rand; tussen twee stekels blijft minstens 1 kolom inkeping.
    OMH={(0,0):'p',(-1,1):'L',(0,1):'h',(1,1):'D',(-1,2):'L',(0,2):'m',(1,2):'d',(2,2):'D',(-1,3):'m',(0,3):'m',(1,3):'d',(2,3):'d'}
    REC={(0,0):'p',(-1,-1):'L',(-1,0):'h',(-1,1):'D',(-2,-1):'L',(-2,0):'m',(-2,1):'d',(-2,2):'D',(-3,-1):'m',(-3,0):'m',(-3,1):'d',(-3,2):'d'}
    STEKELS=[((39,ex[39]-3),OMH),((42,ex[42]-3),OMH),((46,ex[46]-3),OMH),((50,ex[50]-3),OMH),((54,ex[53]-3),OMH),((56,32),REC)]
    rol={}
    for (tx,ty),sj in STEKELS:
        for (dx,dy),r in sj.items():
            x,y=tx+dx,ty+dy; rol[(x,y)]=r; sil[y,x]=True
    nieuw=sil&~sil0; weg=sil0&~sil
    I[weg]=0
    rand=sil&~nd.binary_erosion(sil,N4,border_value=0)
    lucht=~sil; lucht[:,58:]=False; lucht[42:,:]=False; lucht[:17,:]=False; lucht[:,:36]=False
    strook=sil&nd.binary_dilation(lucht,np.ones((3,3)),iterations=2)
    strook[:,:37]=False
    for y,x in zip(*np.where(strook)):
        r=rol.get((x,y))
        if r=='p': I[y,x]=1
        elif r=='h': I[y,x]=14
        elif r=='m': I[y,x]=5
        elif r=='d': I[y,x]=3
        elif rand[y,x]:
            lucht_boven=not sil[y-1,x]; lucht_rechts=not sil[y,x+1]
            I[y,x]=2 if (r=='L' or (lucht_boven and not lucht_rechts and r!='D')) else 1
        elif I[y,x]==0 or (RAND0[y,x] and I[y,x] in (1,2)):   # nieuw lijf of oude buitenlijn die nu binnen ligt
            I[y,x]=4
    gat=sil&(I==0); I[gat]=4                     # gaatjes van r1 onder de nieuwe rand -> lijf
    LOG.append('%-58s %3d px erbij, %d px weg'%('rugstekels + gladde rugrand: silhouet',int(nieuw.sum()),int(weg.sum())))
    NIEUWSIL=sil&~SIL0
    # 7. tintvlakjes < 3 px (bruin) in het lijf -> omringende tint (niet in gezicht, handen, stekels, kop-stekels)
    BESCH=np.zeros((64,64),bool); BESCH[19:34,11:25]=True; BESCH[40:47,31:38]=True; BESCH[41:48,8:14]=True; BESCH[:15,:]=True
    BESCH[58:62,13:20]=True
    for (tx,ty),sj in STEKELS:
        for (dx,dy) in sj: BESCH[ty+dy,tx+dx]=True
    for _ in range(3):
        for k in (3,4,5):                 # 14 = bewust klein hooglicht, niet opruimen
            l,nn=nd.label(I==k,N4)
            for i in range(1,nn+1):
                mm=l==i
                if mm.sum()>=3 or (mm&BESCH).any(): continue
                ring=nd.binary_dilation(mm,N4)&~mm
                ks=[v for v in I[ring] if v in BRUIN]
                if ks:
                    v=max(set(ks),key=ks.count); n=int(mm.sum()); I[mm]=v; LOG.append('%-58s %3d px'%('vlakje < 3 px -> buurtint',n))
    return I,NIEUWSIL

def opslaan(I,pad,pal):
    im=Image.fromarray(I.astype('uint8'),'P'); im.putpalette(pal); im.save(pad,transparency=0)

if __name__=='__main__':
    out=open(D+'reparaties.txt','w')
    for var in 'AB':
        b=Image.open(D+'pinsir_evo_v2_r3_%s_basis.png'%var); pal=b.getpalette()
        LOG.clear()
        I,ns=repareer(np.array(b),var)
        assert len(np.unique(I))<=16
        naam=D+'pinsir_evo_v2_r3_%s%s.png'%(var,'' if PUPIL else '_zonderpupil')
        opslaan(I,naam,pal)
        chk=Image.open(naam); assert chk.mode=='P' and chk.info.get('transparency')==0
        r1=np.array(Image.open('sprite_v2/pinsir_evo_v2_r1.png'))
        sil=((I>0)!=(r1>0))
        out.write('== %s ==\n'%var+'\n'.join(LOG)+'\nsilhouet anders dan r1: %d px, allemaal nieuw (stekels): %s\n  %s\n\n'%(sil.sum(),bool(((I>0)&~(r1>0)).sum()==sil.sum()),[(int(x),int(y)) for y,x in zip(*np.where(sil))]))
    out.close(); print(open(D+'reparaties.txt').read()[:3000])

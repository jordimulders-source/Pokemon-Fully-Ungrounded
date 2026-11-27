# Ronde 2 op basis van r1 (maak_r1): gemeten modelhelderheid per spritepixel, wit oogwit, gezichtsvarianten,
# glans + lijn op het schouderglas. Nog steeds: alleen verschuiven, weghalen, tinten kiezen.
import numpy as np; from PIL import Image
import maak_r1 as m1, reduceer3, schoon, bouw
PAL=dict(m1.PAL); PAL[3]=(248,248,248)          # oogwit = eigen witte kleur (r8: wit oogwit)
KEYS=[0,1,10,11,12,13,14,20,21,22,23,30,31,32,3]
def label_png(lab,pad):
    idx=np.zeros(lab.shape,'uint8'); pal=[]
    for i,k in enumerate(KEYS): idx[lab==k]=i; pal+=list(PAL[k])
    idx[lab==2]=1
    pal+=[0,0,0]*(16-len(KEYS)); im=Image.fromarray(idx,'P'); im.putpalette(pal+[0]*(768-len(pal))); im.save(pad,transparency=0); return im
def reductie(a,brein):
    z=bouw.Z_HOOFD
    if brein=='A': return reduceer3.reduceer(a,(2,2),2,z,4,None,'gem')[2:66,0:64].copy()
    return reduceer3.reduceer(a,(2,2),2,z,3,None,'gem')[2:66,0:64].copy()
# --- gezicht ---
def ogen_r8(lab,x0=22,y0=13,dr=0):
    lab=m1.zet_ogen(lab,x0,y0,dr)
    lab[(lab==23)&(np.arange(64)[:,None]>=12)&(np.arange(64)[:,None]<=17)&(np.arange(64)[None,:]>=21)&(np.arange(64)[None,:]<=36)]=3
    return lab
def zand_buur(lab,p):
    n=schoon.buurtint(lab,p,1,set()); return n if n else 12
def wenkbrauw(lab,modus,y=13,x0=22):
    """r5-wenkbrauwlijn (rij 13) weghalen: 'a' = hele doorlopende lijn weg (alleen r8-oogleden blijven),
    'b' = alleen het stuk tussen de ogen weg (boven elk oog blijft hij staan)."""
    xs=range(x0+1,x0+8) if modus=='a' else range(x0+4,x0+7)
    weg=[]
    for x in xs:
        if lab[y,x]==1: lab[y,x]=zand_buur(lab,(y,x)); weg.append((y,x))
    return lab,weg
MACHAMP=np.asarray(Image.open('../../../../../../graphics/pokemon/machamp/anim_front_gba.png'))
def ogen_machamp(lab,dx=-1,dy=-3):
    """Machamp-ogen (anim_front_gba, x24-25 en x31-34, rij 15-18) 1-op-1 als één blok: wit/lichtgrijs -> oogwit,
    zwart -> pupil (zwart), rood/donkerrood -> donkerste zandtint (iris), donkergroene wenkbrauwlijn -> lijntint."""
    # r5/r8-oogwit en pupillen eerst weg
    for y in range(12,17):
        for x in range(21,36):
            if lab[y,x] in (2,3,23): lab[y,x]=zand_buur(lab,(y,x))
    mp={1:3,10:3,15:2,6:10,7:10,14:10}
    gezet=[]
    for y in range(15,19):
        for x in list(range(24,26))+list(range(31,35)):
            v=int(MACHAMP[y,x])
            if v in mp: lab[y+dy,x+dx]=mp[v]; gezet.append((y+dy,x+dx))
    return lab
# --- glas op de schouders: glans links (lichtste glastint), schaduw rechts, lijn waar het glas op het lijf staat ---
def schouderglas(lab):
    for y in range(3,20):
        rij=[x for x in range(64) if 20<=lab[y,x]<30]
        if not rij: continue
        # groepen (fles links van het hoofd, trechter rechts)
        groepen=[]; g=[rij[0]]
        for x in rij[1:]:
            if x==g[-1]+1: g.append(x)
            else: groepen.append(g); g=[x]
        groepen.append(g)
        for g in groepen:
            if g[0]>20 and g[-1]<40: continue        # geen boeien/hoofd
            if len(g)>=2: lab[y,g[0]]=23; lab[y,g[-1]]=21 if lab[y,g[-1]]!=20 else 20
            elif len(g)==1 and lab[y,g[0]]==22: lab[y,g[0]]=23
    return lab
def linkerbol(lab):
    """Linkerbol: glas boven = één glastint (G2) met de lichtste tint als glans, zand onder; de middentint G1
    (losse vlekken) wordt G2. Alleen tintkeuze; barst (G0) en zand blijven."""
    n=0
    for y in range(51,59):
        for x in range(22,30):
            if lab[y,x]==21: lab[y,x]=22; n+=1
    return lab,n
def bouw_sprite(brein='B',gezicht='a',fles=(-8,-14),trechter=(0,-8),spier=6):
    a=m1.natief(brein,fles,trechter,spier); lab=reductie(a,brein)
    lab=schoon.tintclusters(lab,3); lab=schoon.losse_lijnen(lab,3)
    lab,_=m1.glasspikkels_weg(lab)
    if gezicht=='c': lab=ogen_machamp(lab)
    else:
        lab=ogen_r8(lab); lab,_=wenkbrauw(lab,gezicht)
    lab=m1.barst_r5_weg(lab); lab,_=m1.barst(lab)
    lab=schouderglas(lab); lab,_=linkerbol(lab)
    return bouw.binnenlijnen(bouw.buitenlijn(lab))

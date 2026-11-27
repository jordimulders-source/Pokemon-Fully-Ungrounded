# r3: kaal_lab.npy (64x64 modellabels na 2x-reductie + schrappen) -> palet r5 per klasse/toon. Geen pixel verschuift.
import numpy as np, sys; from PIL import Image
sys.path.insert(0,'gereedschap')
L=np.load('kaal_lab.npy')
PAL=[(152,208,160),(26,16,20),                     # 0 transp, 1 lijn
 (124,76,18),(196,148,53),(229,184,79),(246,214,124),# 2-5 goud r5: donker/selout, schaduw, hoofd, hooglicht
 (206,188,180),(244,240,234),                       # 6-7 wit r5
 (128,28,42),(166,48,63),(208,99,104),              # 8-10 rood r5 (kop/kam en karmijn pennen)
 (186,82,38),(222,118,50),                          # 11-12 oranje r5
 (50,41,52),                                        # 13 donkere punt
 (204,192,148),                                     # 14 ivoor schaduw (snavel/klauw)
 (92,80,96)]                                        # 15 punt-licht
# modelkleur (natief label) -> paletindex
M={2:1,18:1, 6:13,14:13,23:13, 1:2,5:2,25:2,24:2,27:2,21:3, 0:3,15:3,20:3, 13:4,11:4,19:4,4:4,
   17:7,3:7,16:7, 9:6, 7:7,26:14, 8:8,12:9,10:10,22:10}
def omzet(k):
    if k<0: return 0
    if k>=200: b=k-200; return 8 if M[b] in (2,3) else 9            # karmijn: schaduw / midden
    if k>=100: b=k-100; return 11 if M[b] in (2,3) else 12          # oranje
    return M[k]
o=np.vectorize(omzet)(L)
np.save('stap_palet.npy',o)
def opslaan(o,pad,schaal=1):
    im=Image.new('P',(64,64)); flat=[x for c in PAL for x in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.putdata([int(v) for v in o.ravel()]); im.save(pad,transparency=0)
if __name__=='__main__':
    opslaan(o,'stap_palet.png')

# ---------------- technische stappen; elke stap telt zijn wijzigingen per zone ----------------
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(a,b) for a in (-1,0,1) for b in (-1,0,1) if a or b]
GRP={2:'g',3:'g',4:'g',5:'g',6:'w',7:'w',14:'w',8:'r',9:'r',10:'r',11:'o',12:'o',13:'t',15:'t'}
DONKER={'g':2,'w':6,'r':8,'o':11,'t':13}
def zone(Y,X):
    if 16<=Y<=38 and 14<=X<=30: return 'kop+kraag'
    if Y>=42: return 'poten+staart'
    return 'vleugels+lijf'
tel={}
def noteer(naam,oud,nieuw):
    d=np.argwhere(oud!=nieuw); t={}
    for Y,X in d: z=zone(Y,X); t[z]=t.get(z,0)+1
    tel[naam]=t
def g(o,Y,X): return o[Y,X] if 0<=Y<64 and 0<=X<64 else 0
KOP=(16,38,14,30)
# 1. oog: 1-op-1 Spearow (Gen 3), omgekleurd zoals r2, op de modelplek van het oog (r7 -> sprite (22,21)), kijkt naar links
v=o.copy()
sp=np.array(Image.open('../../../../../graphics/pokemon/spearow/anim_front_gba.png'))
kmap={15:1,1:7,9:8,13:8}; DX,DY=22-25,22-23
for yy in range(21,27):
    for xx in range(23,28):
        if sp[yy,xx] in kmap: o[yy+DY,xx+DX]=kmap[sp[yy,xx]]
noteer('oog Spearow',v,o)
# 2. snavel: modelpixels van de snavel (ivoor) -> licht linksboven 7, rest 14; omlijning waar de snavel aan vleugel/band grenst
v=o.copy(); SN=[(25,16),(25,17),(26,16),(26,17),(27,16)]
for Y,X in SN: o[Y,X]=14
o[25,16]=7
for Y,X in SN:
    for dy,dx in N4:
        q=(Y+dy,X+dx)
        if q not in SN and o[q] not in (0,1,8,9,10): o[q]=1
noteer('snavel',v,o)

# 2b. kop: binnenlijnen (zwarte modelpixel geheel omringd door kop) -> donkerste kooptint 8 (Gen 3: binnenlijn in eigen tint);
#     rand van de kop tegen vleugel/kraag blijft zwart = gesloten omlijning van de voorste vorm. Oog blijft.
v=o.copy(); OOG=set()
for yy in range(21,27):
    for xx in range(23,28):
        if sp[yy,xx] in kmap: OOG.add((yy+DY,xx+DX))
for Y,X in zip(*np.where(v==1)):
    if not(KOP[0]<=Y<=KOP[1] and KOP[2]<=X<=KOP[3]) or (Y,X) in OOG: continue
    nb=[g(v,Y+a,X+b) for a,b in N8]
    if all(q in (1,8,9,10) for q in nb) and sum(q in (8,9,10) for q in nb)>=3: o[Y,X]=8
    elif all(q in (1,6,7) for q in nb) and sum(q in (6,7) for q in nb)>=3: o[Y,X]=6
noteer('kop/kraag binnenlijnen',v,o)
# 2c. staart (rij >= 52, onder het lijf): per veer licht links, schaduw rechts tegen de volgende scheiding; scheidingen lopen
#     door in de donkere punten; lichtste punt-tint aan de lichtkant van elke punt.
v=o.copy()
for Y in range(52,64):
    for X in range(20,50):
        k=v[Y,X]
        if k in (3,4):
            if g(v,Y,X+1) in (1,2) and g(v,Y,X-1) not in (1,2): o[Y,X]=3
            elif g(v,Y,X-1) in (1,2,0) : o[Y,X]=4
        if k==13 and g(v,Y-1,X) in (1,2) and g(v,Y,X-1)==13 and g(v,Y,X+1)==13: o[Y,X]=1
for Y in range(52,64):
    for X in range(20,50):
        if o[Y,X]==13 and g(o,Y,X-1) in (1,2,0) and g(o,Y,X+1)==13 and g(o,Y-1,X)!=0: o[Y,X]=15
noteer('staart tinten/scheiding',v,o)

# 2d. poten (tenen rij 48-52 links van de staart): goud een tint lichter zodat tenen (goud) tegen de zwarte lijn lezen;
#     klauwen = modelklauwpixels in ivoor (licht 7, schaduw 14 onder/rechts).
v=o.copy()
for Y in range(48,53):
    for X in range(19,40):
        if v[Y,X]==2: o[Y,X]=3
        elif v[Y,X]==3: o[Y,X]=4
        elif v[Y,X] in (6,7,14) and Y>=49: o[Y,X]=14 if g(v,Y-1,X) in (6,7,14) else 7
noteer('poten',v,o)
# 3. hooglicht linksboven op grote goudvlakken: goud 4 met buur boven/links buiten de groep en >=2 goud eronder/rechts
v=o.copy()
for Y,X in zip(*np.where(v==4)):
    up,lf=g(v,Y-1,X),g(v,Y,X-1)
    if (GRP.get(up)!='g' or GRP.get(lf)!='g') and up!=0 and lf!=0 and g(v,Y+1,X) in (3,4) and g(v,Y,X+1) in (3,4) and g(v,Y+1,X+1) in (3,4):
        o[Y,X]=5
for Y,X in zip(*np.where(v==12)):
    if GRP.get(g(v,Y-1,X))!='o' and g(v,Y+1,X)==12: o[Y,X]=12
noteer('hooglicht goud',v,o)
# 4. buitenlijn: lichte pixel op de rand -> zwart (achtergrond rechts/onder) of selout = donkerste eigen tint (achtergrond links/boven)
v=o.copy()
for Y,X in zip(*np.where(v>0)):
    k=v[Y,X]
    if k in (1,2,13,8,11,6): continue
    u,d,l,r=[g(v,Y+a,X+b) for a,b in N4]
    if 0 not in (u,d,l,r): continue
    o[Y,X]=1 if (d==0 or r==0) else DONKER[GRP[k]]
noteer('buitenlijn',v,o)
# 5. losse pixels (geen enkele 8-buur) weg
v=o.copy()
for Y,X in zip(*np.where(v>0)):
    if all(g(v,Y+a,X+b)==0 for a,b in N8): o[Y,X]=0
noteer('losse pixels',v,o)
np.save('sprite.npy',o); opslaan(o,'sprite.png')
k=Image.open('kaal.png')
rand=[(Y,X) for Y,X in zip(*np.where(o>0)) if any(g(o,Y+a,X+b)==0 for a,b in N4)]
print('kleuren',len(set(o.ravel()))-1,'figuurpx',(o>0).sum(),'rand zwart %.0f%%'%(100*sum(o[p]==1 for p in rand)/len(rand)))
for a,b in tel.items(): print(a,b)

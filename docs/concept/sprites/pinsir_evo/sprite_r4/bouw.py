# Pinsir-evolutie r4: KLEURRONDE over de hele sprite + 3 oogvarianten (A/B/C).
# Jordi op r3: "ogen niet goed en beetje zelfde probleem als pitahaya fase 3 had" · "als in hele sprite blurry".
# Silhouet, zwarte lijnposities, kaak-, dekschild- en tandvormen komen 1-op-1 uit r3 (= uit het model); alleen de VULTINTEN
# worden opnieuw verdeeld:
#   1. palet gespreid: per kleurgroep 3 vultinten (+ 1 glans in het lijf) met stappen van ±40-50, donkerste vultint ±40 boven zwart;
#   2. per vorm licht linksboven / schaduw rechtsonder: voor elke vulpixel de afstand tot de vormrand (lijn of achtergrond)
#      in de richtingen linksboven en rechtsonder (stralen, stoppen op zwart/ander materiaal); dichtbij de rand linksboven = licht,
#      dichtbij rechtsonder = schaduw; middenvlak in de middentint (grote egale vlakken zoals Heracross/Pinsir Gen 3);
#   3. modeltoon telt mee (gemiddelde modelhelderheid per spritecel, niet-zwarte pixels): de donkere romp blijft donker,
#      de knieplaten en de onderarm blijven de lichte platen uit het model;
#   4. verre ledematen (linkerarm + linkerbeen; links = ver, zoals het verre oog) één stap donkerder;
#   5. opruimen: tintvlekjes < 3 px gaan naar de meest voorkomende buurtint van hetzelfde materiaal;
#   6. binnenlijnen: zwart blijft waar r3/het model zwart is; tussen twee lichte vlakken (>=3) wordt een 1-px zwart stukje
#      dat niet aan de buitenrand ligt de donkerste vultint (Gen 3: binnenlijn in de donkerste vlaktint).
#   7. ogen: variant A/B/C (alleen in het ooggebied x14-25, y26-29).
# Bouwen: cd pinsir_evo && python3 sprite_r4/bouw.py
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from model import klassen
from PIL import Image; from scipy import ndimage
UIT='sprite_r4'
R3=np.asarray(Image.open('sprite_r3/pinsir_evo_r3.png')).astype(int)
H=W=64; yy,xx=np.mgrid[:H,:W]
# ---------- palet ----------
PAL=[(120,200,160),(18,14,14),
     (70,60,54),(110,94,80),(152,132,108),(198,178,148),     # 2-5 lijf: donker 61, midden 95, licht 131, glans 175
     (96,42,32),(150,72,50),(198,120,86),                    # 6-8 kaak: 57, 91, 135 (donker roodbruin, familie van het model)
     (90,52,26),(150,104,64),(206,160,104),                  # 9-11 dekschild: 56, 106, 157
     (236,222,206),(160,142,130)]                            # 12 oog/tand crème, 13 tandschaduw
LIJF=[2,3,4,5]; KAAK=[6,7,8]; SCHILD=[9,10,11]
def L(c): return sum(c)/3
# ---------- modeltoon per spritecel ----------
a,c,fg=klassen(); ML=a.mean(2); CEL=974/64; MX0,MY0=31,134; DY=13
mt=np.full((H,W),np.nan)
for Y in range(H):
    for X in range(W):
        j=Y-DY; ya,yb=int(round(MY0+j*CEL)),int(round(MY0+(j+1)*CEL)); xa,xb=int(round(MX0+X*CEL)),int(round(MX0+(X+1)*CEL))
        if yb<=0 or xb<=0 or ya>=1024 or xa>=1024: continue
        blk=ML[max(ya,0):yb,max(xa,0):xb]; ff=fg[max(ya,0):yb,max(xa,0):xb]&(blk>=25)
        if ff.sum()>=8: mt[Y,X]=blk[ff].mean()
mtf=np.where(np.isnan(mt),np.nanmean(mt),mt); mts=ndimage.uniform_filter(mtf,3)   # licht gladgestreken: geen celruis
# ---------- materialen ----------
mat=np.zeros((H,W),int)        # 0 bg, 1 zwart, 2 lijf, 3 kaak, 4 schild, 5 tand/oog
mat[R3==1]=1; mat[np.isin(R3,LIJF)]=2; mat[np.isin(R3,KAAK)]=3; mat[np.isin(R3,SCHILD)]=4; mat[np.isin(R3,[12,13])]=5
# ---------- zwarte binnenpixels zonder modellijn ----------
# r3 had in het lijf zwarte streepjes waar het model maar een randje lijn heeft (< 30 % van de cel zwart): die worden vulling
# (krijgen hieronder de tint van hun plaat). Buitenrand en kaak-/schild-/tandgrenzen blijven zwart.
MZ=np.zeros((H,W))
for Y in range(H):
    for X in range(W):
        j=Y-DY; ya,yb=int(round(MY0+j*CEL)),int(round(MY0+(j+1)*CEL)); xa,xb=int(round(MX0+X*CEL)),int(round(MX0+(X+1)*CEL))
        if yb<=0 or xb<=0: continue
        MZ[Y,X]=(c[max(ya,0):yb,max(xa,0):xb]==1).mean()
Pd=np.pad(R3,1)
ZWVULLING=np.zeros((H,W),bool)
for Y,X in zip(*np.where(R3==1)):
    nb=[Pd[Y+1+dy,X+1+dx] for dy in (-1,0,1) for dx in (-1,0,1)]
    if 0 in nb or any(v in KAAK+SCHILD+[12,13] for v in nb): continue
    if MZ[Y,X]<0.20 and Y>=28: ZWVULLING[Y,X]=True
mat[ZWVULLING]=2
# ---------- platen uit het model ----------
# De zwarte modellijnen verdelen het lijf in platen (4-samenhangend, >= 300 modelpx); elke spritepixel krijgt de plaat met de
# meeste modelpixels in zijn cel, en de mediane modelhelderheid van die plaat (de toon van de plaat in het model).
body=np.isin(c,(2,3,4,5)); plab,pn=ndimage.label(body)
pcnt=ndimage.sum(body,plab,np.arange(pn+1)); pmed=ndimage.median(ML,plab,np.arange(pn+1))
PL=np.zeros((H,W),int)
for Y in range(H):
    for X in range(W):
        if mat[Y,X]!=2: continue
        j=Y-DY; ya,yb=int(round(MY0+j*CEL)),int(round(MY0+(j+1)*CEL)); xa,xb=int(round(MX0+X*CEL)),int(round(MX0+(X+1)*CEL))
        l=plab[max(ya,0):yb,max(xa,0):xb].ravel(); l=l[l>0]; l=l[pcnt[l]>=300]
        if len(l): PL[Y,X]=np.bincount(l).argmax()
leeg=(mat==2)&(PL==0)                       # cel zonder grote plaat: plaat van de dichtstbijzijnde lijfpixel
if leeg.any():
    _,idx=ndimage.distance_transform_edt(PL==0,return_indices=True); PL[leeg]=PL[idx[0][leeg],idx[1][leeg]]
PL_ARM=PL[44,37]                                    # plaat van de onderarmstrook (x35-40, y39-51)
# vormid per pixel: lijf = plaat, andere materialen = materiaal
VORM=np.where(mat==2,1000+PL,mat)
# ---------- afstand tot de vormrand linksboven / rechtsonder ----------
def straal(Y,X,dy,dx,m):
    n=0
    while True:
        Y+=dy; X+=dx; n+=1
        if not(0<=Y<H and 0<=X<W) or VORM[Y,X]!=m or n>=7: return n
def richting(Y,X):
    m=VORM[Y,X]
    ul=np.mean([straal(Y,X,-1,-1,m),straal(Y,X,-1,0,m),straal(Y,X,0,-1,m)])
    dr=np.mean([straal(Y,X,1,1,m),straal(Y,X,1,0,m),straal(Y,X,0,1,m)])
    return (dr-ul)/(dr+ul)         # +1 = tegen de rand linksboven (licht), -1 = tegen rechtsonder (schaduw)
# ---------- regio's (voor de verre-ledemaat-stap) ----------
VER=((xx<=24)&(yy>=40))|((xx>=22)&(xx<=31)&(yy>=45))     # verre arm + hand, ver been (links = ver)
o=R3.copy()
for Y,X in zip(*np.where(np.isin(mat,[2,3,4]))):
    m=mat[Y,X]; d=richting(Y,X)
    if m==2:
        med=pmed[PL[Y,X]]; lv=0 if med<45 else 1 if med<64 else 2
        if PL[Y,X]==PL_ARM: lv=2                    # onderarmstrook: lichtste deel van het onderlijf in het model
        if VER[Y,X]: lv=max(lv-1,0)                 # verre ledematen één stap donkerder
        if lv==0:   o[Y,X]=3 if d>0.45 else 2                                   # donkere plaat (romp, schenen, staart)
        elif lv==1: o[Y,X]=4 if d>0.35 else 2 if d<-0.45 else 3                 # middenplaat (kopschild, rug, gezicht)
        else:       o[Y,X]=5 if (d>0.4 and mt[Y,X]>=70) else 4 if d>-0.4 else 3  # lichte plaat (knieën, onderarm, klauwen)
    elif m==3:
        s=d+0.5*(mts[Y,X]-70)/25
        o[Y,X]=6 if s<-0.35 else 7 if s<0.45 else 8
    else:
        # dekschild: modeltekening (vlek/midden/licht) blijft, alleen licht/schaduw per vorm erbovenop
        base={9:-1,10:0,11:1}[R3[Y,X]]
        s=base+0.6*d
        o[Y,X]=9 if s<-0.5 else 10 if s<0.75 else 11
# plaatgrenzen = binnenlijnen uit het model: tussen twee modelplaten komt precies 1 px lijn (op de pixel waarvan de buur
# boven of links in een andere plaat ligt). Zwart waar het model in die cel echt een lijn heeft (>= 35 % zwart), anders de
# donkerste vultint (Gen 3: binnenlijn in de donkerste vlaktint). Bovenlijf (y < 36): r3-lijnen blijven, alleen grenzen zonder lijn.
GRENS=np.zeros((H,W),bool)
for Y,X in zip(*np.where(mat==2)):
    for dy,dx in ((-1,0),(0,-1)):
        Y2,X2=Y+dy,X+dx
        if 0<=Y2<H and 0<=X2<W and mat[Y2,X2]==2 and PL[Y2,X2]!=PL[Y,X] and abs(pmed[PL[Y,X]]-pmed[PL[Y2,X2]])>=12:
            GRENS[Y,X]=True
o[GRENS]=2
# glans alleen op de modelglans (knieplaten, onderarm): 5 waar het model >= 80 is, anders hooguit 4
o[(o==5)&(mt<80)&~np.isnan(mt)]=4
# ---------- opruimen: tintvlekjes < 3 px ----------
def opruimen(o,groep,minpx=3):
    for _ in range(4):
        veranderd=0
        for k in groep:
            lab,n=ndimage.label(o==k)
            for i in range(1,n+1):
                pts=np.argwhere(lab==i)
                if len(pts)>=minpx: continue
                buren={}
                for Y,X in pts:
                    for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
                        v=o[Y+dy,X+dx] if 0<=Y+dy<H and 0<=X+dx<W else 0
                        if v in groep and v!=k: buren[v]=buren.get(v,0)+1
                if buren:
                    nv=max(buren,key=buren.get)
                    for Y,X in pts: o[Y,X]=nv
                    veranderd+=1
        if not veranderd: break
    return o
for g in (LIJF,KAAK,SCHILD): o=opruimen(o,g)
# glans mag klein zijn (hooglicht), maar niet als losse pixel: 1-px glans -> 4
lab,n=ndimage.label(o==5)
for i in range(1,n+1):
    if (lab==i).sum()<2: o[lab==i]=4
# ---------- onderlijf met de hand (onderlijf.txt) ----------
# De automatische verdeling gaf in het onderlijf nog vlekken (platen lopen zonder gesloten lijn in elkaar over). Daarom per
# onderdeel de tinten met de hand gezet op de modelvormen; alleen lijfpixels en zwart (nooit silhouet, kaak, schild).
for ln in open(UIT+'/onderlijf.txt'):
    if not ln.strip() or ln.startswith('#'): continue
    Y,X0,t=ln.split(); Y,X0=int(Y),int(X0)
    for i,ch in enumerate(t):
        X=X0+i; assert R3[Y,X] in [1]+LIJF,(ln,X,R3[Y,X]); o[Y,X]={'K':1}.get(ch,None) or int(ch)
# losse 1-px tintvlekjes die de handronde achterliet (vóór de randregel: de selout langs een schuine rand is per pixel los)
for g in (LIJF,KAAK,SCHILD): o=opruimen(o,g,minpx=2)
# ---------- buitenrand: gekleurde selout aan de lichtkant, geen lichte tint op de rand ----------
# (klauwpunten y >= 53 uitgezonderd, zoals r3: anders verdwijnen ze)
Pb=np.pad(o,1)
for Y,X in zip(*np.where(o>0)):
    if Y>=53: continue
    if any(Pb[Y+1+dy,X+1+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))):
        if o[Y,X] in (4,5): o[Y,X]=3
        elif o[Y,X]==8: o[Y,X]=7
        elif o[Y,X]==11: o[Y,X]=10
# ---------- binnenlijnen ----------
P=np.pad(o,1)
for Y,X in zip(*np.where(R3==1)):
    nb=[P[Y+1+dy,X+1+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
    if 0 in nb: continue
    k8=[P[Y+1+dy,X+1+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
    if sum(v==1 for v in k8)<=1 and all(v in (3,4,5) for v in nb):
        o[Y,X]=2                           # los zwart puntje tussen lichte lijfvlakken -> donkerste vultint
BASIS=o.copy()
# ---------- ogen ----------
# ooggebied: x14-25, y26-29. Model (12x/40x bekeken): beide ogen onder de zwarte kopschildrand (y26), lichte schuine spleet die
# naar binnen (naar de neus) zakt, de donkere pupil zit aan de BINNENKANT onderaan (tussen het kleine en het grote lichte stukje),
# zwarte wenkbrauwband erboven. Verre oog = links (x15-17), nabije oog = rechts (x21-24).
# T = crème 12, t = tandschaduw 13, K = zwart, '-' = laat BASIS staan
OGEN={
 # A: Pinsir Gen 3 1-op-1 (nabij: "K W K W l" onder een brauw die naar binnen zakt; ver: wit met pupil binnen-onder)
 'A':{(22,26):1,(23,26):1,(24,26):1,
      (21,27):1,(22,27):12,(23,27):12,(24,27):12,
      (20,28):1,(21,28):12,(22,28):1,(23,28):12,(24,28):13,
      (16,26):1,(15,27):12,(16,27):12,(17,27):1,
      (15,28):12,(16,28):1,(17,28):1},
 # B: het model letterlijk: één schuine spleet per oog (rechts hoger, zakt naar binnen), pupil als inkeping binnen-onder
 'B':{(22,26):1,(23,26):1,(24,26):1,(21,27):1,(22,27):1,
      (23,27):12,(24,27):12,
      (21,28):12,(22,28):1,(23,28):12,(24,28):12,
      (16,26):1,(15,27):12,(16,27):12,(17,27):1,(16,28):1,(17,28):1},
 # C: zoals A, maar groter wit (3 breed op beide rijen) en de pupil als 1 zwarte pixel onderin tegen de brauwpunt; verre oog 2 breed
 'C':{(22,26):1,(23,26):1,(24,26):1,(25,26):1,
      (21,27):1,(22,27):12,(23,27):12,(24,27):12,
      (21,28):1,(22,28):1,(23,28):12,(24,28):12,
      (16,26):1,(15,27):12,(16,27):12,(17,27):1,
      (15,28):12,(16,28):1,(17,28):1},
}
OOG=(xx>=14)&(xx<=25)&(yy>=26)&(yy<=28)
def opslaan(o,path):
    p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(path,transparency=0)
uit={}
for v,px in OGEN.items():
    q=BASIS.copy()
    for (X,Y),k in px.items():
        assert OOG[Y,X] and R3[Y,X]>0,(v,X,Y); q[Y,X]=k
    opslaan(q,f'{UIT}/pinsir_evo_r4_{v}.png'); uit[v]=q
# ---------- controles ----------
for v,q in uit.items():
    print(v,'silhouet-diff met r3:',int(((q>0)!=(R3>0)).sum()),'| px anders dan r3:',int((q!=R3).sum()),
          '| zwart %.1f%%'%(100*(q==1).sum()/(q>0).sum()),'| kleuren',len(set(q.ravel())))
A,B,C=uit['A'],uit['B'],uit['C']
print('buiten ooggebied A=B=C:',int((A[~OOG]!=B[~OOG]).sum()),int((A[~OOG]!=C[~OOG]).sum()))
print('zwart-posities gewijzigd t.o.v. r3 (buiten ogen):',int(((A==1)!=(R3==1))[~OOG].sum()))
for nm,g in (('lijf',LIJF),('kaak',KAAK),('schild',SCHILD)):
    print('%-6s'%nm,'r3:',[(k,int((R3==k).sum())) for k in g],'-> r4:',[(k,int((A==k).sum())) for k in g])
if len(sys.argv)>1:
    CH='.K2345abcvmlTt'
    for Y in range(12,62): print('%2d '%Y+''.join(CH[v] for v in A[Y]))
# ---------- vel.png: A | r3 | model op 8x; kop A/B/C op 12x; 1x naast Gen 3-Pinsir/Heracross/Scizor op wit en donker ----------
from PIL import ImageDraw
sys.path.insert(0,'gereedschap'); from vel import rgbp, model_op_schaal
def gen3(s,bg):
    im=Image.open(f'../../../../graphics/pokemon/{s}/anim_front.png'); q=np.asarray(im)[:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[q==k]=pal[k]
    return Image.fromarray(img)
v=Image.new('RGB',(3*520,14+512+20+2*(16*12)+40+20+150),'white'); d=ImageDraw.Draw(v)
for i,(nm,im) in enumerate((('r4 A',rgbp(f'{UIT}/pinsir_evo_r4_A.png')),('r3',rgbp('sprite_r3/pinsir_evo_r3.png')),('model',model_op_schaal()))):
    v.paste(im.resize((512,512),Image.NEAREST),(i*520,14)); d.text((i*520+2,0),nm+' 8x',fill=(0,0,0))
y=14+512+20; d.text((2,y-14),'kop op 12x: A | B | C  (x10-30, y20-36)',fill=(0,0,0))
for i,k in enumerate('ABC'):
    im=rgbp(f'{UIT}/pinsir_evo_r4_{k}.png').crop((10,20,30,36)).resize((240,192),Image.NEAREST)
    v.paste(im,(i*260,y)); d.text((i*260+2,y+194),k,fill=(0,0,0))
y+=192+30
for j,bg in enumerate(((255,255,255),(40,48,56))):
    for i,im in enumerate([rgbp(f'{UIT}/pinsir_evo_r4_{k}.png',bg) for k in 'ABC']+[gen3(s,bg) for s in ('pinsir','heracross','scizor')]):
        v.paste(im,(i*70,y+j*70))
d.text((440,y+20),'1x: r4 A, B, C | Gen 3 Pinsir, Heracross, Scizor (wit / donker)',fill=(0,0,0))
v.save(f'{UIT}/vel.png'); print('vel',v.size)

# Pinsir-evolutie r8: basis = r7 (sprite_r7/pinsir_evo_r7_zonder_stekels.png). Zie sprite_r8/NOTITIES.md.
# Jordi bij r7 (letterlijk): "arm, been zijn veel beter nu, qua kleur en tinten de goede kant op, staart ook beter, vleugel nog
# niet, hoofd ietsje beter, maar de vorm van het hoofd is niet mooi, de ogen zijn nu weer verdwenen, die moesten puntiger, niet
# kleiner, en de stekels zijn nergens echt netjes, kijk naar andere stekelige pokemon. Vleugel is ook nog niet gelukt, ik vraag me
# af of je daar naar andere pokemon hebt gekeken, je mag daar meer van het model afwijken zodat het naar een sprite vertaalt"
# r8:
#  BEVROREN (script-check, diff 0): arm, verre arm, been, ver been, staart (r7-delenkaart sprite_r8/r7_delen.npy), kaken, mond, romp.
#  1. KOPSCHILD: veelhoek uit de modelmaten (punt links, lange bovenrand die naar achter oploopt, rechte onderrand over het gezicht),
#     omlijning volgt automatisch uit de vorm (geen hobbels), lichte onderrand (model) + zwarte onderlijn = wenkbrauw.
#  2. OGEN: oog van Gen 3 Pinsir 1-op-1 (3 rijen, schuin, punt naar het midden); varianten A (met pupil) / B (zonder pupil, model).
#  3. STEKELS: opbouw van Tyranitar/Sandslash: driehoek, punt 1 px zwart, lichte linkerflank, donkere rechterflank, vulling loopt
#     zonder lijn door in het lijf; plekken = model.
#  4. DEKSCHILD: twee varianten met elk een Gen 3-aanpak (zie NOTITIES).
# Bouwen: cd pinsir_evo && python3 sprite_r8/bouw.py [raster]
import sys, numpy as np
from PIL import Image
from skimage.draw import polygon as skpoly
from scipy import ndimage
UIT='sprite_r8'
R7=np.asarray(Image.open('sprite_r7/pinsir_evo_r7_zonder_stekels.png')).astype(int)
R7S=np.asarray(Image.open('sprite_r7/pinsir_evo_r7.png')).astype(int)
PAL=[tuple(c) for c in np.array(Image.open('sprite_r7/pinsir_evo_r7.png').getpalette()[:48]).reshape(-1,3)]
DEEL=np.load(UIT+'/r7_delen.npy')
H=W=64; yy,xx=np.mgrid[:H,:W]
CH='.KLabcdopqrsvwxT'; C={c:i for i,c in enumerate(CH)}
N4=((-1,0),(1,0),(0,-1),(0,1))
BEVROREN=np.isin(DEEL,['arm','arm_ver','been','been_ver','staart'])
def inpoly(pts):
    m=np.zeros((H,W),bool); r,c=skpoly([p[1] for p in pts],[p[0] for p in pts],(H,W)); m[r,c]=True; return m
# ======================= 1. KOPSCHILD, RUG, STEKELS =======================
# Model gemeten op rooster 30x: punt links (11.3, 22.5), bovenrand x13 21.8 / x17 21 / x21 20.4 / x25 19.3 / x28 17.5, onderrand
# (lichte band) x16 26.5 .. x26 26.7 .. x36 25.3, rechts tegen de rug (37, 24.5); ogen 27.6-28.8 (1 rij).
# r8: het kopschild staat 1 rij hoger dan het model (lichte onderrand rij 24, zwarte onderlijn rij 25) zodat de ogen rij 26-28
# krijgen (r4 deed hetzelfde). Vorm = zeshoekige plaat: punt links, rechte schuine bovenrand, rechte onderrand over het gezicht,
# achterrand schuin onder de rug. Tinten: bovenband c, vlak b, lichte onderrand c (model), glans d op de voorste punt.
# Stekels (opbouw Tyranitar/Sandslash): vin die naar rechts helt, linkerrand recht, rechterrand 1 px per rij, punt 1 px zwart,
# lichte linkerflank d, midden c, donkere rechterflank b; vulling loopt zonder lijn door in de bovenband van het lijf.
# Plekken = model: kopschild (15.5,19.7) (18.5,18.3) (23.5,16.5) (26.5,15.3) -> 1 rij hoger zoals het kopschild; kegels op de
# achterrand (31.5,19.5) (36,20) -> (31,19) (37,19); rug (32.3,13.1) (38.3,13.4) (44.2,18.3) niet verschoven.
# Raster x 8..49, rij 12..25; '?' = r7 houden.
KOPRASTER=open(UIT+'/kop_raster.txt').read().split('\n')
o=R7.copy()
for r in KOPRASTER[1:]:
    if not r.strip(): continue
    Y=int(r[:2]); rij=r[3:]
    for i,ch in enumerate(rij):
        X=8+i
        if ch=='?': continue
        assert not BEVROREN[Y,X],(Y,X)
        o[Y,X]=C[ch]
for Y in range(12,26):                                  # alles rechts van het raster tot de schildrand: r7-rug boven rij 24 weg
    for X in range(50,64):
        if Y<=23 and DEEL[Y,X] in ('rug','kopschild'): o[Y,X]=0
# ======================= 2. GEZICHT + OGEN =======================
GZ=(yy>=26)&(yy<=28)&(xx>=13)&(xx<=36)&np.isin(DEEL,['kopschild'])
o[GZ]=C['a']
for X in range(27,37):
    if o[26,X]==C['a'] and DEEL[26,X]=='kopschild': o[26,X]=C['L']
# Gen 3 Pinsir-oog 1-op-1 (graphics/pokemon/pinsir/anim_front.png, nabij oog x30-35 rij 25-27, ver oog x22-27 rij 26-28):
# Pinsir 6 wit -> T, 7 zwart -> K, B donkerbruin -> L, 8 huidschaduw -> b, 5 licht -> c
OOG={'A':{(26,22):'L',(26,23):'T',(26,24):'T',(26,25):'b',
          (27,21):'K',(27,22):'T',(27,23):'T',(27,24):'T',(27,25):'b',
          (28,20):'K',(28,21):'T',(28,22):'K',(28,23):'T',(28,24):'c',
          (26,15):'T',(26,16):'L',(26,17):'K',
          (27,15):'T',(27,16):'T',(27,17):'T',(27,18):'K',
          (28,15):'c',(28,16):'T',(28,17):'K',(28,18):'T'}}
OOG['B']=dict(OOG['A']); OOG['B'][(28,22)]='T'; OOG['B'][(28,17)]='T'
FACE0=o.copy()
# ======================= 4. DEKSCHILD + RUGRAND MET STEKELS =======================
# Schildvorm: linkerrand = r7 (grens met arm, romp, rug; bevroren delen blijven), rechterrand = gladde bolle curve gemeten op het
# model (rooster 22x): x 44 (rij 24) .. 50 (31) .. 52 (37) .. 54 (43), punt (52, 47.5). Daarachter de donkere rugrand (model:
# 3 px boven, 1 px onder) met de zwarte silhouetlijn; de rugstekels van het model staan op die rand.
XR={24:43,25:44,26:45,27:46,28:47,29:48,30:48,31:49,32:49,33:50,34:50,35:51,36:51,37:51,38:52,39:52,40:52,41:53,42:53,43:53,44:53,45:53,46:52,47:52}
XS={24:48,25:48,26:49,27:49,28:50,29:50,30:51,31:51,32:52,33:52,34:52,35:53,36:53,37:53,38:54,39:54,40:54,41:54,42:55,43:55,44:55,45:55,46:53,47:53}
S7=(DEEL=='schild')
XL={Y:int(np.where(S7[Y])[0].min()) for Y in range(24,48)}
SM=np.zeros((H,W),bool)
for Y in range(24,48):
    for X in range(XL[Y],XR[Y]+1):
        if not BEVROREN[Y,X]: SM[Y,X]=True
RIM=np.zeros((H,W),bool); SIL=np.zeros((H,W),bool)
for Y,xs in XS.items():
    x0=XR[Y]+1 if Y in XR else 0
    for X in range(max(x0,38),xs):
        if not BEVROREN[Y,X] and not SM[Y,X] and (Y>=24 or o[Y,X]!=0): RIM[Y,X]=True
    for X in range(xs,W):
        if not BEVROREN[Y,X] and Y>=24: o[Y,X]=0
    if not BEVROREN[Y,xs]: SIL[Y,xs]=True
# rugstekels op de rand (model (48.5,24.3) (51.6,29.4) (53.4,33.3) (54.8,37.4) (56.2,44.3)): kleine vin schuin omhoog,
# punt zwart, lichte flank
# rugstekels op de rand (model (48.5,24.3) (51.6,29.4) (53.4,33.3) (54.8,37.4) (56.2,44.3)), met de hand op de rand gezet:
# vin naar Tyranitar (punt 1 px zwart, lichte flank links/boven, vulling loopt door in de rand)
RUGSTEK=[[(21,49,'K'),(22,48,'K'),(22,49,'d'),(22,50,'K'),(23,47,'a'),(23,48,'d'),(23,49,'b'),(23,50,'K'),(24,48,'a'),(24,49,'K')],
         [(27,51,'K'),(28,50,'K'),(28,51,'d'),(28,52,'K'),(29,50,'c'),(29,51,'b'),(29,52,'K')],
         [(31,53,'K'),(32,52,'K'),(32,53,'d'),(32,54,'K'),(33,52,'c'),(33,53,'K')],
         [(36,54,'K'),(37,53,'c'),(37,54,'K')],
         [(42,56,'K'),(43,55,'c'),(43,56,'K')]]
# Variant A (Mega Pinsir-vleugel / Ninjask: weinig grote vlakke contrastvormen direct op de basiskleur, geen lijntjes):
# de V-tekens van het model als drie grote V's die naar de punt wijzen (arm omhoog + arm naar links, 2 px dik).
# Variant B (Shuckle / Dustox: ronde vlekken in een regelmatig patroon, met een schaduwrand rechtsonder = bultjes op het schild):
# zeven schorsknobbels in twee rijen langs de lengteas.
def _v(x0,y0,pts,ch='v'): return [(x0+dx,y0+dy,ch) for dx,dy in pts]
VTEKEN=[(0,0),(1,0),(0,-1),(1,-1),(1,-2),(2,-2),(1,-3),(2,-3),(-1,0),(-2,0),(-3,-1),(-4,-1),(-1,1),(0,1),(-2,1),(-3,0)]   # dikke V (2 px), armen 4 px schuin langs de as
KNOBBEL=[(0,0),(1,0),(-1,1),(0,1),(1,1)]; KRING=[(2,1),(0,2),(1,2)]
SCHILDTEKENING={
 'A':_v(43,31,VTEKEN)+_v(47,37,VTEKEN)+_v(50,43,VTEKEN[:8]+[(-1,0),(-2,0),(-1,1),(0,1)]),
 'B':sum([_v(x,y,KNOBBEL)+_v(x,y,KRING,'w') for x,y in ((41,27),(45,29),(42,32),(47,33),(44,37),(49,38),(47,42))],[]),
}
CEL=974/64; SCX,SCY=(723.4-31)/CEL,(470.1-134)/CEL+13                   # schildas (r7, gemeten op het model)
V=-((xx+0.5-SCX)*(-0.847)+(yy+0.5-SCY)*0.532)                           # dwars: + = rechts
T=(xx+0.5-SCX)*0.532+(yy+0.5-SCY)*0.847                                  # lengte: -11 boven .. +13 punt
def schild(o,variant):
    o=o.copy()
    for Y in range(24,48):
        for X in range(XL[Y],W):
            if not BEVROREN[Y,X] and not SM[Y,X] and not RIM[Y,X] and not SIL[Y,X] and X>XR.get(Y,0): o[Y,X]=0
    fig=(o>0)|SM|RIM|SIL
    for Y,X in zip(*np.where(SM)):                                     # basis: lijn links/boven, lichte rand, oker, schaduwrand rechts
        dl=X-XL[Y]; dr=XR[Y]-X
        if Y==24 or dl==0 or (Y==25 and dl==0): o[Y,X]=C['s']
        elif Y==47 or (Y==46 and dl==0): o[Y,X]=C['s']
        elif dr==0 or (Y>=31 and dr<=1) or Y==46: o[Y,X]=C['w']           # schaduwsikkel rechtsonder (breder naar de punt)
        elif dl==1 or (dl==2 and Y<=30) or (Y==25): o[Y,X]=C['o']          # lichte rand linksboven (Ledian), breder bovenaan
        else: o[Y,X]=C['x']
    for X,Y,ch in SCHILDTEKENING[variant]:
        assert SM[Y,X],(X,Y)
        o[Y,X]=C[ch]
    if variant=='A':                                                   # lichte streep langs de bovenkant van elke V (model: licht naast donker)
        vv=set((X,Y) for X,Y,ch in SCHILDTEKENING['A'])
        for X,Y in vv:
            if (X,Y-1) not in vv and SM[Y-1,X] and o[Y-1,X]==C['x']: o[Y-1,X]=C['o']
    for Y,X in zip(*np.where(RIM)): o[Y,X]=C['a']
    for Y,X in zip(*np.where(RIM)):                                    # rugrand: lichte band boven, lijn tegen het schild
        pass
    for Y,X in zip(*np.where(SIL)): o[Y,X]=C['K']
    for Y in range(24,47):                                             # silhouetlijn sluitend maken (trap tussen rijen)
        a,b=XS.get(Y),XS.get(Y+1)
        if a and b and b>a:
            for X in range(a,b): o[Y,X]=C['K'] if o[Y,X]==0 or X>=a else o[Y,X]
    for st in RUGSTEK:
        for Y,X,ch in st:
            assert not BEVROREN[Y,X]; o[Y,X]=C[ch]
    return o

# ======================= opslaan, controles, vel =======================
def opslaan(q,path):
    p=Image.fromarray(q.astype('uint8'),'P'); pal=[v for cc in PAL for v in cc]; p.putpalette(pal+[0]*(768-len(pal))); p.save(path,transparency=0)
OGEN=['A','B']; SCHILDEN=['A','B']; HOOFD=('A','A')
VAR={}
for sv in SCHILDEN:
    q0=schild(FACE0,sv)
    for ov in OGEN:
        q=q0.copy()
        for (Y,X),v in OOG[ov].items(): q[Y,X]=C[v]
        VAR[(ov,sv)]=q; opslaan(q,UIT+'/pinsir_evo_r8_%s_%s.png'%(ov,sv))
def vlekjes(q,ks):
    t=[]
    for k in ks:
        lbq,nq=ndimage.label(q==k,structure=np.ones((3,3)))
        t+=[(k,[(int(x),int(y)) for y,x in np.argwhere(lbq==i)]) for i in range(1,nq+1) if (lbq==i).sum()<3]
    return t
print('controle per variant:')
for (ov,sv),q in VAR.items():
    q2=np.asarray(Image.open(UIT+'/pinsir_evo_r8_%s_%s.png'%(ov,sv)))
    assert (q2==q).all() and Image.open(UIT+'/pinsir_evo_r8_%s_%s.png'%(ov,sv)).info.get('transparency')==0
    bev=int((q[BEVROREN]!=R7[BEVROREN]).sum())
    kaak=np.isin(R7,[8,9,10]) & ~((yy>=26)&(yy<=28)&(xx>=13)&(xx<=26))
    dk=int((q[kaak]!=R7[kaak]).sum())
    mond=(yy>=29)&(yy<=35)&(xx>=15)&(xx<=22); dm=int((q[mond]!=R7[mond]).sum())
    romp=(DEEL=='romp')&(yy>=29); dr=int((q[romp]!=R7[romp]).sum())
    print('  %s_%s: kleuren %d | bevroren arm/been/staart diff %d | kaken diff %d | mond diff %d | romp (rij>=29) diff %d | zwart %.1f%% | tintvlekjes<3px %d'%(
        ov,sv,len(set(q.ravel())),bev,dk,dm,dr,100*(q==1).sum()/(q>0).sum(),len(vlekjes(q,[3,4,5,6,7,12,13,14]))))
    assert bev==0 and dk==0 and dm==0
q=VAR[HOOFD]
print('  pixels anders dan r7 (met stekels):',int((q!=R7S).sum()),'| silhouet anders:',int(((q>0)!=(R7S>0)).sum()))
if 'detail' in sys.argv:
    for k,pts in vlekjes(q,[3,4,5,6,7,12,13,14]): print('   vlekje',CH[k],pts)
if 'raster' in sys.argv:
    print('   '+''.join(str(x%10) for x in range(64)))
    for Y in range(10,62): print('%2d '%Y+''.join(CH[v] for v in q[Y]))
if 'raster' not in sys.argv and 'detail' not in sys.argv:
    sys.path.insert(0,'gereedschap')
    from PIL import ImageDraw
    from vel import rgbp, M
    G3='../../../../graphics/pokemon/'
    def gen3(sp,bg=(255,255,255)):
        im=Image.open(G3+sp+'/anim_front.png'); qq=np.asarray(im)[:64]
        ls=open(G3+sp+'/normal.pal').read().split('\n')[3:19]; pal=np.array([[int(t) for t in l.split()] for l in ls if l.strip()])
        img=np.zeros((64,64,3),'uint8'); img[:]=bg
        for k in range(1,16): img[qq==k]=pal[k]
        return Image.fromarray(img)
    CELm=974/64; MX0,MY0,DYm=31,134,13
    def modelbox(x0,y0,x1,y1,w,h):
        box=(MX0+x0*CELm,MY0+(y0-DYm)*CELm,MX0+x1*CELm,MY0+(y1-DYm)*CELm)
        big=Image.new('RGB',(1300,1300),'white'); big.paste(M,(100,100))
        return big.crop(tuple(int(round(v+100)) for v in box)).resize((w,h),Image.LANCZOS)
    def P(path,bg=(255,255,255)): return rgbp(path,bg)
    f=lambda ov,sv: UIT+'/pinsir_evo_r8_%s_%s.png'%(ov,sv)
    hoofd=P(f(*HOOFD)); r7=P('sprite_r7/pinsir_evo_r7.png')
    Wv=1600; v=Image.new('RGB',(Wv,3000),'white'); d=ImageDraw.Draw(v); y=4
    def kop(t):
        global y; d.text((4,y),t,fill=(0,0,0)); y+=14
    kop('1. hoofdvariant r8 (oog %s, schild %s) | r7 (met stekels) | model op dezelfde maat  (8x)'%HOOFD)
    for i,im in enumerate((hoofd,r7)): v.paste(im.resize((512,512),Image.NEAREST),(i*528,y))
    v.paste(modelbox(0,0,64,64,512,512),(1056,y)); y+=520
    kop('2. ooggebied 12x (x10-30, y21-33): r8 oog A (Pinsir Gen 3 1-op-1, met pupil) | r8 oog B (zelfde, zonder pupil zoals het model) | r7 | r4 oog A | model | Gen 3 Pinsir-ogen (12x)')
    box=(10,21,30,33); z=12
    ims=[P(f('A',HOOFD[1])),P(f('B',HOOFD[1])),r7,P('sprite_r4/pinsir_evo_r4_A.png')]
    x=0
    for im in ims:
        c=im.crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST); v.paste(c,(x,y)); x+=c.width+8
    v.paste(modelbox(*box,(box[2]-box[0])*z,(box[3]-box[1])*z),(x,y)); x+=(box[2]-box[0])*z+8
    c=gen3('pinsir').crop((20,22,36,30)); v.paste(c.resize((c.width*z,c.height*z),Image.NEAREST),(x,y)); y+=(box[3]-box[1])*z+12
    kop('3. dekschild 8x (x34-58, y18-50): A = Mega Pinsir/Ninjask-aanpak (grote vlakke V-vormen) + referenties | B = Shuckle/Dustox-aanpak (knobbels met schaduwrand) + referenties | model')
    box=(34,18,58,50); z=8; x=0
    for sv,refs in (('A',(('pinsir/mega',(0,14,22,40)),('ninjask',(36,8,62,36)))),('B',(('shuckle',(16,24,46,52)),('dustox',(36,22,64,48))))):
        c=P(f(HOOFD[0],sv)).crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST); v.paste(c,(x,y)); d.text((x,y+c.height+2),'schild '+sv,fill=(0,0,0)); x+=c.width+6
        for sp,b in refs:
            c=gen3(sp).crop(b); c=c.resize((c.width*z,c.height*z),Image.NEAREST); v.paste(c,(x,y)); d.text((x,y+c.height+2),sp,fill=(0,0,0)); x+=c.width+6
        if sv=='A': y2=y; y+=(box[3]-box[1])*z+20; x=0
    v.paste(modelbox(*box,(box[2]-box[0])*z,(box[3]-box[1])*z),(x,y)); d.text((x,y+(box[3]-box[1])*z+2),'model',fill=(0,0,0)); y+=(box[3]-box[1])*z+20
    kop('4. stekels 8x: r8 kop/rug (x8-50, y11-26) | Tyranitar (rug) | Tyranitar (staart) | Sandslash (rug)')
    x=0; z=8
    c=hoofd.crop((8,11,50,26)).resize((42*z,15*z),Image.NEAREST); v.paste(c,(x,y)); x+=c.width+8
    for sp,b in (('tyranitar',(26,0,52,30)),('tyranitar',(36,44,64,60)),('sandslash',(10,6,44,30))):
        c=gen3(sp).crop(b); c=c.resize((c.width*z,c.height*z),Image.NEAREST)
        if x+c.width>Wv: break
        v.paste(c,(x,y)); x+=c.width+8
    y+=30*z+16
    kop('5. 1x op wit en donker: r8 AA | AB | BA | BB | r7 | Gen 3 Pinsir | Heracross | Tyranitar        2x: r8 hoofdvariant | r7 | Pinsir | Heracross | Tyranitar')
    for j,bg in enumerate(((255,255,255),(40,48,56))):
        ims=[P(f(o_,s_),bg) for o_ in OGEN for s_ in SCHILDEN]+[P('sprite_r7/pinsir_evo_r7.png',bg)]+[gen3(sp,bg) for sp in ('pinsir','heracross','tyranitar')]
        for i,im in enumerate(ims): v.paste(im,(i*68,y+j*68))
    for i,im in enumerate([hoofd,r7]+[gen3(sp) for sp in ('pinsir','heracross','tyranitar')]): v.paste(im.resize((128,128),Image.NEAREST),(i*134,y+140))
    y+=280
    v=v.crop((0,0,Wv,y)); v.save(UIT+'/vel.png'); print('vel',v.size)

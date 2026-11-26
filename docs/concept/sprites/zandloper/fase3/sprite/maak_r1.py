# Ronde 1: zand-djinn A/B + varianten. Alles uit r5 (basis), r8 (fles, trechter, windingen A, ogen), r10 (barst).
# Toegestaan: weghalen, verschuiven, tinten kiezen, technisch opschonen. Elke andere pixel wordt gelogd.
import numpy as np; from PIL import Image; import json
import bewerk, reduceer2, schoon, lijnweg, ogen, kleur, materiaal as mt, bouw
PAL={0:(0,0,0),1:(16,16,16),
     10:(72,46,16),11:(159,121,55),12:(201,158,75),13:(228,188,101),14:(250,217,140),   # zand: mediaan r5 per band
     20:(69,98,112),21:(117,163,183),22:(159,202,220),23:(219,241,248),                 # glas: mediaan r8-glas per band
     30:(90,58,32),31:(130,86,47),32:(174,121,72)}                                       # hout: r5 (donkerste stap verder uit elkaar gezet)
LOG=[]
def natief(brein,fles,trechter,spier=6):
    a=bewerk.maak(fles,trechter)
    if brein=='A': a=bewerk.brein_r8(a,140)
    else: a=lijnweg.weg(a,bouw.Z_HOOFD,20,drempel=100)   # B: kleine windingen van r5 weg, de grootste (>=20 natieve px) blijven
    if spier: a=lijnweg.weg(a,bouw.Z_LIJF,spier,drempel=100)   # minder spierlijnen: kleinste binnenlijnen (< spier natieve px) weg
    return a
def reductie(a,brein):
    z=bouw.Z_HOOFD
    if brein=='A': return reduceer2.reduceer(a,(2,2),2,z,4,None)[2:66,0:64].copy()
    return reduceer2.reduceer(a,(2,2),2,z,3,None)[2:66,0:64].copy()
# ogen r8: factor-2-verkleining (fase 1,1), rijen 1-3; alleen ooglid (10), pupil (1) en oogwit (23)
OOG=ogen.oog((80,52,106,62),(1,1))[1:4]
LINKS=[(r,c) for r in range(3) for c in range(0,4) if OOG[r,c] in (1,10,23)]
RECHTS=[(r,c) for r in range(3) for c in range(6,12) if OOG[r,c] in (1,10,23)]
def zet_ogen(lab,x0=22,y0=13,dr=0,dy_r=0):
    # r5-oogwit weg (weghalen -> buurtint)
    for y in range(12,18):
        for x in range(21,36):
            if lab[y,x]==23:
                n=schoon.buurtint(lab,(y,x),1,set()) or 12; lab[y,x]=n if n>=10 else 12
    for r,c in LINKS: lab[y0+r,x0+c]=2 if OOG[r,c]==1 else OOG[r,c]       # 2 = pupil (zwart, niet omkleuren)
    for r,c in RECHTS: lab[y0+r+dy_r,x0+c+dr]=2 if OOG[r,c]==1 else OOG[r,c]
    return lab
def barst(lab,ax=27,ay=52):
    """Barstlijnen uit r10 (donkerblauwe lijnen binnen de linkerbol, uitsnede x396-448, y288-412), verkleind met
    factor 24,9 (schaal zandloper r10/r5 = 503/310 x 15,36); een spritepixel is barst bij >= 40 barstpixels (6,5 %).
    Verschoven naar de linkerbol bij de hals, waar het zand eruit komt."""
    a=np.asarray(Image.open('../gemini/r10_onderkant.png').convert('RGB')).astype(float)
    h,s,v=mt.hsv(a); L=a@[0.299,0.587,0.114]
    m=(L<115)&(h>170)&(h<250)
    box=np.zeros(m.shape,bool); box[288:412,396:448]=True; m&=box
    f=503/310*15.36; ys,xs=np.where(m); pts={}
    for y,x in zip(ys,xs):
        p=(int(np.floor((y-288)/f))+ay,int(np.floor((x-396)/f))+ax); pts[p]=pts.get(p,0)+1
    gezet=[]
    for p,c in pts.items():
        if c>=40 and lab[p]//10 in (1,2): lab[p]=20; gezet.append(p)
    return lab,gezet
# r5-barst bij de rechterdop weg (Jordi: "de barst zit op de verkeerde plek"): de dubbele/gekartelde lijn tussen
# glas en dop wordt 1 px; de pixels nemen de tint van het glas/zand ernaast aan (alleen weghalen).
BARST_R5_WEG={(54,37):23,(55,37):23,(56,37):23,(57,35):13,(57,36):13,(57,37):13}
def barst_r5_weg(lab):
    for p,t in BARST_R5_WEG.items(): lab[p]=t
    return lab
def glasspikkels_weg(lab,maxpx=2):
    """Losse glaspixels (restjes van het weggehaalde rugglas bij de snijrand) weghalen -> zand-buurtint."""
    weg=[]
    for c in schoon.comps((lab>=20)&(lab<30)):
        if len(c)>maxpx: continue
        for p in c:
            n=schoon.buurtint(lab,p,1,set(c)); lab[p]=n if n else 1; weg.append(p)
    return lab,weg
def label_png(lab,pad):
    keys=[0,1,10,11,12,13,14,20,21,22,23,30,31,32]
    idx=np.zeros(lab.shape,'uint8'); pal=[]
    for i,k in enumerate(keys): idx[lab==k]=i; pal+=list(PAL[k])
    idx[lab==2]=1
    pal+=[0,0,0]*(16-len(keys))
    im=Image.fromarray(idx,'P'); im.putpalette(pal+[0]*(768-len(pal))); im.save(pad,transparency=0); return im
def bouw_sprite(brein='B',fles=(-8,-14),trechter=(0,-8),oog=dict(),barstplek=(27,52),spier=6):
    a=natief(brein,fles,trechter,spier); lab=reductie(a,brein)
    lab=schoon.tintclusters(lab,3); lab=schoon.losse_lijnen(lab,3)
    lab,gw=glasspikkels_weg(lab); LOG.append(('glasspikkels weg',gw))
    lab=zet_ogen(lab,**oog)
    lab=barst_r5_weg(lab)
    lab,gb=barst(lab,*barstplek)
    lab=bouw.binnenlijnen(bouw.buitenlijn(lab))
    return lab
if __name__=='__main__':
    lab=bouw_sprite('B'); np.save('/tmp/claude-0/r1B.npy',lab); label_png(lab,'/tmp/claude-0/r1B.png')

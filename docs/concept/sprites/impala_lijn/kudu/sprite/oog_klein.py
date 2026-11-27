# Ronde 6, kleine zwarte ogen (Jordi: "alle ogen zijn prutswerk, allemaal te lieflijk, zwarte vlekken of raar gepositioneerd,
# s1 is nog het beste maar ziet er raar uit, kijk naar andere pokemon met kleine zwarte ogen").
# Start = r6/grid.json (oog B). Eerst alle oogpixels van A-D terug naar het lege oogvlak (zelfde regel als oog_streng.py / r6.py),
# dan per variant een oog van een echte Pokemon 1-op-1 (alleen omgekleurd naar het kudupalet), op de modelplek van het oog.
# Geen pixel getekend. Gebruik: python3 oog_klein.py -> r6/kudu_r6_oogK1..png, r6/oog_klein_varianten.png, r6/oog_klein_pixels.txt
import json, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
import oog4
H,W=64,51; x0,p=91,16
GR='../../../../../../graphics/pokemon/'
hx=lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
PAL={'.':(0,0,0),'0':hx('#302418'),'L':hx('#F8D888'),'M':hx('#D8A850'),'D':hx('#A07030'),
     'l':hx('#D8AC30'),'m':hx('#B08824'),'d':hx('#7C5A10'),'A':hx('#4A4A52'),'3':hx('#8A8A92'),'4':hx('#C8C8CC'),
     'W':hx('#FFFFFF'),'R':hx('#E0A090'),'r':hx('#B06A58'),'K':hx('#5C4434')}
ORDER=list(PAL)
B=[list(r) for r in json.load(open('r6/grid.json'))['grid']]
Am=np.asarray(Image.open('r3/model_A3.png').convert('RGB')).astype(int)
R_,G_,B_=Am[...,0],Am[...,1],Am[...,2]; lum=Am@[.299,.587,.114]
LIJN=lum<70; HAAR=(B_<R_*0.31)&(R_>=110)&~LIJN&(lum<200); VACHT=(~HAAR)&~LIJN&(lum<200)&(R_-B_>60)
HALO=nd.binary_dilation(lum>=200,iterations=4)
def cel(x,y): return slice(y*p,(y+1)*p),slice(x0+x*p,x0+(x+1)*p)
def vachttoon(x,y,TD=160):
    s=cel(x,y); m=VACHT[s]&~HALO[s]
    if m.sum()<30: m=VACHT[s]
    l=lum[s][m].mean(); return 'L' if l>=181 else 'M' if l>=TD else 'D'
LEEG=[r[:] for r in B]; OOGCEL=set()
for v in 'ABCD':
    for x,y,c,_ in oog4.variant(v):
        OOGCEL.add((x,y)); wf=(lum[cel(x,y)]>=215).mean()
        LEEG[y][x]='W' if wf>=0.3 else vachttoon(x,y)
# ---- bron: een oog 1-op-1 uit een echte sprite; kaart = bronindex -> kudukleur; indexen buiten de kaart (vacht van de bron) blijven kudu ----
def bron(n,gba,bx0,by0,bx1,by1,kaart,dx,dy):
    a=np.asarray(Image.open(GR+n+('/anim_front_gba.png' if gba else '/anim_front.png')))
    out=[]
    for y in range(by0,by1+1):
        for x in range(bx0,bx1+1):
            c=kaart.get(int(a[y,x]))
            if c: out.append((x+dx,y+dy,c,'%s bronpixel (%d,%d) index %x'%(n,x,y,a[y,x])))
    return out
# Modelplek (oog_streng.md): spleet rij 22 (x 10-13), pupil rij 23 (x 11-12); wenkbrauw D op rij 21 blijft (modelvacht).
# Elk oog komt met zijn zwarte kern op de modelpupil (x 11-12, rij 22-23), zonder modellid erover.
VAR={}
# K1 Sawsbuck (Gen 5, hert): 1 px breed zwart, lichtgrijs ervoor, grijs erachter; daaronder zwart + donkerrood. Geen glans op de pupil.
#   normal.pal: 2 (16,16,16) -> 0; d (216,216,216) -> 4; e (168,168,168) -> 3; 5 (72,16,8) -> K. Bron x20-22 y23-24 -> dx -9, dy -1.
#   (Het bronoog staat schuin: rij 23 = d 2 e (x20-22), rij 24 = 2 5 (x20-21).)
VAR['K1']=('Sawsbuck (hert, Gen 5): smal zwart oog, lichtgrijs ervoor', 'sawsbuck',0,(16,20,24,27),
           bron('sawsbuck',0,20,23,22,24,{2:'0',13:'4',14:'3',5:'K'},-9,-1))
# K2 Wailord (Gen 3): 1x2 zwart met donkere rand erachter, geen glans.
#   9 (41,82,197) donkere lijftint -> D; a (49,57,90) -> K; d (0,0,0) -> 0. Bron x29-30 y14-15 -> dx -18, dy +8.
VAR['K2']=('Wailord (Gen 3): 1x2 zwart, donkere rand erachter, geen glans', 'wailord',1,(25,11,34,18),
           bron('wailord',1,29,14,30,15,{13:'0',9:'D',10:'K'},-18,8))
# K3 Kabuto (Gen 1): zwart 2x2 met glans rechtsboven, donkere rand aan beide kanten.
#   d (156,106,8) -> D; f (16,16,16) -> 0; 1 wit -> W. Bron x32-35 y20-21 -> dx -21, dy +2.
VAR['K3']=('Kabuto (Gen 1): klein zwart oog, glans rechtsboven, donkere rand', 'kabuto',1,(27,16,39,24),
           bron('kabuto',1,32,20,35,21,{13:'D',15:'0',1:'W'},-21,2))
# K4 Bidoof (Gen 4): 3 zwarte pixels met donkerbruine rand links, geen glans.
#   1 (64,48,16) -> K; 5 (16,16,16) -> 0; 2 (152,96,48) -> D. Bron x45-47 y27-28 -> dx -35, dy -5.
VAR['K4']=('Bidoof (Gen 4): 3 zwarte pixels, donkere rand, geen glans', 'bidoof',0,(40,23,51,31),
           bron('bidoof',0,45,27,47,28,{1:'K',5:'0',2:'D'},-35,-5))
# ---- Afgevallen na eigen keuring (niet gebouwd) ----
# # K3 Yungoos (Gen 7): zware wenkbrauw boven een klein zwart oog met lichtpunt in de bovenrij.
# #   3 (112,56,48) wenkbrauw -> K; 8 (64,56,56) -> K; 9 (248,248,248) -> W; a (16,16,16) -> 0. Bron x6-7 y33-36 -> dx +5, dy -12.
# VAR['K3']=('Yungoos (Gen 7): zware wenkbrauw, klein zwart oog', 'yungoos',0,(2,30,12,39),
#            bron('yungoos',0,6,33,7,36,{3:'K',8:'K',9:'W',10:'0'},5,-12))
# # K6 Ampharos (Gen 2, linkeroog): 2x2 zwart met glans linksboven.
# #   a (16,16,16) -> 0; 1 wit -> W. Bron x10-11 y16-17 -> dx +1, dy +6.
# VAR['K6']=('Ampharos (Gen 2): 2x2 zwart, glans linksboven', 'ampharos',1,(5,12,17,21),
#            bron('ampharos',1,10,16,11,17,{10:'0',1:'W'},1,6))
# Yungoos: wenkbrauw + oog = 7 donkere px onder elkaar, op 1x een donkere veeg (zwarte vlek); vervangt ook de modelwenkbrauw.
# Ampharos: 2x2 met glans linksboven = het klassieke ronde snoezige oog (zelfde soort als Ponyta B): te lief.
OX=(64-W)//2
def bouw(px):
    g=[r[:] for r in LEEG]
    for x,y,c,_ in px: g[y][x]=c
    return g
def png(G,pad):
    img=np.zeros((64,64),'uint8')
    for y in range(H):
        for x in range(W): img[y,OX+x]=ORDER.index(G[y][x])
    pal=[v for k in ORDER for v in PAL[k]]; pal+=[0]*(48-len(pal))
    im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(pad,transparency=0)
def rgb(G,bg=(170,200,230)):
    a=np.zeros((H,W,3),'uint8')
    for y in range(H):
        for x in range(W): a[y,x]=bg if G[y][x]=='.' else PAL[G[y][x]]
    return a
def bronbeeld(n,gba,box):
    im=Image.open(GR+n+('/anim_front_gba.png' if gba else '/anim_front.png')); a=np.asarray(im)[:64]
    f=open(GR+n+('/normal_gba.pal' if gba else '/normal.pal')).read().split('\n')[3:19]
    P=np.array([[int(v) for v in l.split()[:3]] for l in f if len(l.split())>=3]+[[0,0,0]]*16,'uint8')[:16]
    r=P[a].copy(); r[a==0]=(170,200,230); x0_,y0_,x1_,y1_=box
    return Image.fromarray(r[y0_:y1_,x0_:x1_])
if __name__=='__main__':
    items=[]; log=open('r6/oog_klein_pixels.txt','w')
    for k,(t,n,gba,box,px) in VAR.items():
        g=bouw(px); png(g,'r6/kudu_r6_oog%s.png'%k)
        diff=[(x,y) for y in range(H) for x in range(W) if g[y][x]!=B[y][x]]
        buiten=[d for d in diff if d not in OOGCEL and d not in {(a,b) for a,b,*_ in px}]
        log.write('%s: %s\n  anders dan r6 (oog B): %d px, buiten oogvlak A-D + variant: %d\n'%(k,t,len(diff),len(buiten)))
        for x,y,c,w in px: log.write('  (%d,%d) %s  %s\n'%(x,y,c,w))
        items.append((k+': '+t,g,n,gba,box))
    log.close()
    Z=8; HX0,HX1,HY0,HY1=2,20,14,30
    hw=(HX1-HX0)*Z; bw=max((b[2]-b[0]) for *_,b in items)*Z
    cw=hw+16+bw+16+W*2+16+W+16; ch=max((HY1-HY0)*Z,H*4+8)+42
    V=Image.new('RGB',(2*cw,((len(items)+1)//2)*ch),(255,255,255)); d=ImageDraw.Draw(V)
    for i,(t,g,n,gba,box) in enumerate(items):
        X=(i%2)*cw; Y=(i//2)*ch; a=rgb(g)
        V.paste(Image.fromarray(a[HY0:HY1,HX0:HX1]).resize((hw,(HY1-HY0)*Z),Image.NEAREST),(X,Y+30))
        bb=bronbeeld(n,gba,box); V.paste(bb.resize((bb.size[0]*Z,bb.size[1]*Z),Image.NEAREST),(X+hw+16,Y+30))
        d.text((X+hw+16,Y+18),'bron: %s %s 8x'%(n,'gba' if gba else ''),fill=(90,90,90))
        full=Image.fromarray(a); xx=X+hw+16+bw+16
        V.paste(full.resize((W*2,H*2),Image.NEAREST),(xx,Y+30)); V.paste(Image.fromarray(rgb(g,(40,44,52))).resize((W*2,H*2),Image.NEAREST),(xx,Y+30+H*2+8))
        V.paste(full,(xx+W*2+16,Y+30)); V.paste(Image.fromarray(rgb(g,(40,44,52))),(xx+W*2+16,Y+30+H+8))
        d.text((X,Y+4),t[:100],fill=(0,0,0)); d.text((xx,Y+18),'2x',fill=(90,90,90)); d.text((xx+W*2+16,Y+18),'1x',fill=(90,90,90))
    V.save('r6/oog_klein_varianten.png'); print(open('r6/oog_klein_pixels.txt').read())

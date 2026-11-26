# Hoatzin r12 (alleen B; keurder: tintverdeling naar Murkrow, achterhoofd, een bolling borst+buik, teal ramp, schouders).
# Hoatzin r11 (op r10, punten coordinator): vleugels als Gen 3-veren, snavel als kegel zonder banden, kop-sikkel.
# Hoatzin r10: kleurronde (alleen tinten binnen het silhouet; alpha-diff 0, lijnen K blijven op hun plek).
# Toon per lijfpixel = vorm-licht (bol/kegel/cilinder per zone, licht linksboven) + modelhelderheid per pixel.
# Versie A = r9-donkerte, versie B = een stap lichter in het Murkrow-bereik met hooglicht.
import os,sys,numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,H+'/../r8'); from gemeen import model_op_schaal
r9=np.array(Image.open(H+'/../r9/hoatzin_r9.png'))
md=np.array(model_op_schaal().convert('RGB')).astype(float)
ML=.299*md[...,0]+.587*md[...,1]+.114*md[...,2]
# Helderheid van alleen de zwartige modelpixels (klassen zwart/donker lijf): het geelgroen van teken en
# veerpunten mag het lijf niet oplichten.
from gemeen import laad,vak
_a,_c,_L=laad(); MLD=np.full((64,64),np.nan)
for _y in range(64):
    for _x in range(64):
        _v=vak(_x,_y,_c,_L)
        if _v is None: continue
        cc,ll,w,_=_v; m=(cc==1)|(cc==2)
        if w[m].sum()>0.15: MLD[_y,_x]=(ll[m]*w[m]).sum()/w[m].sum()
LIJF={2,3,4}; GROEN={5,6,7}
LV=np.array([-0.5,-0.6,0.62]); LV/=np.linalg.norm(LV)

def ell(x,y,cx,cy,rx,ry,rot=0):
    dx,dy=x-cx,y-cy
    c,s=np.cos(rot),np.sin(rot)
    u,v=(dx*c+dy*s)/rx,(-dx*s+dy*c)/ry
    r2=min(u*u+v*v,0.97); nz=np.sqrt(1-r2)
    nx,ny=u*c-v*s,u*s+v*c   # terug naar beeldassen
    n=np.array([nx,ny,nz]); n/=np.linalg.norm(n); return float(n@LV)
def bez(t,P):
    P0,P1,P2=P; return (1-t)**2*P0+2*(1-t)*t*P1+t*t*P2
def buis(x,y,P,hw0,hw1,boven):
    """kegel/cilinder langs een gebogen as; boven = 2D-vector naar de bovenkant van de doorsnede"""
    P=[np.array(p,float) for p in P]; q=np.array([x,y],float)
    ts=np.linspace(0,1,201); pts=np.array([bez(t,P) for t in ts]); i=np.argmin(((pts-q)**2).sum(1)); t=ts[i]
    tan=pts[min(i+1,200)]-pts[max(i-1,0)]; tan/=np.linalg.norm(tan)
    perp=np.array([-tan[1],tan[0]])
    if perp@np.array(boven)<0: perp=-perp      # perp wijst naar boven
    hw=hw0*(1-t)+hw1*t; v=np.clip((q-pts[i])@perp/hw,-0.97,0.97)
    n=np.array([perp[0]*v,perp[1]*v,np.sqrt(1-v*v)]); return float(n@LV)


# Kop + snavel: toonniveaus per pixel (0 donker,1 midden,2 licht,3 hooglicht), x 8..26. Het model is hier vlak
# (helderheid 40-80 overal), dus de ronding volgt Murkrow gba: hooglicht als sikkel linksboven op de bol,
# donkere sikkel achter de gezichtsnaad (x23) en onder het oog; snavel = kegel met hooglichtrug langs de bovenkant,
# midden, donkere onderkant tegen de bek-lijn. '.' = niet aanraken (lijn, oog, kuif, buitenrand).
# kop+snavel, x 8..26: lichte sikkel langs de bovenrand en linkerrand van de bol (hooglicht 3 px linksboven), midden binnenin, donkere sikkel rechts (achter de naad x23) en onder het oog; snavel: een doorlopende lichte rugstrook 2 px (punt 1 px) langs de bovenkant, midden, donkere onderkant
HAND_KOP=(8,{
  7 :'.............0.....',
  8 :'..........0000110..',
  9 :'.......332222111100',
  10:'.......32...2111110',
  11:'........22211.11100',
  12:'........22111111000',
  13:'.......221....1.000',
  14:'.......21........00',
  15:'......221......00.0',
  16:'.....2211.......00.',
  17:'....221111....0.00.',
  18:'...221110000000.00.',
  19:'..22110000.000.000.',
  20:'..2110.............',
  21:'.211...............',
  22:'.21................',
  23:'.1.................',
})
# nabije vleugel, x 31..43: smalle gebogen lichte strook langs de voorrand (binnen de selout), hooglicht bovenaan; per veerlijn (K) licht eronder (bovenrand volgende veer) en donker erboven; rechtsonder naar het lijf donker (Swellow/Skarmory gba)
HAND_VL=(31,{
  16:'........2.111',
  17:'.....33.211.1',
  18:'....33321.111',
  19:'...2332111111',
  20:'...222111110.',
  21:'...2111110...',
  22:'....21111122.',
  23:'..2.1111100..',
  24:'..21111110...',
  25:'...211110....',
  26:'...111110....',
  27:'....1110.....',
})
# verre vleugel (achter het lijf), x 8..18: alleen een smalle lichte bovenrand/voorrand, verder overwegend donker
HAND_VV=(8,{
  30:'.....222111',
  31:'....2232.10',
  32:'....22321..',
  33:'...22221110',
  34:'...21111100',
  35:'..2.1111000',
  36:'..111110000',
  37:'..1100000..',
  38:'....111....',
})
# kuifvoet loopt onregelmatig 1-2 px de kop in (kuifkleur O = index 5); geen lijn- of silhouetwijziging
KUIFVOET=[(26,9),(25,10),(26,10),(25,12),(26,12),(26,13)]
HANDEN=[HAND_KOP,HAND_VL,HAND_VV]
def zone(x,y):
    if y>=47 or (y>=46 and x>=26): return 'poot'
    if (x<=16 and 15<=y<=24) or (x<=17 and y in (18,19)): return 'snavel'
    if y<=19 and x<=29: return 'kop'
    if 20<=y<=28 and 17<=x<=26: return 'hals'
    if (x>=29 and y<=29) or (x>=33 and y<=31): return 'vleugel'
    if x>=38 and y>=32: return 'staart'
    if x<=18 and y>=28: return 'vervleugel'
    if (y>=40 and 22<=x<=37) or (y==39 and 22<=x<=27): return 'dij'
    return 'lijf'
def geo(x,y,z):
    if z=='kop': return ell(x,y,21,14,7.5,7.5)+0.12
    if z=='snavel': return buis(x,y,[(19,15),(12.5,16.5),(8.5,23.5)],3.4,1.3,(0.3,-1))
    if z=='hals': return buis(x,y,[(23,18),(22,23),(21,29)],2.8,3.2,(-1,0))*0.9
    if z=='vleugel': return 0.9*ell(x,y,40.5,22.5,9,11,-0.5)
    if z=='staart': return buis(x,y,[(37,38),(46,37),(55,34)],3.2,2.5,(0,-1))
    if z=='vervleugel': return ell(x,y,12.5,35,6.5,7.5,0.3)+0.12
    if z=='dij': return (ell(x,y,28,44,5,4.5)-0.35 if x<=30 else ell(x,y,34,42.5,3.8,3.8))-0.1
    if z=='lijf': return ell(x,y,25,35,13,10.5,0.2)
    return 0
def kaart(drempels,modelw=0.25):
    """lijfpixel -> 2 donker,3 midden,4 licht,10 hooglicht"""
    o=r9.copy(); S=np.full(r9.shape,np.nan); Z={}
    for y in range(64):
        for x in range(64):
            if r9[y,x] not in LIJF: continue
            z=zone(x,y); Z[(y,x)]=z
            if z=='poot': o[y,x]=r9[y,x]; continue
            rand=any(not(0<=y+dy<64 and 0<=x+dx<64) or r9[y+dy,x+dx]==0 for dy,dx in((1,0),(-1,0),(0,1),(0,-1)))
            if rand: o[y,x]=r9[y,x] if r9[y,x]==2 else 2; continue   # buitenrand: selout blijft
            ml=MLD[y,x] if not np.isnan(MLD[y,x]) else 45
            s=geo(x,y,z)+modelw*(ml-55)/40
            S[y,x]=s
            o[y,x]=2 if s<drempels[0] else 3 if s<drempels[1] else 4 if (s<drempels[2] or not (z=='lijf' and ((x-20.4)/1.9)**2+((y-30.6)/1.7)**2<=1)) else 10
            # kuif valt over de kop: pixel direct onder of links naast kuifgroen = schaduw
            if z=='kop' and (y<=8 or r9[y-1,x] in GROEN or (r9[y,x+1] in GROEN and x>=24) or (r9[y-1,x]==1 and y<=10 and r9[y-2,x] in GROEN|{1})):
                o[y,x]=2
    return o,S,Z
def ontkorrel(o,Z,keep=(10,)):
    from collections import Counter
    for _ in range(3):
        for t in (2,3,4,10):
            m=(o==t)
            lab=np.zeros(o.shape,int); n=0
            for y,x in zip(*np.where(m)):
                if lab[y,x]: continue
                n+=1; st=[(y,x)]; lab[y,x]=n
                while st:
                    cy,cx=st.pop()
                    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                        yy,xx=cy+dy,cx+dx
                        if 0<=yy<64 and 0<=xx<64 and m[yy,xx] and not lab[yy,xx]: lab[yy,xx]=n; st.append((yy,xx))
            for k in range(1,n+1):
                pts=list(zip(*np.where(lab==k)))
                if len(pts)>=3 or (t in keep and len(pts)>=2): continue
                if any(Z.get(p)=='poot' for p in pts): continue
                for y,x in pts:
                    if r9[y,x]==2 and t==2 and any(r9[y+dy,x+dx]==0 for dy,dx in((1,0),(-1,0),(0,1),(0,-1))): continue
                    c=Counter(o[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1)) if o[y+dy,x+dx] in (2,3,4,10) and o[y+dy,x+dx]!=t)
                    if c: o[y,x]=c.most_common(1)[0][0]
    return o
PAL_R9=[tuple(Image.open(H+'/../r9/hoatzin_r9.png').getpalette()[3*i:3*i+3]) for i in range(13)]
def palet(lijf,hl):
    p=list(PAL_R9); p[2],p[3],p[4]=lijf; p[10]=hl; return p
VERSIES={
 'B':dict(pal=palet([(38,48,60),(56,70,80),(78,96,104)],(128,150,156)),dr=(-0.05,0.45,0.90),niv=(2,3,4,10)),
}
def opslaan(o,pal,path):
    p=Image.fromarray(o.astype('uint8'),'P'); fl=[v for c in pal for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save(path,transparency=0)
if __name__=='__main__':
    for k,v in VERSIES.items():
        o,S,Z=kaart(v['dr']); o=ontkorrel(o,Z)
        for x0,hand in HANDEN:
          for y,rij in hand.items():
            for i,c in enumerate(rij):
                x=x0+i
                if c=='.' or r9[y,x] not in LIJF: continue
                rand=any(r9[y+dy,x+dx]==0 for dy,dx in((1,0),(-1,0),(0,1),(0,-1)))
                if rand: continue
                o[y,x]=v['niv'][int(c)]
        for x,y in KUIFVOET: o[y,x]=5
        opslaan(o,v['pal'],H+'/hoatzin_r12.png')
        np.save(H+f'/r12_{k}.npy',o)
        from collections import Counter
        c=Counter(o[(o>=2)&(o<=4)|(o==10)].tolist())
        print(k,'alpha-diff',((o>0)!=(r9>0)).sum(),'K-diff',((o==1)!=(r9==1)).sum(),'gewijzigd',(o!=r9).sum(),'lijf',dict(sorted(c.items())),'kleuren',len(np.unique(o)))

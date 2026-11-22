# r7 = vorm van r6 (gereedschap/baltoy_r6_klassen.txt, ongewijzigd) met nieuwe kleur/schaduw naar de studie (sprite_r7/studie.md):
# elk vlak een verloop (licht linksboven -> donker rechtsonder, checker-dither alleen in de overgang), lijnen = vlaktint + 3/4 stappen
# (dus licht in het licht, donker in de schaduw), selout lichtkant varieert mee met het vlak, zwart alleen buiten aan de schaduwkant.
import sys; sys.path.insert(0,'gereedschap'); from r4lib import lees, op, rgba
import numpy as np; from PIL import Image
g=lees('gereedschap/baltoy_r6_klassen.txt'); H,W=len(g),len(g[0])
RAMP=[(246,240,222),(230,222,198),(212,202,176),(196,186,162),(178,168,146),(154,145,128),(128,120,110),(104,97,92),(80,72,70),(40,32,36)]
RED={'Rp':(240,140,124),'R':(220,90,86),'r':(166,52,60)}
nb=lambda y,x: g[y][x] if 0<=y<H and 0<=x<W else '.'
def regio(y,x):
    if y<=1 and x<=21: return 'top'
    if y<=8 and x<=21: return 'band'
    if y<=9 and x>=22: return 'bandzij'
    if y<=17 and x<=20: return 'gezicht'
    if y<=17: return 'gezichtzij'
    if y>=30 and 12<=x<=22: return 'punt'
    if 10<=x<=20 and y<=29: return 'lijf'
    if 21<=x<=24 and y<=29: return 'lijfzij'
    return 'arm'
def vlak(y,x):
    R=regio(y,x)
    if R=='top': return 0.2+(x-8)/13*1.3
    if R=='band': return 1.5+(x-7)/14*1.6+(y-3)/4*0.5+(0.8 if y==8 else 0)
    if R=='bandzij': return 6.6 if y==9 else 4.6+(y-1)/8*0.9+(x-22)/4*0.4
    if R=='gezicht': return 1.3+(x-8)/12*1.9+(y-10)/6*1.0+(1.4 if y==9 else 0)
    if R=='gezichtzij': return 6.2 if y<=10 else 4.9+(y-11)/6*0.8
    if R=='lijf': return 6.4 if y==18 else 4.9 if y==19 else 5.4 if y==29 else 1.0+(x-11)/8*2.4+(y-20)/8*1.6+max(0,(x-15)/4+(y-24)/4-0.6)*1.2   # sikkel naar rechtsonder
    if R=='lijfzij': return 6.8 if y<=19 else 5.6+(y-20)/8*0.8
    if R=='punt': return 6.2 if y==31 else 2.0+(x-15)/5*2.2+(y-32)*0.3
    return None
DITHER=False   # getest: dither op deze maat = ruis in gezicht en lijf; vlakken in treden
def q(v,y,x,dither=True):
    f=v-int(v)
    if dither and DITHER and 0.42<=f<=0.58: return int(v)+((x+y)%2)
    return int(round(v))
out=[[None]*W for _ in range(H)]
oog={(12,x) for x in (8,9,10,11,15,16,17,18)}
for y in range(H):
    for x in range(W):
        c=g[y][x]
        if c=='.': continue
        R=regio(y,x); rand=any(nb(y+a,x+b)=='.' for a,b in((1,0),(-1,0),(0,1),(0,-1)))
        schaduw=nb(y,x+1)=='.' or nb(y+1,x)=='.'
        if R=='arm':
            # cilinder: licht boven/buiten, schaduw aan de onderkant tegen de zwarte rand
            if rand and (c in 'KDdm' or schaduw):
                if c=='K' or schaduw or x>=21: out[y][x]=9
                else: out[y][x]=6 if y>=23 else 5          # selout: iets donkerder naar het uiteinde
                continue
            if c=='l':
                out[y][x]=1 if (x<10 and any(nb(y+a,x+b) in 'md' and (rand or True) for a,b in((-1,0),(0,-1))) and nb(y,x-1)!='l') else 2
            elif c=='M': out[y][x]=5 if any(nb(y+a,x+b)=='K' for a,b in((1,0),(0,1),(0,-1),(-1,0))) else 4
            elif c in 'md': out[y][x]=6
            elif c=='K': out[y][x]=8
            else: out[y][x]=7
            if y<=20: out[y][x]=min(out[y][x]+1,8)           # schouder in de schaduw van de kop
            continue
        v=vlak(y,x)
        if c in 'Rr':
            # rood: hooglicht alleen op de bovenkant van de linkerboog, schaduw rechts en op de punten
            if c=='r' or x>=19 or (y>=12): out[y][x]='r'
            elif y==10 and x in (8,9): out[y][x]='Rp'
            else: out[y][x]='R'
            continue
        if rand and c in 'KDdm' or rand and schaduw:
            if schaduw or c=='K': out[y][x]=9
            else: out[y][x]=min(max(int(round(v))+4,5),7)
            continue
        if (y,x) in oog: out[y][x]=8; continue
        if c in 'KD': out[y][x]=min(int(round(v))+4,8); continue
        if c=='d': out[y][x]=min(int(round(v))+(4 if regio(y,x)=='gezicht' else 3),8); continue
        extra={'h':-0.5,'l':0,'M':1.0,'m':2.0}[c] if R in ('band','gezicht','lijf','top','punt') else {'h':-0.5,'l':-1,'M':-0.5,'m':0}[c]
        out[y][x]=max(0,min(q(v+extra,y,x,R in ('gezicht','lijf','gezichtzij','lijfzij','bandzij')),7))
# keurderpunten r6 (alleen kleur):
for y in range(21,30):                       # rechterarm: schaduwband binnen-onder, buitenkant iets terug, punt naar schaduw
    xs=[x for x in range(21,W) if g[y][x]!='.' and regio(y,x)=='arm']
    if not xs: continue
    ls=[x for x in xs if g[y][x]=='l']
    if ls and len(ls)>=2: out[y][ls[-1]]=3
    if y>=28:
        for x in xs:
            if g[y][x] in 'lM' and out[y][x]!=9: out[y][x]=min(out[y][x]+1,6)
for (y,x),v in {(20,7):3,(20,8):4,(20,9):5,(20,10):5,(21,8):5,(21,9):5}.items(): out[y][x]=v   # linkerschouder: geen dambord
for x in range(13,21):                        # onderrand lijf gelijkmatig
    if g[29][x] in 'lMm': out[29][x]=6
    elif g[29][x] in 'dD': out[29][x]=7
out[24][10]=6; out[12][7]=6                   # losse zwarte pixels in de selout -> selout
# hooglichten op lichte hoeken/randen (studie: Registeel/Probopass)
for y,x in ((1,9),(1,10),(3,8),(32,15)):
    if isinstance(out[y][x],int): out[y][x]=max(0,out[y][x]-1)
keys=['.']+[str(i) for i in range(10)]+list(RED); cols=[(255,255,255)]+RAMP+list(RED.values())
txt=[]
full=np.zeros((64,64),'uint8'); y0=64-H; x0=(64-W)//2
for y in range(H):
    s=''
    for x in range(W):
        o=out[y][x]; k='.' if o is None else str(o) if isinstance(o,int) else o
        s+={'Rp':'P'}.get(k,k); full[y0+y-1 if y0+y-1>=0 else 0,x0+x]=keys.index(k)
    txt.append(s)
open('sprite_r7/baltoy_r7.txt','w').write('\n'.join(txt)+'\n')
for y,s in enumerate(txt): print('%2d %s'%(y,s))
im=Image.fromarray(full,'P'); im.putpalette([v for c in cols for v in c]+[0]*(768-3*len(cols))); im.save('sprite_r7/baltoy_r7.png',transparency=0)
op(rgba(Image.open('sprite_r7/baltoy_r7.png')),(255,255,255,255),8).save('sprite_r7/baltoy_r7_8x.png')
print('kleuren:',len(set(''.join(txt))))

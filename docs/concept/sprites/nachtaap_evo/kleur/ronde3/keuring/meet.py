# Meetscript keuring nachtaap fase 2 ronde 3
import numpy as np
from PIL import Image
from collections import Counter
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_evo/'
a=np.array(Image.open(D+'kleur/ronde3/nachtaap.png'))
H,W=a.shape
op=a>0
print('pixels',op.sum(),'kleuren gebruikt',len(set(a[op].tolist())))
# alpha-diff tegen bevroren silhouet
s=np.load(D+'silhouet/silhouet_bevroren.npy')
s=(s>0) if s.dtype!=bool else s
print('alpha-diff tegen silhouet_bevroren.npy:',int((s!=op).sum()))
txt=[l for l in open(D+'silhouet/silhouet_bevroren.txt').read().split('\n') if l]
t=np.array([[c=='#' for c in l] for l in txt])
print('alpha-diff tegen silhouet_bevroren.txt:',int((t!=op).sum()))
# rand: pixels naast transparant (4-buren)
def nb(y,x):
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        yield a[yy,xx] if 0<=yy<H and 0<=xx<W else 0
rand=Counter(); open_=[]
OUT={1,2,14}  # zwart, omlijningsbasis violet, omlijning creme
for y in range(H):
    for x in range(W):
        if a[y,x] and any(v==0 for v in nb(y,x)):
            rand[int(a[y,x])]+=1
            if a[y,x] not in OUT: open_.append((x,y,int(a[y,x])))
print('randpixels per index',sorted(rand.items()))
print('zwart-aandeel van de rand: %.2f'%(rand[1]/sum(rand.values())))
print('open randen (niet 1/2/E naast transparant):',len(open_)); print(open_)
# losse pixels: kleur die geen enkele 4-buur van dezelfde kleur heeft (binnen de figuur)
lone=[(x,y,int(a[y,x])) for y in range(H) for x in range(W) if a[y,x] and all(v!=a[y,x] for v in nb(y,x))]
print('losse pixels (geen 4-buur met zelfde index):',len(lone)); print(lone)
print('aandeel zwart (idx1) totaal: %.3f'%((a==1).sum()/op.sum()))
# rechte stukken >=4 in de omtrek (horizontaal/verticaal) 
runs=[]
for y in range(H):
    x=0
    while x<W:
        if op[y,x] and ((y==0 or not op[y-1,x]) or (y==H-1 or not op[y+1,x])):
            x0=x
            while x<W and op[y,x] and ((y==0 or not op[y-1,x]) or (y==H-1 or not op[y+1,x])): x+=1
            if x-x0>=4: runs.append(('h',y,x0,x-1,x-x0))
        else: x+=1
for x in range(W):
    y=0
    while y<H:
        if op[y,x] and ((x==0 or not op[y,x-1]) or (x==W-1 or not op[y,x+1])):
            y0=y
            while y<H and op[y,x] and ((x==0 or not op[y,x-1]) or (x==W-1 or not op[y,x+1])): y+=1
            if y-y0>=4: runs.append(('v',x,y0,y-1,y-y0))
        else: y+=1
print('rechte omtrekstukken >=4 (silhouet, bevroren):',runs)
# interne rechte lijnen van zwart/omlijning >=4
ir=[]
for idx in (1,2):
    m=a==idx
    for y in range(H):
        x=0
        while x<W:
            if m[y,x]:
                x0=x
                while x<W and m[y,x]: x+=1
                if x-x0>=5: ir.append((idx,'h',y,x0,x-1))
            else: x+=1
    for x in range(W):
        y=0
        while y<H:
            if m[y,x]:
                y0=y
                while y<H and m[y,x]: y+=1
                if y-y0>=5: ir.append((idx,'v',x,y0,y-1))
            else: y+=1
print('lijnen van idx1/2 >=5 px:',ir)
# symmetrie / kopie ogen
L=a[43:48,6:12]; R_=a[43:48,15:21]
print('linker- en rechteroog identiek:',bool((L==R_).all()))
print('wit (idx8):',int((a==8).sum()),'kop-box px',int(op[36:56,3:27].sum()))
print('creme (C,D,E,F):',int(np.isin(a,[12,13,14,15]).sum()))
print('kene (6,7):',int(np.isin(a,[6,7]).sum()))
# strenger: geen 8-buur met dezelfde index (echte losse stippen)
lone8=[]
for y in range(1,H-1):
    for x in range(1,W-1):
        v=a[y,x]
        if v and not any(a[y+dy,x+dx]==v for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx):
            lone8.append((x,y,'0123456789ABCDEF'[v]))
print('losse stippen (geen 8-buur zelfde index):',len(lone8),lone8)

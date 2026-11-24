# scan.py: controles r8 tegen r7b
import numpy as np; from PIL import Image
A=np.array(Image.open('r7b_basis.png')).astype(int); B=np.array(Image.open('gnometrotter_rock.png')).astype(int)
print('silhouet-diff (alpha):',int(((A>0)!=(B>0)).sum()))
fam={0:'bg',1:'L',2:'S',3:'S',4:'S',5:'S',6:'P',7:'P',8:'P',15:'P',9:'B',10:'B',11:'B',12:'W',13:'W',14:'W'}
LINE={1,2,6,9,4}  # lijnkleuren (4 = baard-lijn)
ch=np.argwhere(A!=B); print('pixels gewijzigd:',len(ch))
famB=dict(fam); famB[12]='B'
ok=lambda a,b: fam[a]==famB[b] or (b==5 and fam[a]=='W')
fx=[(x,y,A[y,x],B[y,x]) for y,x in ch if not ok(A[y,x],B[y,x])]
print('familiewissels (alleen lijn<->lijn toegestaan):',len(fx))
for x,y,a,b in fx: print('  (%d,%d) %X->%X %s'%(x,y,a,b,'ok lijn' if (a in LINE and b in LINE) else 'ok blauw hooglicht' if b==12 else 'ok baard-tint' if (a in (12,13,14) and b==4) or (a==4 and b in (5,13,14)) else 'CHECK'))
# losse pixels: geen 8-buur met dezelfde index (binnen figuur)
H,W=B.shape; los=[]
for y in range(H):
  for x in range(W):
    v=B[y,x]
    if v==0: continue
    n=[B[j,i] for j in range(y-1,y+2) for i in range(x-1,x+2) if (i,j)!=(x,y) and 0<=i<W and 0<=j<H]
    if v not in n: los.append((x,y,'%X'%v))
print('losse pixels:',len(los),los)
# buitenrand: pixels naast transparant (4-buur)
rand=[];
for y in range(H):
  for x in range(W):
    if B[y,x]==0: continue
    if any((not(0<=x+dx<W and 0<=y+dy<H)) or B[y+dy,x+dx]==0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): rand.append((x,y))
nonline=[(x,y,'%X'%B[y,x]) for x,y in rand if B[y,x] not in (1,2,6,9,4)]
print('buitenrand niet-lijnkleur:',len(nonline),nonline)
# om-en-om zwart/lijnkleur langs de rand: patroon 1,L,1,L in 4 opeenvolgende randpixels (8-buren)
rs=set(rand); alt=[]
for x,y in rand:
  for dx,dy in ((1,0),(0,1),(1,1),(1,-1)):
    seq=[(x+k*dx,y+k*dy) for k in range(4)]
    if all(p in rs for p in seq):
      v=[B[q[1],q[0]] for q in seq]
      if all(t in (1,2,6,9,4) for t in v) and v[0]==1 and v[2]==1 and v[1]!=1 and v[3]!=1: alt.append(seq[0])
print('om-en-om 1/lijn op rand:',len(alt),alt)
pal=np.array(Image.open('gnometrotter_rock.png').getpalette()[:48]).reshape(16,3)
print('palet:',[tuple(p) for p in pal])

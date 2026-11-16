# r7: keuring r6c punten 1-4. Basis r6c. Tinten uit modelmetingen; gezicht bevroren.
import numpy as np; from PIL import Image
src=Image.open('r6c.png'); pal=src.getpalette(); o=np.asarray(src).astype(int).copy(); r=o.copy()
MG=np.load('../sprite_r6/modelstats.npy')[0]
FACE=np.zeros((64,64),bool); FACE[9:27,25:42]=True
log={}
def mark(pt,x,y,v):
    assert not FACE[y,x]
    if o[y,x]!=v: log.setdefault(pt,[]).append((x,y,int(o[y,x]),int(v))); o[y,x]=v
def fg(y,x): return 0<=y<64 and 0<=x<64 and o[y,x]>0
# 1: spookwiel 5 -> 4 (model 120-160), alleen waar het model >=115 meet
P1=[(25,47),(30,47),(21,48),(24,48),(25,48),(26,48),(28,48),(29,48),(23,49),(24,49),(25,49),(26,49),(28,49),(29,49),(23,50),(24,50),(27,50),(29,50),(30,50),(23,51),(24,51),(27,51),(23,52),(24,52),(26,52),(28,52),(29,52),(21,53),(24,53),(25,53),(26,53),(24,54),(25,54),(23,55),(28,55)]
for x,y in P1:
    if o[y,x]==5 and MG[y,x]>=115: mark('1 spookwiel 5->4',x,y,4)
# 2+3: roest 10 en plank 8 samen tot één middenbruin (model: front-10 = 104, flank-8 = 88, samen (112,86,64) = 91)
for y,x in zip(*np.where(o==10)): mark('2/3 roest 10 -> 8',x,y,8)
# 4: snippers <3 px opgaan in het vlak: buurtint (geen omlijning) die het dichtst bij de modelhelderheid ligt
def L(i): return 0.3*pal[3*i]+0.59*pal[3*i+1]+0.11*pal[3*i+2]
P4=[(20,39),(20,40),(13,43),(6,43),(5,43),(43,40),(51,41),(52,41),(44,43),(44,44),(46,60),(9,29),(29,38),(35,44),(36,44)]
newpal={8:(118,90,67),13:(78,74,68),9:(54,49,34)}
for i,c in newpal.items(): pal[3*i:3*i+3]=list(c)
for x,y in P4:
    v=o[y,x]; nb={o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and fg(y+dy,x+dx) and o[y+dy,x+dx] not in (1,v)}
    if x<24: nb-={13,11,12}
    if (x,y) in P4 and nb:
        # snipper van 2 px: buur die zelf ook snipper is niet als doel
        t=min(nb,key=lambda i:abs(L(i)-MG[y,x])); mark('4 snippers',x,y,int(t))
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(pal); im.save('sprite.png',transparency=0)
d=o!=r
with open('telling.txt','w') as f:
    for k in sorted(log): s='%s: %d %s'%(k,len(log[k]),log[k]); print(s[:300]); f.write(s+'\n')
    s='palet: 8 (124,94,71)=100 -> (118,90,67)=%.0f; 13 (74,68,60)=69 -> (78,74,68)=%.0f; 9 (61,56,39)=56 -> (54,49,34)=%.0f; 10 ongebruikt'%(L(8),L(13),L(9)); print(s); f.write(s+'\n')
print('totaal',int(d.sum()),'gezicht diff',int(d[FACE].sum()))
Lt=np.array([0]+[L(i) for i in range(1,14)])
print('helderheden',{i:round(Lt[i]) for i in range(1,14)})
print('stappen 7-8 %.0f 8-13 %.0f 13-9 %.0f 9-1 %.0f 8-9 %.0f'%(Lt[7]-Lt[8],Lt[8]-Lt[13],Lt[13]-Lt[9],Lt[9]-Lt[1],Lt[8]-Lt[9]))
z=np.zeros((64,64),bool); z[30:45,36:51]=True; z&=o>0; w=z&np.isin(o,(7,8,9,13))
print('rechterflank sprite %.0f model %.0f; hout/ijzer %.0f model %.0f'%(Lt[o][z].mean(),MG[z].mean(),Lt[o][w].mean(),MG[w].mean()))
fr=np.zeros((64,64),bool); fr[23:44,4:24]=True; fr&=np.isin(o,(7,8,9,10,13)); print('front sprite %.0f model %.0f'%(Lt[o][fr].mean(),MG[fr].mean()))

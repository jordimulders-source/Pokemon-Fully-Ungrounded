# Startraster: groepenkaart (uit het model) + toonkaart als GIDS (licht linksboven).
# Dit geeft alleen een begin; de definitieve tonen staan met de hand in r1.txt.
import numpy as np, os
D=os.path.dirname(os.path.abspath(__file__))
G=[l.rstrip('\n') for l in open(os.path.join(D,'groep.txt'))]
G=np.array([list(r) for r in G])
fig=G!='.'
part=np.full((64,64),'',object)
for y in range(64):
  for x in range(64):
    c=G[y,x]
    if c=='.': continue
    if c=='B': part[y,x]='body'
    elif y<=34 and x>=44: part[y,x]='tail'
    elif y<=48 and x<=28: part[y,x]='head'
    elif x>=42 and y>=44: part[y,x]='hind'
    elif x>=34 and y>=47: part[y,x]='far'
    elif y>=53 and x>=22: part[y,x]='step'
    elif y>=48 and x<=26: part[y,x]='raised'
    else: part[y,x]='head'
def blur(m,r=2):
  p=np.pad(m,r); o=np.zeros_like(m)
  for dy in range(-r,r+1):
    for dx in range(-r,r+1): o+=p[r+dy:r+dy+64,r+dx:r+dx+64]
  return o/((2*r+1)**2)
S=np.zeros((64,64))
for P in ['body','tail','head','hind','far','step','raised']:
  m=(part==P).astype(float)
  h=blur(blur(m,2),1)
  gy,gx=np.gradient(h)
  s=0.55*gx+0.85*gy
  S[part==P]=s[part==P]/max(1e-6,np.abs(s[part==P]).max())
tone={'K':(4,3,2),'B':(7,6,5),'C':(10,9,8)}
out=np.zeros((64,64),int)
for y in range(64):
  for x in range(64):
    c=G[y,x]
    if c=='.': continue
    if c=='#': out[y,x]=1; continue
    if c=='E': out[y,x]=11; continue
    lt,md,sh=tone[c]; s=S[y,x]
    t=md
    if s>0.30: t=lt
    if s<-0.25: t=sh
    if part[y,x]=='far': t=sh
    # rand: grenst aan transparant -> omlijning (schaduwkant) of selout (lichtkant)
    nb=[(0,-1),(-1,0),(1,0),(0,1)]
    edge=[(dx,dy) for dx,dy in nb if not(0<=x+dx<64 and 0<=y+dy<64) or G[y+dy,x+dx]=='.']
    if edge:
      lit=all(d in [(0,-1),(-1,0)] for d in edge)
      t=1
      if lit and c=='B': t=5
      if lit and c=='C': t=8
    out[y,x]=t
open(os.path.join(D,'start.txt'),'w').write('\n'.join(''.join('0123456789ABCDEF'[v] for v in r) for r in out)+'\n')
open(os.path.join(D,'deel.txt'),'w').write('\n'.join(''.join({'':'.','body':'b','tail':'t','head':'h','hind':'H','far':'f','step':'s','raised':'r'}[part[y,x]] for x in range(64)) for y in range(64))+'\n')

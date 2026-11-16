import random,sys
from PIL import Image
from collections import Counter
im=Image.open('../sprite_r25/sprite.png');A=im.load();p=im.getpalette()
L0={i:.299*p[3*i]+.587*p[3*i+1]+.114*p[3*i+2] for i in range(16)}
pc=Counter()
for y in range(64):
  for x in range(64):
    for dx,dy in((1,0),(0,1)):
      if x+dx<64 and y+dy<64:
        a,b=A[x,y],A[x+dx,y+dy]
        if a!=b and a and b: pc[tuple(sorted((a,b)))]+=1
FREE=[2,3,4,5,6,7,8,9,10,11,12,14]
def run(bounds,w_dev=0.02,seed=0):
    random.seed(seed)
    L=dict(L0)
    for i,(lo,hi) in bounds.items(): L[i]=min(max(L[i],lo),hi)
    def cost(L):
        c=0
        for (a,b),n in pc.items():
            d=abs(L[a]-L[b])
            if d<20: c+=n*(1+ (20-d)/20)
            elif d<26: c+=n*0.1*(26-d)/6
        c+=w_dev*sum((L[i]-L0[i])**2 for i in FREE)
        return c
    best=cost(L)
    for it in range(60000):
        i=random.choice(FREE);lo,hi=bounds.get(i,(0,255))
        old=L[i];L[i]=min(max(old+random.uniform(-15,15),lo),hi)
        c=cost(L)
        if c<=best: best=c
        else: L[i]=old
    return L,best

import numpy as np; from PIL import Image
o=np.load('r15w/o0.npy'); line=np.load('r15w/line.npy')
pal=Image.open('r14.png').getpalette(); P=np.array(pal[:48]).reshape(16,3)
fg=o>0
def bg_adj(j,i): return any(not fg[j+dy,i+dx] for dy in(-1,0,1) for dx in(-1,0,1))
outer=np.array([[fg[j,i] and bg_adj(j,i) for i in range(64)] for j in range(64)]) if True else None
B=line.copy().astype(np.uint8)
def zs(B,keep):
  ch=True
  while ch:
    ch=False
    for st in (0,1):
      rm=[]
      for y in range(1,63):
        for x in range(1,63):
          if not B[y,x] or keep[y,x]: continue
          Q=[B[y-1,x],B[y-1,x+1],B[y,x+1],B[y+1,x+1],B[y+1,x],B[y+1,x-1],B[y,x-1],B[y-1,x-1]]
          b=sum(Q); a=sum((Q[k]==0 and Q[(k+1)%8]==1) for k in range(8))
          if 2<=b<=6 and a==1:
            if st==0 and Q[0]*Q[2]*Q[4]==0 and Q[2]*Q[4]*Q[6]==0: rm.append((y,x))
            if st==1 and Q[0]*Q[2]*Q[6]==0 and Q[0]*Q[4]*Q[6]==0: rm.append((y,x))
      for y,x in rm: B[y,x]=0
      if rm: ch=True
  return B.astype(bool)
thin=zs(B,outer)
o2=o.copy()
icet=[2,3,4,5]  # W L M D indices in r14-palet? controleer
names={tuple(P[k]):k for k in range(16)}
W,L,M,D=[names[c] for c in [(238,248,250),(206,228,238),(166,198,220),(128,164,194)]]
for j,i in zip(*np.where(line&~thin)):
  # weggehaalde lijnpixel: kleur van niet-lijn ijsburen in het model
  nb=[o[j+dy,i+dx] for dy in(-1,0,1) for dx in(-1,0,1) if not line[j+dy,i+dx] and o[j+dy,i+dx] in (W,L,M,D)]
  o2[j,i]=max(set(nb),key=nb.count) if nb else M
np.save('r15w/o1.npy',o2); np.save('r15w/thin.npy',thin)
im=Image.fromarray(o2.astype(np.uint8)).convert('P'); im.putpalette(pal); im.save('r15w/o1.png',transparency=0)
im.convert('RGB').resize((512,512),Image.NEAREST).save('r15w/o1_8x.png')
print('lijn',line.sum(),'dun',thin.sum())

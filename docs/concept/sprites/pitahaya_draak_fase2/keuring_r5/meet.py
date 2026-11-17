from PIL import Image; import numpy as np

def label(m):
  lab=np.zeros(m.shape,int); n=0
  for y,x in zip(*np.nonzero(m)):
    if lab[y,x]: continue
    n+=1; st=[(y,x)]; lab[y,x]=n
    while st:
      cy,cx=st.pop()
      for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        ny,nx=cy+dy,cx+dx
        if 0<=ny<64 and 0<=nx<64 and m[ny,nx] and not lab[ny,nx]: lab[ny,nx]=n; st.append((ny,nx))
  return lab,n
def dil(m):
  p=np.pad(m,1); o=np.zeros_like(m)
  for dy in range(3):
    for dx in range(3): o|=p[dy:dy+64,dx:dx+64]
  return o
s=np.array(Image.open('sprite_r5/pitahaya2_r5.png'))
names={1:'K',2:'d',3:'r',4:'p',5:'P',6:'g',7:'G',8:'h',9:'H',10:'w',11:'W',12:'s',13:'v'}
bg=s==0
edge=dil(bg)&~bg
for i in range(1,14):
  m=s==i; print(names[i],'n',m.sum(),'op rand',(m&edge).sum())
# kleine clusters per index (4-conn)
print('clusters <3 px:')
for i in range(1,14):
  lab,n=label(s==i)
  for k in range(1,n+1):
    pts=np.argwhere(lab==k)
    if len(pts)<3: print(' ',names[i],[(int(x),int(y)) for y,x in pts])
# zwart binnen figuur
inner=~bg&~edge
print('zwart binnen (niet buitenrand):',((s==1)&inner).sum(),'van',(~bg).sum(), 'zwart totaal',(s==1).sum())
# dambord: 2x2 met diagonaal gelijke, verschillend
cb=0
for y in range(63):
  for x in range(63):
    a,b,c,d=s[y,x],s[y,x+1],s[y+1,x],s[y+1,x+1]
    if a==d and b==c and a!=b and 0 not in (a,b): cb+=1; 
print('dambord-2x2:',cb)

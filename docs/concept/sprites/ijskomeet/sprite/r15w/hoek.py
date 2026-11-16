# trapjes in binnennaden: hoekpixels weg zodat de lijn 8-verbonden 1 px dun wordt
import numpy as np; from PIL import Image
o=np.load('r15w/o1.npy'); thin=np.load('r15w/thin.npy')
pal=Image.open('r14.png').getpalette(); P=np.array(pal[:48]).reshape(16,3)
names={tuple(P[k]):k for k in range(16)}
W,L,M,D=[names[c] for c in [(238,248,250),(206,228,238),(166,198,220),(128,164,194)]]
fg=o>0
outer=np.array([[fg[j,i] and any(not fg[j+dy,i+dx] for dy in(-1,0,1) for dx in(-1,0,1)) for i in range(64)] for j in range(64)])
L_=thin.copy(); rm=0
for _ in range(3):
  for j in range(1,63):
    for i in range(1,63):
      if not L_[j,i] or outer[j,i]: continue
      n4=[(dy,dx) for dy,dx in((-1,0),(1,0),(0,-1),(0,1)) if L_[j+dy,i+dx]]
      n8=[(dy,dx) for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and L_[j+dy,i+dx]]
      if len(n8)==2 and len(n4)==2:
        (a1,b1),(a2,b2)=n4
        if a1!=a2 and b1!=b2:   # loodrecht: hoek van een trapje
          L_[j,i]=False; rm+=1
          nb=[o[j+dy,i+dx] for dy in(-1,0,1) for dx in(-1,0,1) if not L_[j+dy,i+dx] and o[j+dy,i+dx] in (W,L,M,D)]
          o[j,i]=max(set(nb),key=nb.count) if nb else M
print('hoekpixels weg',rm)
np.save('r15w/o2.npy',o); np.save('r15w/naad.npy',L_)
im=Image.fromarray(o.astype(np.uint8)).convert('P'); im.putpalette(pal); im.save('r15w/o2.png',transparency=0)
im.convert('RGB').resize((512,512),Image.NEAREST).save('r15w/o2_8x.png')

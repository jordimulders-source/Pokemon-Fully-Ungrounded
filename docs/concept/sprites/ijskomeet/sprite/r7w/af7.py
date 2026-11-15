import sys; sys.path.insert(0,'r7w'); sys.path.insert(0,'r6w')
from zones import *
import p6
o=np.load('r7w/s2.npy'); b=np.load('r7w/body2.npy'); ot=np.load('r7w/outer2.npy')
fixed=[]
for j in range(1,63):
  for i in range(1,63):
    if not b[j,i] or ot[j,i] or CH[o[j,i]] not in 'WLMD': continue
    n4=[o[j+dy,i+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
    dg=[o[j+dy,i+dx] for dy,dx in ((1,1),(-1,-1),(1,-1),(-1,1))]
    if o[j,i] in n4 or o[j,i] in dg: continue
    f=[v for v in n4 if CH[v] in 'WLMD']
    if f: o[j,i]=max(set(f),key=f.count); fixed.append((j,i))
print('opgeruimd',fixed)
np.save('r7w/r7.npy',o); p6.to_txt(o,'r7.txt')
im=Image.fromarray((o+1).astype('uint8'),'P'); pal=[255,255,255]+[v for c in p6.PAL for v in c]
im.putpalette(pal+[0]*(768-len(pal))); im.save('r7.png',transparency=0)
r=Image.open('r7.png').convert('RGBA').resize((512,512),0); bg=Image.new('RGBA',r.size,(255,255,255,255)); bg.alpha_composite(r); bg.convert('RGB').save('r7_8x.png')

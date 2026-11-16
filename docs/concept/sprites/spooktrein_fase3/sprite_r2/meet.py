# Metingen sprite: kleuren, zwart-percentage buitenlijn (geheel en alleen vaste delen), kleine tintclusters.
import numpy as np; from PIL import Image
im=Image.open('sprite.png'); o=np.array(im); H,W=o.shape
print('modus',im.mode,'transparantie-index',im.info.get('transparency'),'kleuren incl transparant',len(np.unique(o)))
N4=[(0,1),(1,0),(0,-1),(-1,0)]
edge=[(y,x) for y in range(H) for x in range(W) if o[y,x] and any(not(0<=y+dy<H and 0<=x+dx<W) or o[y+dy,x+dx]==0 for dy,dx in N4)]
v=[int(o[p]) for p in edge]; vast=[t for t in v if t!=6]
print('buitenrand',len(v),'px, zwart %.0f%%'%(100*v.count(1)/len(v)),'| zonder bleekgroen (wolken/geest): zwart %.0f%% van %d'%(100*vast.count(1)/max(1,len(vast)),len(vast)))
lab=np.zeros_like(o,int);n=0;klein={}
for y in range(H):
    for x in range(W):
        if o[y,x] and not lab[y,x]:
            n+=1;st=[(y,x)];lab[y,x]=n;c=[]
            while st:
                cy,cx=st.pop();c.append((cy,cx))
                for dy,dx in N4+[(1,1),(1,-1),(-1,1),(-1,-1)]:
                    ny,nx=cy+dy,cx+dx
                    if 0<=ny<H and 0<=nx<W and o[ny,nx]==o[y,x] and not lab[ny,nx]: lab[ny,nx]=n;st.append((ny,nx))
            if len(c)<3: klein.setdefault(int(o[y,x]),[]).append(c[0][::-1])
print('clusters < 3 px (8-buren) per index (x,y):',{k:len(v) for k,v in klein.items()}); print(klein)

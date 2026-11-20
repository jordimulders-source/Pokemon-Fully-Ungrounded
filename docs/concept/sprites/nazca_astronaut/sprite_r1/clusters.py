# Tintvlakjes < 3 px (4-buren, zelfde rol), buiten ogen/glans/lijnen
import numpy as np
o=np.array([list(l.rstrip('\n')[3:]) for l in open('rollen_hand.txt') if l.strip()]); H,W=o.shape
seen=np.zeros((H,W),bool); res=[]
for j in range(H):
    for i in range(W):
        if seen[j,i] or o[j,i] in '.K': continue
        st=[(j,i)]; comp=[]
        while st:
            y,x=st.pop()
            if 0<=y<H and 0<=x<W and not seen[y,x] and o[y,x]==o[j,i]:
                seen[y,x]=True; comp.append((y,x)); st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
        if len(comp)<3 and not (8<=j<=12 and o[j,i] in 'WBb') and o[j,i] not in 'gS': res.append((o[j,i],comp))
for r in res: print(r)
print(len(res))

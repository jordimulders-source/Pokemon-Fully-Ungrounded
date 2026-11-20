# Klassen (schoon.npy) -> rollenraster voor Gen 3-kleur. Vorm verandert niet: alleen welke tint elke pixel krijgt.
# Rollen: . transp | K lijn zwart | S selout/binnenlijn creme | 1 2 3 g kop donker/midden/licht/glans
#         L M D creme licht/midden/schaduw | B b blauw licht/donker | R r rood/donker | W w wit/witschaduw
import numpy as np
g=np.load('schoon.npy'); H,W=g.shape; o=np.full((H,W),'.',dtype='<U1')
def bgat(j,i): return not(0<=j<H and 0<=i<W) or g[j,i]=='.'
KOP=lambda j,i: j<=19 and i>=7
# kop: bol, licht linksboven
cy,cx,rad=9.6,17.6,10.8
Lv=np.array([-0.5,-0.6,0.62]); Lv/=np.linalg.norm(Lv)
for j in range(H):
    for i in range(W):
        c=g[j,i]
        if c=='.': continue
        if KOP(j,i) and c in 'kK':
            if c=='K' and any(bgat(y,x) for y,x in ((j+1,i),(j-1,i),(j,i+1),(j,i-1))): o[j,i]='K'; continue
            x=(i-cx)/rad; y=(j-cy)/rad; z=np.sqrt(max(0,1-x*x-y*y)); s=np.dot([x,y,z],Lv)
            o[j,i]='g' if s>0.985 else '3' if s>0.86 else '2' if s>0.45 else '1'; continue
        if c in 'Ko':
            edge=[(y,x) for y,x in ((j,i-1),(j-1,i),(j,i+1),(j+1,i)) if bgat(y,x)]
            if not edge:  # binnenlijn
                o[j,i]='S'; continue
            lit=any(x<i or y<j for y,x in edge) and not any(x>i or y>j for y,x in edge)
            if lit:
                # naast welke kleur? selout in de donkere tint van het vlak ernaast
                nbs=[g[y,x] for y,x in ((j,i+1),(j+1,i),(j,i-1),(j-1,i)) if 0<=y<H and 0<=x<W and g[y,x] not in '.Ko']
                f=nbs[0] if nbs else 'Y'
                o[j,i]={'B':'b','b':'b','R':'r','W':'w'}.get(f,'S')
            else: o[j,i]='K'
            continue
        o[j,i]={'Y':'M','y':'D','B':'B','b':'b','R':'R','W':'W','k':'1'}.get(c,'?')
# creme volume: per rij-run de eerste pixel na de lichte kant licht (run >=3)
for j in range(H):
    i=0
    while i<W:
        if o[j,i] in 'MD':
            k=i
            while k<W and o[k if False else j,k] in 'MD': k+=1
            run=k-i
            licht=(i==0) or o[j,i-1] in 'SK.'   # alleen waar de run aan de lichte buitenkant begint
            if licht and run>=3 and o[j,i]=='M': o[j,i]='L'
            if licht and run>=7 and o[j,i+1]=='M': o[j,i+1]='L'
            i=k
        else: i+=1
np.save('rollen.npy',o)
for j,r in enumerate(o): print('%2d '%j+''.join(r))

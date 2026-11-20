# Handwerk (alleen kleur, geen vorm): kopglans/hooglicht met de hand gezet. Schrijft rollen_hand.txt.
import numpy as np
o=np.load('rollen.npy'); voor=o.copy()
KOP={1:(15,"333222"),2:(11,"2333333322222"),3:(10,"233gg3333222221"),4:(10,"233g333332222211"),
     5:(9,"223333333222221111"),6:(9,"222333332222221111"),7:(9,"222233322222211111")}
for j,(i0,s) in KOP.items():
    for k,ch in enumerate(s):
        assert o[j,i0+k] in '123g', (j,i0+k,o[j,i0+k]); o[j,i0+k]=ch
d=(o!=voor); print('handpixels (alleen kleur, kop):',d.sum())
open('rollen_hand.txt','w').write('\n'.join('%2d '%j+''.join(r) for j,r in enumerate(o))+'\n')
# --- ruis: tintvlakjes < 3 px binnen dezelfde kleurgroep opgaan in de meest voorkomende buurtint van die groep
GROEP={'L':'LMD','M':'LMD','D':'LMD','B':'Bb','b':'Bb','R':'Rr','r':'Rr','1':'123','2':'123','3':'123'}
H,W=o.shape
def isbg(y,x): return not(0<=y<H and 0<=x<W) or o[y,x]=='.'
def rand(y,x): return any(isbg(y+a,x+b) for a,b in ((1,0),(-1,0),(0,1),(0,-1)))
voor2=o.copy()
for ronde in range(3):
    seen=np.zeros((H,W),bool)
    for j in range(H):
        for i in range(W):
            c=o[j,i]
            if seen[j,i] or c not in 'BbRr123M' or (8<=j<=12 and 9<=i<=23): continue
            st=[(j,i)]; comp=[]
            while st:
                y,x=st.pop()
                if 0<=y<H and 0<=x<W and not seen[y,x] and o[y,x]==c:
                    seen[y,x]=True; comp.append((y,x)); st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
            if len(comp)>=3 or any(rand(y,x) for y,x in comp): continue
            tel={}
            for y,x in comp:
                for a,b in ((1,0),(-1,0),(0,1),(0,-1)):
                    if 0<=y+a<H and 0<=x+b<W:
                        n=o[y+a,x+b]
                        if n!=c and n in GROEP[c]: tel[n]=tel.get(n,0)+1
            if tel:
                n=max(tel,key=tel.get)
                for y,x in comp: o[y,x]=n
d2=(o!=voor2); print('ruis opgeschoond (alleen tint binnen kleurgroep):',d2.sum(), [ (int(y),int(x)) for y,x in zip(*np.where(d2))])
# --- zigzag: onderrand van elke band in de donkere tint (schaduw onder de band), rest licht; alleen tint, vorm uit het model
voor3=o.copy()
for j in range(23,32):
    for i in range(12,22):
        if o[j,i] in 'Bb' and not rand(j,i):
            o[j,i]='b' if (j+1<H and o[j+1,i] not in 'Bb') else 'B'
print('zigzagtint (onderrand donker):',(o!=voor3).sum())
open('rollen_hand.txt','w').write('\n'.join('%2d '%j+''.join(r) for j,r in enumerate(o))+'\n')

# Kale reductie: natief raster -> indexen van het oude palet (per kleurgroep op helderheid), figuur verschoven naar onderkant y55
from PIL import Image; import numpy as np, sys
a=np.asarray(Image.open('r1/natief.png')).astype(int)
H,W,_=a.shape
L=0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2]
mx=a.max(2); mn=a.min(2)
white=(mn>232)&(mx-mn<14)
# achtergrond = flood fill van de rand over (bijna) wit
bg=np.zeros((H,W),bool); st=[(0,0)]
while st:
    y,x=st.pop()
    if 0<=y<H and 0<=x<W and not bg[y,x] and white[y,x]:
        bg[y,x]=True; st+= [(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
idx=np.zeros((H,W),int)
for y in range(H):
    for x in range(W):
        if bg[y,x]: continue
        r,g,b=a[y,x]; l=L[y,x]
        if r>g+28 and abs(r-b)<15 and l<55: v=14            # pupil
        elif l<45: v=1                                       # omlijning
        elif r>g+35 and b>g and r>b-5:                               # roze/oog
            v=9 if l<95 else 10 if l<140 else 11
        elif l>200 and b>g+5: v=12                           # oogwit
        elif r-b>15 and l>150:                               # creme
            v=8 if l>239 else 7 if l>200 else 6
        elif r-b>15 and r>g: v=13                            # bruin
        elif abs(r-g)<20 and abs(g-b)<20: v=1 if l<172 else 0     # grijze randcellen (half lijn, half wit)
        else:                                                # paars
            v=5 if l>=118 else 4 if l>=94 else 3 if l>=64 else 2
        idx[y,x]=v
np.save('r1/kaal_natief.npy',idx)
S='.123456789ABCDEF'
for y in range(17,58): print('%2d '%y+''.join('?' if v<0 else S[v] if v else '.' for v in idx[y,12:53]))

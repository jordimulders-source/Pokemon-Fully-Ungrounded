# Kale reductie: natief raster (r1/natief.png) -> indexen van het oude palet, per kleurgroep op helderheid.
# Achtergrond = floodfill vanaf de rand over (bijna) wit; wit binnen de figuur blijft wit (8).
# Figuur 2 px omlaag geschoven (onderkant y62, zoals de oude sprite) -> r1/kaal.npy (64x64)
import sys; sys.path.insert(0,'r1'); from pal import *
a=np.asarray(Image.open('r1/natief.png')).astype(int)
H,W,_=a.shape
L=0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2]
r,gg,b=a[...,0],a[...,1],a[...,2]
white=(a.min(2)>232)
bg=np.zeros((H,W),bool); st=[(0,0)]
white_ff=white.copy(); white_ff[40,3]=False   # lijngat links in de kop (natief (3,40)) alleen voor de floodfill dicht

while st:
    y,x=st.pop()
    if 0<=y<H and 0<=x<W and not bg[y,x] and white_ff[y,x]:
        bg[y,x]=True; st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
PL={i:0.3*c[0]+0.59*c[1]+0.11*c[2] for i,c in enumerate(PAL)}
def near(l,ids): return min(ids,key=lambda i:abs(PL[i]-l))
idx=np.zeros((H,W),int)
for y in range(H):
    for x in range(W):
        if bg[y,x]: continue
        R,G,B=a[y,x]; l=L[y,x]
        if white[y,x]: v=8
        elif B>R+25 and G>R+10: v=15                       # lichtblauwe rugwiggen
        elif R>G+50 and R>B+15: v=near(l,[9,10,11])         # rood oog
        elif R>B+12 and G>B-5 and l>60: v=near(l,[13,12,14]) if l>95 else 14   # creme/bruin tenen
        else: v=near(l,[1,2,3,4,5,6,7,8])                  # paars/lijn
        idx[y,x]=v
g=np.zeros((64,64),int); g[2:2+H-1,0:W]=idx[0:H-1,:]       # 2 px omlaag
np.save('r1/kaal.npy',g)
if __name__=='__main__': toon(g,0,64,7,64)

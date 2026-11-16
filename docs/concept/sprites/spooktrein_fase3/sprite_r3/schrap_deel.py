# Onderdeel (uitsnede van het natieve model) verkleinen door te SCHRAPPEN, met lijnbescherming:
# een rij/kolom mag alleen weg als hij (bijna) gelijk is aan een buur (egaal vlak); rijen/kolommen met lijnpixels
# (zwart, donkergroen, donkerbruin) die niet in de buurlijn terugkomen kosten extra. Daarna kwantiseren naar het
# r1-palet binnen de eigen kleurgroep. Gebruik als module: verklein(x0,x1,y0,y1,W,H) -> (indexarray, kolommen, rijen)
import numpy as np, colorsys; from PIL import Image
NAT=np.asarray(Image.open('../model/natief.png').convert('RGB')).astype(int)
PAL=np.array(Image.open('../sprite_r1/sprite.png').getpalette()[:39]).reshape(-1,3)
GIDX={0:[1],1:[2,3],2:[4,5,6],3:[7,8,9],4:[10,11,12]}
def groep(p):
    r,g,b=p; h,l,s=colorsys.rgb_to_hls(r/255,g/255,b/255)
    if min(p)>=0xe0: return -1
    if r+g+b<150: return 0
    if g>r+20: return 1 if s>0.47 else 2
    if r>g+20: return 3
    return 4
def lijn(p): r,g,b=p; return (r+g+b<230) or (g>r+20 and r+g+b<330)
def kies(A,k,vast=()):
    n=len(A); L=np.array([[lijn(p) for p in row] for row in A])
    cost=[]
    for i in range(n):
        if i==0 or i==n-1: cost.append(1e9); continue
        d=min(np.abs(A[i]-A[i-1]).sum(), np.abs(A[i]-A[i+1]).sum())
        # lijnpixel die in geen van beide buren op dezelfde plek staat = lijnschade
        schade=(L[i]&~L[i-1]&~L[i+1]).sum()
        cost.append(d+600*schade+(1e8 if i in vast else 0))
    gek=[]
    for i in np.argsort(cost,kind='stable'):
        if all(abs(i-j)>=2 for j in gek): gek.append(int(i))
        if len(gek)==k: break
    return sorted(gek),[cost[i] for i in sorted(gek)]
def verklein(x0,x1,y0,y1,W,H,vk=(),vr=()):
    A=NAT[y0:y1+1,x0:x1+1]
    cols,cc=kies(A.transpose(1,0,2),A.shape[1]-W,[c-x0 for c in vk]); B=np.delete(A,cols,1)
    rk=[r-y0 for r in vr]; rows,rc=kies(B,B.shape[0]-H,rk); B=np.delete(B,rows,0)
    out=np.zeros(B.shape[:2],'uint8')
    for y in range(B.shape[0]):
        for x in range(B.shape[1]):
            g=groep(B[y,x])
            if g<0: continue
            ii=GIDX[g]; out[y,x]=ii[((PAL[ii]-B[y,x])**2).sum(1).argmin()]
    return out,[c+x0 for c in cols],[r+y0 for r in rows],cc,rc

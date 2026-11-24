# r18.py: Gnometrotter Rock r18 = Rock af + neus van Ice r9 1-op-1 (Jordi: "wat je hier met de neus hebt gedaan mag
# direct gecopy paste worden naar rock"). Neus = binnenkant (7/8/15) vanaf het neusmidden + rand (1/6) die eraan grenst.
# Waar de Rock-neus buiten de Ice-neus valt: de Rock af-pixel die er het dichtst naast ligt buiten beide neuzen
# (muts/haar/baard in Rock-tinten). Logt elke gewijzigde pixel (r18_log.txt).
import numpy as np, os; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(H,'../af/gnometrotter_rock.png')); R=np.asarray(im).copy(); n=R.copy()
I=np.asarray(Image.open(os.path.join(H,'../../gnometrotter_ice/sprite_r9/gnometrotter_ice.png')))
BOX=(14,28,13,25)   # x0,x1,y0,y1
def neus(A,rand):
    M=np.zeros((64,64),bool); st=[(21,19)]; M[19,21]=True
    while st:
        x,y=st.pop()
        for a,b in ((1,0),(-1,0),(0,1),(0,-1)):
            X,Y=x+a,y+b
            if BOX[0]<=X<=BOX[1] and BOX[2]<=Y<=BOX[3] and not M[Y,X] and A[Y,X] in (7,8,15): M[Y,X]=True; st.append((X,Y))
    N=M.copy()
    for y,x in np.argwhere(M):
        for a in (-1,0,1):
            for b in (-1,0,1):
                if A[y+b,x+a] in rand: N[y+b,x+a]=True
    return N
NI=neus(I,(1,6)); NR=neus(R,(1,6,12))   # Rock af gebruikt ook 12 (donkerroze in het Rock-palet) als neusrand
log=[]
for y,x in np.argwhere(NI):
    if n[y,x]!=I[y,x]: log.append(('ice-neus',x,y,R[y,x],I[y,x])); n[y,x]=I[y,x]
achter=[]
for y,x in np.argwhere(NR&~NI):
    best=None
    for d in range(1,6):
        for a,b in ((-d,0),(d,0),(0,-d),(0,d),(-d,-d),(d,-d),(-d,d),(d,d)):
            X,Y=x+a,y+b
            if not NR[Y,X] and not NI[Y,X] and R[Y,X]!=0: best=(X,Y); break   # niet transparant: silhouet blijft dicht
        if best: break
    v=R[best[1],best[0]]
    if any(R[y+b,x+a]==0 for a,b in ((1,0),(-1,0),(0,1),(0,-1))): v=2   # op de buitenrand: Rock-omlijning (2), zoals Ice daar 2 heeft
    if n[y,x]!=v: log.append(('achter de neus',x,y,R[y,x],v)); n[y,x]=v; achter.append((x,y,best,v))
out=Image.fromarray(n.astype('uint8'),'P'); out.putpalette(im.getpalette())
out.save(os.path.join(H,'gnometrotter_rock.png'),transparency=0)
out.resize((512,512),Image.NEAREST).save(os.path.join(H,'gnometrotter_rock_8x.png'),transparency=0)
with open(os.path.join(H,'r18_log.txt'),'w') as f:
    for z,x,y,a,b in log: f.write('%s (%d,%d) %X -> %X\n'%(z,x,y,a,b))
    for x,y,b,v in achter: f.write('achter: (%d,%d) <- Rock af (%d,%d) = %X\n'%(x,y,b[0],b[1],v))
tel={}
for z,*_ in log: tel[z]=tel.get(z,0)+1
print(tel,'| totaal diff met Rock af:',int((n!=R).sum()),'| buiten de neuzen:',int(((n!=R)&~(NI|NR)).sum()))
